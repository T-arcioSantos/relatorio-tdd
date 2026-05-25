from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    id: int
    name: str
    email: str
    phone: str = ""
