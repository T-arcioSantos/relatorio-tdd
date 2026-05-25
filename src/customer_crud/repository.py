from dataclasses import asdict
import json
from pathlib import Path

from .models import Customer


class CustomerRepository:
    def __init__(self, storage_path: str | Path | None = None) -> None:
        self._storage_path = Path(storage_path) if storage_path else None
        self._customers: dict[int, Customer] = {}
        self._next_id = 1
        self._load()

    def create(self, name: str, email: str, phone: str = "") -> Customer:
        name, email, phone = self._validated_fields(name, email, phone)
        self._ensure_email_is_unique(email)
        customer = Customer(
            id=self._next_id,
            name=name,
            email=email,
            phone=phone,
        )
        self._customers[customer.id] = customer
        self._next_id += 1
        self._save()
        return customer

    def get(self, customer_id: int) -> Customer | None:
        return self._customers.get(customer_id)

    def list(self) -> list[Customer]:
        return [self._customers[key] for key in sorted(self._customers)]

    def update(
        self,
        customer_id: int,
        *,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
    ) -> Customer | None:
        current = self.get(customer_id)
        if current is None:
            return None

        next_name = current.name if name is None else name
        next_email = current.email if email is None else email
        next_phone = current.phone if phone is None else phone
        next_name, next_email, next_phone = self._validated_fields(
            next_name,
            next_email,
            next_phone,
        )
        self._ensure_email_is_unique(next_email, ignored_customer_id=customer_id)

        updated = Customer(
            id=customer_id,
            name=next_name,
            email=next_email,
            phone=next_phone,
        )
        self._customers[customer_id] = updated
        self._save()
        return updated

    def delete(self, customer_id: int) -> bool:
        if customer_id not in self._customers:
            return False
        del self._customers[customer_id]
        self._save()
        return True

    def _load(self) -> None:
        if not self._storage_path or not self._storage_path.exists():
            return

        raw_data = json.loads(self._storage_path.read_text(encoding="utf-8"))
        customers = raw_data.get("customers", [])
        self._customers = {
            item["id"]: Customer(
                id=item["id"],
                name=item["name"],
                email=item["email"],
                phone=item.get("phone", ""),
            )
            for item in customers
        }
        self._next_id = max(self._customers.keys(), default=0) + 1

    def _save(self) -> None:
        if not self._storage_path:
            return

        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"customers": [asdict(customer) for customer in self.list()]}
        self._storage_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _validated_fields(
        self,
        name: str,
        email: str,
        phone: str,
    ) -> tuple[str, str, str]:
        name = name.strip()
        email = email.strip().lower()
        phone = phone.strip()

        if not name:
            raise ValueError("Nome do cliente e obrigatorio.")
        if "@" not in email or email.startswith("@") or email.endswith("@"):
            raise ValueError("E-mail do cliente e invalido.")
        return name, email, phone

    def _ensure_email_is_unique(
        self,
        email: str,
        ignored_customer_id: int | None = None,
    ) -> None:
        for customer in self._customers.values():
            if customer.id == ignored_customer_id:
                continue
            if customer.email == email:
                raise ValueError("Ja existe um cliente com este e-mail.")
