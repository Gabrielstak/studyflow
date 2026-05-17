# 📚 StudyFlow — Organizador de Estudos

[![CI](https://github.com/SEU_USUARIO/studyflow/actions/workflows/ci.yml/badge.svg)](https://github.com/SEU_USUARIO/studyflow/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Versão](https://img.shields.io/badge/versão-1.0.0-green.svg)](CHANGELOG.md)
[![Licença](https://img.shields.io/badge/licença-MIT-lightgrey.svg)](LICENSE)

---

## 🎯 O Problema

Muitos estudantes — especialmente aqueles com TDAH, ansiedade, dificuldades de aprendizado ou rotinas instáveis — têm grande dificuldade em organizar o que precisam estudar, quando estudar e quanto tempo dedicaram a cada matéria. A falta de uma ferramenta simples, acessível e sem distrações contribui para a procrastinação, o esquecimento de prazos e a sensação de improdutividade.

## 💡 A Solução

**StudyFlow** é uma aplicação de linha de comando (CLI) leve e intuitiva que ajuda estudantes a:

- **Registrar e priorizar tarefas** de estudo com prazo e matéria;
- **Acompanhar sessões de estudo** realizadas, com registro de tempo e observações;
- **Visualizar um resumo do desempenho**, incluindo tempo total estudado e matéria mais dedicada.

Sem cadastro, sem internet, sem distração. Apenas foco nos estudos.

## 👥 Público-alvo

Estudantes do ensino médio, técnico e superior que enfrentam dificuldades de organização de rotina de estudos, incluindo pessoas com TDAH, ansiedade ou outras condições que afetam o planejamento.

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| Adicionar tarefa | Cria uma tarefa com título, matéria, prioridade e prazo |
| Listar tarefas | Exibe todas as tarefas ordenadas por prioridade |
| Filtrar pendentes | Mostra apenas as tarefas ainda não concluídas |
| Concluir tarefa | Marca uma tarefa como feita |
| Remover tarefa | Exclui uma tarefa pelo ID |
| Registrar sessão | Salva um bloco de estudo com matéria, duração e observação |
| Ver histórico | Lista todas as sessões de estudo registradas |
| Resumo de desempenho | Exibe estatísticas e gráfico de tempo por matéria |

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+** — linguagem principal
- **json** — persistência de dados local (sem banco de dados externo)
- **pytest** — testes automatizados
- **ruff** — linting e análise estática
- **GitHub Actions** — integração contínua (CI)

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.9 ou superior instalado
- Git instalado

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/studyflow.git
cd studyflow

# 2. (Recomendado) Crie e ative um ambiente virtual
python -m venv .venv

# Linux/macOS:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# 3. Instale as dependências de desenvolvimento
pip install -r requirements-dev.txt
```

> A aplicação em si não possui dependências externas além do Python padrão.

---

## ▶️ Como Executar

```bash
python src/app.py
```

Você verá o menu principal interativo:

```
═══════════════════════════════════════════════════════
       📚  StudyFlow — Organizador de Estudos
═══════════════════════════════════════════════════════

───────────────────────────────────────────────────────
  MENU PRINCIPAL
───────────────────────────────────────────────────────
  1. 📝  Tarefas de estudo
  2. ⏱️   Registrar sessão de estudo
  3. 📊  Ver resumo de desempenho
  0. 🚪  Sair

  Escolha:
```

### Exemplo de uso

**Adicionando uma tarefa:**
```
Escolha: 1
Escolha: 1
  Título: Revisar equações do 2º grau
  Matéria: Matemática
  Prioridade (alta/media/baixa): alta
  Prazo (DD/MM/AAAA): 20/06/2025

  ✅ Tarefa 'Revisar equações do 2º grau' adicionada com ID 1.
```

**Registrando uma sessão de estudo:**
```
Escolha: 2
Escolha: 1
  Matéria estudada: Matemática
  Duração em minutos: 90
  Observação (opcional): Fiz exercícios do capítulo 3

  📖 Sessão de 1h30min em 'Matemática' registrada!
```

**Resumo de desempenho:**
```
  📊  RESUMO DO SEU DESEMPENHO
───────────────────────────────────────────────────────
  Tarefas cadastradas : 3
  ✅ Concluídas        : 1
  ⬜ Pendentes         : 2

  ⏱️  Total estudado   : 2h 30min
  📖 Sessões feitas    : 3
  🏆 Mais estudada    : Matemática

  Tempo por matéria:
    Matemática           █████████████ 1h30min
    Física               ████ 45min
    Português            ███ 15min
```

> Os dados ficam salvos em `~/.studyflow_data.json` e persistem entre execuções.

---

## 🧪 Rodando os Testes

```bash
pytest tests/ -v
```

Para ver o relatório de cobertura:

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

O projeto conta com **20+ testes automatizados** cobrindo:
- ✅ Caminho feliz (uso correto)
- ❌ Entradas inválidas (título vazio, duração negativa, prioridade errada, formato de data)
- ⚠️ Casos limite (lista vazia, tarefa já concluída, ID inexistente)

---

## 🔍 Rodando o Lint (Análise Estática)

```bash
ruff check src/ tests/
```

Para corrigir problemas automaticamente:

```bash
ruff check --fix src/ tests/
```

---

## 🔄 Pipeline de CI (GitHub Actions)

A pipeline é executada automaticamente em todo `push` para `main`/`develop` e em `pull_request`.

**Etapas executadas:**
1. Checkout do código
2. Configuração do Python (3.9 e 3.11)
3. Instalação das dependências
4. Análise estática com `ruff`
5. Execução dos testes com `pytest`
6. Relatório de cobertura

---

## 📁 Estrutura do Projeto

```
studyflow/
├── src/
│   ├── __init__.py
│   └── app.py              # Lógica da aplicação e interface CLI
├── tests/
│   ├── __init__.py
│   └── test_app.py         # Testes automatizados
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline GitHub Actions
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml          # Metadados, versão e configuração de ferramentas
├── requirements-dev.txt    # Dependências de desenvolvimento
└── README.md
```

---

## 📌 Versão

**1.0.0** — Veja o [CHANGELOG.md](CHANGELOG.md) para o histórico de mudanças.

---

## 👤 Autor

**Seu Nome**
- GitHub: [@SEU_USUARIO](https://github.com/SEU_USUARIO)

---

## 🔗 Repositório

[https://github.com/SEU_USUARIO/studyflow](https://github.com/SEU_USUARIO/studyflow)

---

## 📄 Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.
