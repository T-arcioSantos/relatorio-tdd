"""Modelos de dados usados pelo cadastro de clientes."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    """Representa um cliente cadastrado.

    Attributes:
        id: Identificador numerico gerado pelo repositorio.
        name: Nome do cliente.
        email: E-mail usado como identificador unico de contato.
        phone: Telefone opcional do cliente.
    """

    id: int
    name: str
    email: str
    phone: str = ""
