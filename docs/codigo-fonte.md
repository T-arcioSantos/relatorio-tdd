# Documentação do Código Fonte

Esta documentação descreve o funcionamento interno do projeto Cadastro de
Clientes com TDD. O código Python foi mantido sem comentários internos, então a
explicação técnica fica concentrada neste arquivo.

## Objetivo do Software

O sistema implementa um CRUD de clientes executado pelo terminal. Ele permite:

- cadastrar cliente;
- listar clientes cadastrados;
- consultar cliente por identificador;
- atualizar dados de um cliente;
- remover cliente;
- persistir os registros em arquivo JSON.

O projeto foi pensado como fragmento de software para demonstrar a metodologia
TDD em uma atividade acadêmica.

## Organização dos Arquivos

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
  codigo-fonte.md
```

## Módulos do Sistema

| Arquivo | Responsabilidade |
| --- | --- |
| `models.py` | Define a estrutura de dados `Customer` |
| `repository.py` | Implementa as operações do CRUD e as validações |
| `cli.py` | Expõe o CRUD por linha de comando |
| `__init__.py` | Exporta `Customer` e `CustomerRepository` |

## Modelo de Dados

O modelo `Customer` representa um cliente cadastrado.

| Campo | Tipo | Observação |
| --- | --- | --- |
| `id` | `int` | Gerado automaticamente pelo repositório |
| `name` | `str` | Obrigatório |
| `email` | `str` | Obrigatório e único |
| `phone` | `str` | Opcional |

O modelo é imutável porque foi declarado com `@dataclass(frozen=True)`. Quando
um cliente é atualizado, o repositório cria um novo objeto com o mesmo `id` e os
novos valores.

## Repositório de Clientes

O `CustomerRepository` concentra a regra de negócio. Ele mantém os clientes em
memória e, quando recebe um caminho em `storage_path`, grava os dados em JSON.

Métodos principais:

| Método | Função |
| --- | --- |
| `create` | Cria um cliente |
| `get` | Busca um cliente por `id` |
| `list` | Retorna todos os clientes em ordem de cadastro |
| `update` | Atualiza nome, e-mail ou telefone |
| `delete` | Remove um cliente |

### Validações

O repositório aplica três validações antes de salvar ou atualizar um cadastro:

| Validação | Resultado esperado |
| --- | --- |
| Nome em branco | Levanta `ValueError` |
| E-mail sem `@` | Levanta `ValueError` |
| E-mail já cadastrado | Levanta `ValueError` |

Essas validações ficam no repositório porque valem para qualquer forma de uso do
sistema, seja pela CLI ou pelos testes.

## Persistência em JSON

Quando o repositório recebe um caminho de arquivo, ele salva os clientes nesse
formato:

```json
{
  "customers": [
    {
      "id": 1,
      "name": "Ana Silva",
      "email": "ana@example.com",
      "phone": "71999990000"
    }
  ]
}
```

Ao iniciar, o repositório verifica se o arquivo existe. Se existir, carrega os
clientes já gravados e calcula o próximo `id` disponível.

## Interface de Linha de Comando

O arquivo `cli.py` usa `argparse` para transformar comandos do terminal em
chamadas ao repositório.

Comandos disponíveis:

| Comando | Ação |
| --- | --- |
| `add` | Cadastra um cliente |
| `list` | Lista todos os clientes |
| `show` | Consulta um cliente por `id` |
| `update` | Atualiza um cliente |
| `delete` | Remove um cliente |

Exemplo:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m customer_crud.cli --db data/customers.json add --name "Ana Silva" --email "ana@example.com"
```

## Testes Automatizados

Os testes ficam na pasta `tests`.

| Arquivo | O que verifica |
| --- | --- |
| `test_customer_repository.py` | CRUD, validações e persistência |
| `test_cli.py` | Uso da CLI com arquivo JSON |

Para executar:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests
```

## Relação com TDD

O desenvolvimento seguiu ciclos pequenos:

1. escrever um teste para um comportamento esperado;
2. executar o teste e observar a falha;
3. implementar o código mínimo para passar;
4. rodar a suíte novamente;
5. ajustar a organização sem alterar o comportamento.

Esse fluxo aparece na cobertura dos testes. O repositório foi testado primeiro,
pois ele concentra as regras do sistema. Depois foi criado um teste para a CLI,
garantindo que o usuário consegue cadastrar e listar clientes pelo terminal.

## Como Visualizar Esta Documentação

Pelo terminal:

```powershell
Get-Content docs\codigo-fonte.md
```

No VS Code:

```powershell
code docs\codigo-fonte.md
```

No próprio gerenciador de arquivos, também é possível abrir o arquivo
`docs/codigo-fonte.md` com qualquer editor de texto ou visualizador Markdown.
