"""Pacote do CRUD de clientes desenvolvido com TDD."""

from .models import Customer
from .repository import CustomerRepository

__all__ = ["Customer", "CustomerRepository"]
