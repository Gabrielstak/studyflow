"""
Módulo de integração com a Open Trivia DB API.
Busca questões de revisão ao final de uma sessão de estudos.
"""

import requests


def buscar_questoes(quantidade: int = 3) -> list:
    """
    Busca questões de revisão na Open Trivia DB (sem necessidade de chave).
    Retorna uma lista de questões de múltipla escolha.
    """
    url = f"https://opentdb.com/api.php?amount={quantidade}&type=multiple"

    resposta = requests.get(url, timeout=5)
    resposta.raise_for_status()

    dados = resposta.json()
    return dados["results"]


def exibir_questoes(questoes: list) -> None:
    """Exibe as questões de revisão no terminal."""
    print("\n" + "─" * 55)
    print("  🎯  QUESTÕES DE REVISÃO")
    print("─" * 55)
    print("  Teste seu conhecimento antes de fechar!\n")

    for i, q in enumerate(questoes, 1):
        print(f"  {i}. {q['question']}\n")
        opcoes = q["incorrect_answers"] + [q["correct_answer"]]
        for j, opcao in enumerate(opcoes, 1):
            print(f"     {j}) {opcao}")
        print()

    input("  Pressione Enter para ver os gabaritos...")
    print()
    for i, q in enumerate(questoes, 1):
        print(f"  ✅ Questão {i}: {q['correct_answer']}")
    print()