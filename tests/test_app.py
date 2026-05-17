"""
Testes automatizados do StudyFlow.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import (
    add_task,
    complete_task,
    generate_id,
    get_summary,
    list_tasks,
    log_session,
    remove_task,
)

# ─── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def empty_data():
    return {"tasks": [], "sessions": []}


@pytest.fixture
def data_com_tarefa(empty_data):
    add_task(empty_data, "Revisar álgebra", "Matemática", "alta", "31/12/2025")
    return empty_data


# ─── generate_id ───────────────────────────────────────────────────────────────

def test_generate_id_lista_vazia(empty_data):
    assert generate_id(empty_data["tasks"]) == 1


def test_generate_id_incrementa(data_com_tarefa):
    novo_id = generate_id(data_com_tarefa["tasks"])
    assert novo_id == 2


# ─── add_task ──────────────────────────────────────────────────────────────────

def test_add_task_caminho_feliz(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    task = add_task(empty_data, "Estudar física", "Física", "media", "15/06/2025")
    assert task["titulo"] == "Estudar física"
    assert task["materia"] == "Física"
    assert task["prioridade"] == "media"
    assert task["concluida"] is False
    assert task["id"] == 1


def test_add_task_titulo_vazio(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    with pytest.raises(ValueError, match="título"):
        add_task(empty_data, "   ", "Química", "baixa", "01/01/2026")


def test_add_task_materia_vazia(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    with pytest.raises(ValueError, match="matéria"):
        add_task(empty_data, "Tarefa válida", "   ", "baixa", "01/01/2026")


def test_add_task_prioridade_invalida(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    with pytest.raises(ValueError, match="Prioridade inválida"):
        add_task(empty_data, "Tarefa X", "História", "urgente", "10/10/2025")


def test_add_task_prazo_formato_errado(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    with pytest.raises(ValueError, match="prazo inválido"):
        add_task(empty_data, "Tarefa Y", "Biologia", "media", "2025-12-01")


# ─── list_tasks ────────────────────────────────────────────────────────────────

def test_list_tasks_retorna_todas(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    add_task(empty_data, "T1", "Mat", "alta", "01/01/2026")
    add_task(empty_data, "T2", "Fis", "baixa", "02/01/2026")
    result = list_tasks(empty_data)
    assert len(result) == 2


def test_list_tasks_filtra_por_materia(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    add_task(empty_data, "T1", "Matemática", "alta", "01/01/2026")
    add_task(empty_data, "T2", "Física", "baixa", "02/01/2026")
    result = list_tasks(empty_data, filtro_materia="Matemática")
    assert len(result) == 1
    assert result[0]["materia"] == "Matemática"


def test_list_tasks_apenas_pendentes(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    add_task(empty_data, "T1", "Mat", "alta", "01/01/2026")
    add_task(empty_data, "T2", "Fis", "baixa", "02/01/2026")
    complete_task(empty_data, 1)
    pendentes = list_tasks(empty_data, apenas_pendentes=True)
    assert len(pendentes) == 1
    assert pendentes[0]["titulo"] == "T2"


def test_list_tasks_ordenada_por_prioridade(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    add_task(empty_data, "Baixa", "Mat", "baixa", "01/01/2026")
    add_task(empty_data, "Alta", "Mat", "alta", "01/01/2026")
    add_task(empty_data, "Media", "Mat", "media", "01/01/2026")
    result = list_tasks(empty_data)
    assert result[0]["prioridade"] == "alta"
    assert result[1]["prioridade"] == "media"
    assert result[2]["prioridade"] == "baixa"


# ─── complete_task ─────────────────────────────────────────────────────────────

def test_complete_task_caminho_feliz(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    add_task(empty_data, "Tarefa", "Mat", "alta", "01/01/2026")
    task = complete_task(empty_data, 1)
    assert task["concluida"] is True


def test_complete_task_id_inexistente(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    with pytest.raises(ValueError, match="não encontrada"):
        complete_task(empty_data, 999)


def test_complete_task_ja_concluida(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    add_task(empty_data, "Tarefa", "Mat", "alta", "01/01/2026")
    complete_task(empty_data, 1)
    with pytest.raises(ValueError, match="já está concluída"):
        complete_task(empty_data, 1)


# ─── remove_task ───────────────────────────────────────────────────────────────

def test_remove_task_caminho_feliz(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    add_task(empty_data, "Tarefa", "Mat", "alta", "01/01/2026")
    removed = remove_task(empty_data, 1)
    assert removed["titulo"] == "Tarefa"
    assert len(empty_data["tasks"]) == 0


def test_remove_task_id_inexistente(empty_data):
    with pytest.raises(ValueError, match="não encontrada"):
        remove_task(empty_data, 42)


# ─── log_session ───────────────────────────────────────────────────────────────

def test_log_session_caminho_feliz(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    session = log_session(empty_data, "Português", 90)
    assert session["materia"] == "Português"
    assert session["duracao_min"] == 90
    assert session["id"] == 1


def test_log_session_duracao_zero(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    with pytest.raises(ValueError, match="maior que zero"):
        log_session(empty_data, "Química", 0)


def test_log_session_duracao_negativa(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    with pytest.raises(ValueError, match="maior que zero"):
        log_session(empty_data, "Química", -30)


def test_log_session_materia_vazia(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    with pytest.raises(ValueError, match="matéria"):
        log_session(empty_data, "   ", 60)


# ─── get_summary ───────────────────────────────────────────────────────────────

def test_get_summary_vazio(empty_data):
    summary = get_summary(empty_data)
    assert summary["total_tasks"] == 0
    assert summary["concluidas"] == 0
    assert summary["total_horas"] == 0
    assert summary["materia_mais_estudada"] is None


def test_get_summary_com_dados(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    add_task(empty_data, "T1", "Mat", "alta", "01/01/2026")
    add_task(empty_data, "T2", "Fis", "baixa", "02/01/2026")
    complete_task(empty_data, 1)
    log_session(empty_data, "Matemática", 120)
    log_session(empty_data, "Matemática", 60)
    log_session(empty_data, "Física", 30)

    summary = get_summary(empty_data)
    assert summary["total_tasks"] == 2
    assert summary["concluidas"] == 1
    assert summary["pendentes"] == 1
    assert summary["total_horas"] == 3
    assert summary["total_minutos_extra"] == 30
    assert summary["materia_mais_estudada"] == "Matemática"


def test_get_summary_horas_calculadas_corretamente(empty_data, monkeypatch):
    monkeypatch.setattr("app.save_data", lambda d: None)
    log_session(empty_data, "Bio", 90)  # 1h30min
    summary = get_summary(empty_data)
    assert summary["total_horas"] == 1
    assert summary["total_minutos_extra"] == 30
