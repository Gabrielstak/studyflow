"""
StudyFlow - Organizador de Estudos CLI
Versão: 1.0.0
"""

import json
from datetime import date, datetime
from pathlib import Path

DATA_FILE = Path.home() / ".studyflow_data.json"


def load_data() -> dict:
    """Carrega os dados salvos do arquivo JSON."""
    if DATA_FILE.exists():
        with open(DATA_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"tasks": [], "sessions": []}


def save_data(data: dict) -> None:
    """Salva os dados no arquivo JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_id(items: list) -> int:
    """Gera um ID único baseado no maior ID existente."""
    if not items:
        return 1
    return max(item["id"] for item in items) + 1


def add_task(data: dict, titulo: str, materia: str, prioridade: str, prazo: str) -> dict:
    """Adiciona uma nova tarefa de estudo."""
    prioridades_validas = ["alta", "media", "baixa"]
    if prioridade.lower() not in prioridades_validas:
        raise ValueError(f"Prioridade inválida. Use: {', '.join(prioridades_validas)}")

    if not titulo.strip():
        raise ValueError("O título da tarefa não pode ser vazio.")

    if not materia.strip():
        raise ValueError("A matéria não pode ser vazia.")

    try:
        datetime.strptime(prazo, "%d/%m/%Y")
    except ValueError:
        raise ValueError("Formato de prazo inválido. Use DD/MM/AAAA.")

    task = {
        "id": generate_id(data["tasks"]),
        "titulo": titulo.strip(),
        "materia": materia.strip(),
        "prioridade": prioridade.lower(),
        "prazo": prazo,
        "concluida": False,
        "criada_em": date.today().strftime("%d/%m/%Y"),
    }
    data["tasks"].append(task)
    save_data(data)
    return task


def list_tasks(data: dict, filtro_materia: str = None, apenas_pendentes: bool = False) -> list:
    """Lista as tarefas, com filtros opcionais."""
    tasks = data["tasks"]

    if filtro_materia:
        tasks = [t for t in tasks if t["materia"].lower() == filtro_materia.lower()]

    if apenas_pendentes:
        tasks = [t for t in tasks if not t["concluida"]]

    prioridade_ordem = {"alta": 0, "media": 1, "baixa": 2}
    return sorted(tasks, key=lambda t: prioridade_ordem.get(t["prioridade"], 9))


def complete_task(data: dict, task_id: int) -> dict:
    """Marca uma tarefa como concluída."""
    for task in data["tasks"]:
        if task["id"] == task_id:
            if task["concluida"]:
                raise ValueError("Essa tarefa já está concluída.")
            task["concluida"] = True
            save_data(data)
            return task
    raise ValueError(f"Tarefa com ID {task_id} não encontrada.")


def remove_task(data: dict, task_id: int) -> dict:
    """Remove uma tarefa pelo ID."""
    for i, task in enumerate(data["tasks"]):
        if task["id"] == task_id:
            removed = data["tasks"].pop(i)
            save_data(data)
            return removed
    raise ValueError(f"Tarefa com ID {task_id} não encontrada.")


def log_session(data: dict, materia: str, duracao_min: int, nota: str = "") -> dict:
    """Registra uma sessão de estudo realizada."""
    if duracao_min <= 0:
        raise ValueError("A duração deve ser maior que zero minutos.")

    if not materia.strip():
        raise ValueError("A matéria não pode ser vazia.")

    session = {
        "id": generate_id(data["sessions"]),
        "materia": materia.strip(),
        "duracao_min": duracao_min,
        "nota": nota.strip(),
        "data": date.today().strftime("%d/%m/%Y"),
    }
    data["sessions"].append(session)
    save_data(data)
    return session


def get_summary(data: dict) -> dict:
    """Retorna um resumo geral do desempenho do estudante."""
    tasks = data["tasks"]
    sessions = data["sessions"]

    total_tasks = len(tasks)
    concluidas = sum(1 for t in tasks if t["concluida"])
    pendentes = total_tasks - concluidas

    total_min = sum(s["duracao_min"] for s in sessions)
    horas = total_min // 60
    minutos = total_min % 60

    materias: dict = {}
    for s in sessions:
        materias[s["materia"]] = materias.get(s["materia"], 0) + s["duracao_min"]

    materia_top = max(materias, key=materias.get) if materias else None

    return {
        "total_tasks": total_tasks,
        "concluidas": concluidas,
        "pendentes": pendentes,
        "total_horas": horas,
        "total_minutos_extra": minutos,
        "sessoes_registradas": len(sessions),
        "materia_mais_estudada": materia_top,
        "minutos_por_materia": materias,
    }


# ─── Helpers de exibição ───────────────────────────────────────────────────────

PRIORIDADE_EMOJI = {"alta": "🔴", "media": "🟡", "baixa": "🟢"}
SEP = "─" * 55


def print_header():
    print("\n" + "═" * 55)
    print("       📚  StudyFlow — Organizador de Estudos")
    print("═" * 55)


def print_task(task: dict):
    status = "✅" if task["concluida"] else "⬜"
    pri = PRIORIDADE_EMOJI.get(task["prioridade"], "")
    print(f"  [{task['id']:>3}] {status} {pri}  {task['titulo']}")
    print(f"        Matéria: {task['materia']}  |  Prazo: {task['prazo']}")


def print_session(session: dict):
    h = session["duracao_min"] // 60
    m = session["duracao_min"] % 60
    duracao_str = f"{h}h{m:02d}min" if h else f"{m}min"
    print(f"  [{session['id']:>3}] 📖 {session['materia']}  —  {duracao_str}  ({session['data']})")
    if session["nota"]:
        print(f"        Nota: {session['nota']}")


# ─── Menu principal ────────────────────────────────────────────────────────────

def menu_tarefas(data: dict):
    while True:
        print(f"\n{SEP}")
        print("  TAREFAS DE ESTUDO")
        print(SEP)
        print("  1. Adicionar tarefa")
        print("  2. Listar todas as tarefas")
        print("  3. Listar tarefas pendentes")
        print("  4. Marcar tarefa como concluída")
        print("  5. Remover tarefa")
        print("  0. Voltar")
        opcao = input("\n  Escolha: ").strip()

        if opcao == "1":
            print(f"\n{SEP}  Nova Tarefa")
            titulo = input("  Título: ")
            materia = input("  Matéria: ")
            prioridade = input("  Prioridade (alta/media/baixa): ")
            prazo = input("  Prazo (DD/MM/AAAA): ")
            try:
                task = add_task(data, titulo, materia, prioridade, prazo)
                print(f"\n  ✅ Tarefa '{task['titulo']}' adicionada com ID {task['id']}.")
            except ValueError as e:
                print(f"\n  ❌ Erro: {e}")

        elif opcao == "2":
            tasks = list_tasks(data)
            print(f"\n{SEP}  Todas as Tarefas ({len(tasks)})")
            if not tasks:
                print("  Nenhuma tarefa cadastrada.")
            for t in tasks:
                print_task(t)

        elif opcao == "3":
            tasks = list_tasks(data, apenas_pendentes=True)
            print(f"\n{SEP}  Tarefas Pendentes ({len(tasks)})")
            if not tasks:
                print("  Nenhuma tarefa pendente. 🎉")
            for t in tasks:
                print_task(t)

        elif opcao == "4":
            task_id = input("  ID da tarefa a concluir: ")
            try:
                task = complete_task(data, int(task_id))
                print(f"\n  ✅ Tarefa '{task['titulo']}' marcada como concluída!")
            except (ValueError, TypeError) as e:
                print(f"\n  ❌ Erro: {e}")

        elif opcao == "5":
            task_id = input("  ID da tarefa a remover: ")
            try:
                task = remove_task(data, int(task_id))
                print(f"\n  🗑️  Tarefa '{task['titulo']}' removida.")
            except (ValueError, TypeError) as e:
                print(f"\n  ❌ Erro: {e}")

        elif opcao == "0":
            break
        else:
            print("  ⚠️  Opção inválida.")


def menu_sessoes(data: dict):
    while True:
        print(f"\n{SEP}")
        print("  SESSÕES DE ESTUDO")
        print(SEP)
        print("  1. Registrar sessão de estudo")
        print("  2. Ver histórico de sessões")
        print("  0. Voltar")
        opcao = input("\n  Escolha: ").strip()

        if opcao == "1":
            print(f"\n{SEP}  Nova Sessão")
            materia = input("  Matéria estudada: ")
            try:
                duracao = int(input("  Duração em minutos: "))
            except ValueError:
                print("\n  ❌ Duração deve ser um número inteiro.")
                continue
            nota = input("  Observação (opcional, Enter para pular): ")
            try:
                session = log_session(data, materia, duracao, nota)
                h = session["duracao_min"] // 60
                m = session["duracao_min"] % 60
                dur_str = f"{h}h{m:02d}min" if h else f"{m}min"
                print(f"\n  📖 Sessão de {dur_str} em '{session['materia']}' registrada!")
            except ValueError as e:
                print(f"\n  ❌ Erro: {e}")

        elif opcao == "2":
            sessions = data["sessions"]
            print(f"\n{SEP}  Histórico ({len(sessions)} sessões)")
            if not sessions:
                print("  Nenhuma sessão registrada ainda.")
            for s in sessions:
                print_session(s)

        elif opcao == "0":
            break
        else:
            print("  ⚠️  Opção inválida.")


def menu_resumo(data: dict):
    s = get_summary(data)
    print(f"\n{SEP}")
    print("  📊  RESUMO DO SEU DESEMPENHO")
    print(SEP)
    print(f"  Tarefas cadastradas : {s['total_tasks']}")
    print(f"  ✅ Concluídas        : {s['concluidas']}")
    print(f"  ⬜ Pendentes         : {s['pendentes']}")
    print(f"\n  ⏱️  Total estudado   : {s['total_horas']}h {s['total_minutos_extra']}min")
    print(f"  📖 Sessões feitas    : {s['sessoes_registradas']}")
    if s["materia_mais_estudada"]:
        print(f"  🏆 Mais estudada    : {s['materia_mais_estudada']}")
    if s["minutos_por_materia"]:
        print("\n  Tempo por matéria:")
        for mat, mins in sorted(s["minutos_por_materia"].items(), key=lambda x: -x[1]):
            h, m = mins // 60, mins % 60
            bar = "█" * min((mins // 10), 20)
            print(f"    {mat:<20} {bar} {h}h{m:02d}min")
    print(SEP)
    input("\n  Pressione Enter para voltar...")


def main():
    """Ponto de entrada principal da aplicação StudyFlow."""
    data = load_data()
    print_header()

    while True:
        print(f"\n{SEP}")
        print("  MENU PRINCIPAL")
        print(SEP)
        print("  1. 📝  Tarefas de estudo")
        print("  2. ⏱️   Registrar sessão de estudo")
        print("  3. 📊  Ver resumo de desempenho")
        print("  0. 🚪  Sair")
        opcao = input("\n  Escolha: ").strip()

        if opcao == "1":
            menu_tarefas(data)
        elif opcao == "2":
            menu_sessoes(data)
        elif opcao == "3":
            menu_resumo(data)
        elif opcao == "0":
            print("\n  Até logo! Continue estudando. 💪\n")
            break
        else:
            print("  ⚠️  Opção inválida.")


if __name__ == "__main__":
    main()
