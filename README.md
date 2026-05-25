<p align="center">
  <h1 align="center">Cadastro de Clientes com TDD</h1>
  <p align="center">
    Um CRUD de clientes em Python, criado para demonstrar TDD com testes automatizados, persistência em JSON e uso pelo terminal.
  </p>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Testes" src="https://img.shields.io/badge/Testes-unittest-2E7D32?style=for-the-badge">
  <img alt="Documentação" src="https://img.shields.io/badge/Docs-Doxygen-0A7CBD?style=for-the-badge">
  <img alt="Persistência" src="https://img.shields.io/badge/Dados-JSON-F59E0B?style=for-the-badge">
  <img alt="Dependências" src="https://img.shields.io/badge/Dependências-zero-111827?style=for-the-badge">
</p>

---

## O que este projeto faz

Este projeto implementa um cadastro de clientes simples, mas completo o bastante
para mostrar o ciclo de TDD na prática. Ele permite cadastrar, listar, consultar,
atualizar e remover clientes pelo terminal.

Foi feito para uma atividade acadêmica de Engenharia de Software, com foco em
testes antes da implementação e organização clara do código.

## Sumário

- [Demonstração rápida](#demonstração-rápida)
- [Como funciona](#como-funciona)
- [Funcionalidades](#funcionalidades)
- [Instalação e execução](#instalação-e-execução)
- [Testes](#testes)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Documentação técnica](#documentação-técnica)
  - [Por que Doxygen?](#por-que-doxygen)
  - [Gerar e visualizar](#gerar-e-visualizar)

## Demonstração rápida

Windows:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m customer_crud.cli --db data/customers.json add --name "Ana Silva" --email "ana@example.com" --phone "71999990000"
```

Linux/macOS:

```bash
export PYTHONPATH="$PWD/src"
python -m customer_crud.cli --db data/customers.json add --name "Ana Silva" --email "ana@example.com" --phone "71999990000"
```

Também é possível quebrar o comando em várias linhas.

Windows:

```powershell
python -m customer_crud.cli --db data/customers.json add `
  --name "Ana Silva" `
  --email "ana@example.com" `
  --phone "71999990000"
```

Linux/macOS:

```bash
python -m customer_crud.cli --db data/customers.json add \
  --name "Ana Silva" \
  --email "ana@example.com" \
  --phone "71999990000"
```

Saída esperada:

```text
Cliente 1 cadastrado: Ana Silva
```

Listando os clientes:

```bash
python -m customer_crud.cli --db data/customers.json list
```

```text
1 | Ana Silva | ana@example.com | 71999990000
```

## Como funciona

```mermaid
flowchart LR
    A["Comando no terminal"] --> B["cli.py"]
    B --> C["CustomerRepository"]
    C --> D["Valida regras do cliente"]
    D --> E["Salva ou lê JSON"]
    C --> F["Retorna resultado ao usuário"]
```

A interface de linha de comando recebe a ação do usuário e chama o repositório.
O repositório concentra as regras do CRUD, valida os dados e grava os clientes
em um arquivo JSON quando um caminho é informado com `--db`.

## Funcionalidades

| Recurso | O que acontece |
| --- | --- |
| Cadastro | Cria cliente com `id`, nome, e-mail e telefone |
| Listagem | Mostra todos os clientes em ordem de cadastro |
| Consulta | Busca cliente pelo identificador |
| Atualização | Altera nome, e-mail ou telefone preservando o mesmo `id` |
| Remoção | Exclui o cliente informado |
| Validação | Recusa nome vazio, e-mail inválido e e-mail repetido |
| Persistência | Salva os dados em JSON |

## Instalação e execução

Requisito:

```text
Python 3.10 ou superior
```

O projeto não precisa de pacotes externos.

Antes de executar os comandos, configure o caminho do código fonte:

Windows:

```powershell
$env:PYTHONPATH = "$PWD\src"
```

Linux/macOS:

```bash
export PYTHONPATH="$PWD/src"
```

Cadastrar:

```bash
python -m customer_crud.cli --db data/customers.json add --name "Ana Silva" --email "ana@example.com" --phone "71999990000"
```

Listar:

```bash
python -m customer_crud.cli --db data/customers.json list
```

Consultar:

```bash
python -m customer_crud.cli --db data/customers.json show 1
```

Atualizar:

```bash
python -m customer_crud.cli --db data/customers.json update 1 --name "Ana Costa" --email "ana.costa@example.com"
```

Remover:

```bash
python -m customer_crud.cli --db data/customers.json delete 1
```

## Testes

A ferramenta de testes usada é o `unittest`, que já vem com o Python. Essa
escolha mantém o projeto fácil de rodar em qualquer máquina, sem instalar
dependências.

Execute a suíte:

Windows:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests
```

Linux/macOS:

```bash
export PYTHONPATH="$PWD/src"
python -m unittest discover -s tests
```

Saída esperada:

```text
Ran 7 tests

OK
```

Os testes cobrem:

| Arquivo | Cobertura |
| --- | --- |
| `tests/test_customer_repository.py` | CRUD, validações e persistência |
| `tests/test_cli.py` | Fluxo de cadastro e listagem pela CLI |

## Estrutura do projeto

```text
src/customer_crud/
  __init__.py
  cli.py
  models.py
  repository.py

tests/
  test_cli.py
  test_customer_repository.py

docs/
  doxygen/html/
```

## Documentação técnica

A documentação do código fonte é gerada com **Doxygen** a partir da pasta
`src`. O código usa docstrings Pythonicas em módulos, classes e funções
principais. A escolha foi feita porque o Doxygen é mais amplo que ferramentas
focadas apenas em Python, como `pdoc`, e pode ser usado em projetos com
diferentes linguagens.

O arquivo de configuração da ferramenta é:

```text
Doxyfile
```

Entrada documentada:

```text
src/
```

Saídas geradas:

```text
docs/doxygen/html/index.html
docs/doxygen/cadastro-clientes-doxygen.pdf
```

### Por que Doxygen?

| Ferramenta | Melhor uso | Motivo da escolha |
| --- | --- | --- |
| `pdoc` | Projetos Python | Simples, mas focado em uma linguagem |
| `Doxygen` | Projetos em várias linguagens | Atende melhor à exigência de uma ferramenta ampla |

### Gerar e visualizar

Para gerar a documentação:

```bash
doxygen Doxyfile
```

Depois da geração, abra:

```text
docs/doxygen/html/index.html
```

O PDF da documentação fica em:

```text
docs/doxygen/cadastro-clientes-doxygen.pdf
```

Para recriar o PDF a partir da saída LaTeX do Doxygen, é necessário ter uma
distribuição LaTeX instalada.

Windows:

```powershell
Set-Location docs\doxygen\latex
.\make.bat
Copy-Item refman.pdf ..\cadastro-clientes-doxygen.pdf -Force
```

Linux/macOS:

```bash
cd docs/doxygen/latex
make
cp refman.pdf ../cadastro-clientes-doxygen.pdf
```

Para abrir pelo terminal:

Windows:

```powershell
Start-Process docs\doxygen\html\index.html
```

Linux:

```bash
xdg-open docs/doxygen/html/index.html
```

macOS:

```bash
open docs/doxygen/html/index.html
```
