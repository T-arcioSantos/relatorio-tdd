"""Interface de linha de comando do cadastro de clientes."""

from argparse import ArgumentParser, Namespace
from pathlib import Path

from .repository import CustomerRepository

DEFAULT_STORAGE_PATH = Path("data/customers.json")


def build_parser() -> ArgumentParser:
    """Cria o parser com todos os comandos aceitos pela CLI."""
    parser = ArgumentParser(
        prog="customer-crud",
        description="CRUD de clientes com persistencia em JSON.",
    )
    parser.add_argument(
        "--db",
        default=str(DEFAULT_STORAGE_PATH),
        help="Arquivo JSON usado para armazenar os clientes.",
    )

    subcommands = parser.add_subparsers(dest="command", required=True)

    add_parser = subcommands.add_parser("add", help="Cadastra um cliente.")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--email", required=True)
    add_parser.add_argument("--phone", default="")

    subcommands.add_parser("list", help="Lista todos os clientes.")

    show_parser = subcommands.add_parser("show", help="Consulta um cliente.")
    show_parser.add_argument("id", type=int)

    update_parser = subcommands.add_parser("update", help="Atualiza um cliente.")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("--name")
    update_parser.add_argument("--email")
    update_parser.add_argument("--phone")

    delete_parser = subcommands.add_parser("delete", help="Remove um cliente.")
    delete_parser.add_argument("id", type=int)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Executa a CLI.

    Args:
        argv: Lista opcional de argumentos. Quando ``None``, usa os argumentos
            recebidos pelo processo.

    Returns:
        Codigo de saida. Retorna ``0`` em sucesso e ``1`` em erro de validacao
        ou cliente nao encontrado.
    """
    args = build_parser().parse_args(argv)
    repo = CustomerRepository(storage_path=args.db)

    try:
        return _dispatch(args, repo)
    except ValueError as error:
        print(f"Erro: {error}")
        return 1


def _dispatch(args: Namespace, repo: CustomerRepository) -> int:
    """Executa o comando selecionado no parser."""
    if args.command == "add":
        customer = repo.create(args.name, args.email, args.phone)
        print(f"Cliente {customer.id} cadastrado: {customer.name}")
        return 0

    if args.command == "list":
        customers = repo.list()
        if not customers:
            print("Nenhum cliente cadastrado.")
            return 0
        for customer in customers:
            print(_format_customer(customer.id, customer.name, customer.email, customer.phone))
        return 0

    if args.command == "show":
        customer = repo.get(args.id)
        if customer is None:
            print("Cliente nao encontrado.")
            return 1
        print(_format_customer(customer.id, customer.name, customer.email, customer.phone))
        return 0

    if args.command == "update":
        customer = repo.update(
            args.id,
            name=args.name,
            email=args.email,
            phone=args.phone,
        )
        if customer is None:
            print("Cliente nao encontrado.")
            return 1
        print(f"Cliente {customer.id} atualizado: {customer.name}")
        return 0

    if args.command == "delete":
        if not repo.delete(args.id):
            print("Cliente nao encontrado.")
            return 1
        print(f"Cliente {args.id} removido.")
        return 0

    print("Comando invalido.")
    return 1


def _format_customer(customer_id: int, name: str, email: str, phone: str) -> str:
    """Formata um cliente para exibicao no terminal."""
    phone_text = phone if phone else "sem telefone"
    return f"{customer_id} | {name} | {email} | {phone_text}"


if __name__ == "__main__":
    raise SystemExit(main())
