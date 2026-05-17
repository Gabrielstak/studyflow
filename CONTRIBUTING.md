# Como Contribuir

Obrigado por querer contribuir com o StudyFlow! 🎉

## Fluxo de trabalho

1. Faça um **fork** do repositório.
2. Crie uma branch descritiva a partir de `main`:
   ```bash
   git checkout -b feature/nome-da-funcionalidade
   ```
3. Implemente as mudanças e adicione testes para novos comportamentos.
4. Certifique-se de que lint e testes passam localmente:
   ```bash
   ruff check src/ tests/
   pytest tests/
   ```
5. Faça commit com mensagem clara:
   ```bash
   git commit -m "feat: adiciona filtro de tarefas por prazo"
   ```
6. Abra um **Pull Request** descrevendo o que foi feito e por quê.

## Padrão de commits

Use o padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/):

| Prefixo    | Uso                                      |
|------------|------------------------------------------|
| `feat:`    | Nova funcionalidade                      |
| `fix:`     | Correção de bug                          |
| `docs:`    | Alterações na documentação               |
| `test:`    | Adição ou correção de testes             |
| `refactor:`| Refatoração sem mudança de comportamento |
| `chore:`   | Tarefas de manutenção                    |

## Regras gerais

- Mantenha o código compatível com Python 3.9+.
- Siga o estilo verificado pelo `ruff`.
- Novos comportamentos devem ter testes correspondentes.
- PRs sem testes serão solicitados a incluí-los antes do merge.
