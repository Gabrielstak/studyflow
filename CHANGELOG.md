# Changelog

Todas as mudanças notáveis neste projeto são documentadas neste arquivo.

O formato segue o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)
e este projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [1.0.0] — 2025

### Adicionado
- Interface CLI interativa com menu principal
- Módulo de **tarefas de estudo**: adicionar, listar, concluir e remover tarefas
- Filtro de tarefas por matéria e por status (pendente/concluída)
- Ordenação automática de tarefas por prioridade (alta → média → baixa)
- Módulo de **sessões de estudo**: registrar tempo estudado por matéria com nota opcional
- Histórico de sessões com duração formatada (horas e minutos)
- **Resumo de desempenho** com estatísticas: tarefas concluídas, tempo total, matéria mais estudada e gráfico de barras por matéria
- Persistência de dados em arquivo JSON no diretório do usuário (`~/.studyflow_data.json`)
- Validação de entradas com mensagens de erro amigáveis
- Testes automatizados com `pytest` cobrindo caminho feliz, entradas inválidas e casos limite
- Análise estática de código com `ruff`
- Pipeline de integração contínua com GitHub Actions (Python 3.9 e 3.11)
- Documentação completa no `README.md`
