"""
Testes de integração — valida a comunicação com a Open Trivia DB API.
"""

import pytest
import sys
import os
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from api_questoes import buscar_questoes


def test_buscar_questoes_mock_retorna_lista():
    mock_response = Mock()
    mock_response.json.return_value = {
        "results": [
            {
                "question": "Qual linguagem é usada no StudyFlow?",
                "correct_answer": "Python",
                "incorrect_answers": ["Java", "C++", "Ruby"],
            }
        ]
    }
    mock_response.raise_for_status = Mock()

    with patch("api_questoes.requests.get", return_value=mock_response):
        questoes = buscar_questoes(quantidade=1)
        assert isinstance(questoes, list)
        assert len(questoes) == 1
        assert questoes[0]["correct_answer"] == "Python"
        assert "incorrect_answers" in questoes[0]


def test_buscar_questoes_mock_estrutura_correta():
    mock_response = Mock()
    mock_response.json.return_value = {
        "results": [
            {
                "question": "Pergunta de teste?",
                "correct_answer": "Resposta certa",
                "incorrect_answers": ["Errada 1", "Errada 2", "Errada 3"],
            },
            {
                "question": "Segunda pergunta?",
                "correct_answer": "Outra resposta",
                "incorrect_answers": ["Errada A", "Errada B", "Errada C"],
            },
        ]
    }
    mock_response.raise_for_status = Mock()

    with patch("api_questoes.requests.get", return_value=mock_response):
        questoes = buscar_questoes(quantidade=2)
        assert len(questoes) == 2
        for q in questoes:
            assert "question" in q
            assert "correct_answer" in q
            assert "incorrect_answers" in q


def test_buscar_questoes_erro_de_rede():
    import requests

    with patch("api_questoes.requests.get", side_effect=requests.exceptions.ConnectionError):
        with pytest.raises(requests.exceptions.ConnectionError):
            buscar_questoes()