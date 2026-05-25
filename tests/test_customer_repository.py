from pathlib import Path
import unittest

from customer_crud import CustomerRepository


class CustomerRepositoryTest(unittest.TestCase):
    def test_create_customer_and_get_by_id(self):
        repo = CustomerRepository()

        customer = repo.create(
            name="Ana Silva",
            email="ana@example.com",
            phone="71999990000",
        )

        self.assertEqual(1, customer.id)
        self.assertEqual("Ana Silva", customer.name)
        self.assertEqual(customer, repo.get(customer.id))

    def test_list_customers_in_creation_order(self):
        repo = CustomerRepository()

        first = repo.create("Ana Silva", "ana@example.com")
        second = repo.create("Bruno Lima", "bruno@example.com")

        self.assertEqual([first, second], repo.list())

    def test_update_customer_keeps_the_same_id(self):
        repo = CustomerRepository()
        customer = repo.create("Ana Silva", "ana@example.com")

        updated = repo.update(
            customer.id,
            name="Ana Costa",
            email="ana.costa@example.com",
            phone="7133334444",
        )

        self.assertEqual(customer.id, updated.id)
        self.assertEqual("Ana Costa", updated.name)
        self.assertEqual(updated, repo.get(customer.id))

    def test_delete_customer_removes_it_from_repository(self):
        repo = CustomerRepository()
        customer = repo.create("Ana Silva", "ana@example.com")

        self.assertTrue(repo.delete(customer.id))
        self.assertIsNone(repo.get(customer.id))
        self.assertFalse(repo.delete(customer.id))

    def test_rejects_blank_name_invalid_email_and_duplicate_email(self):
        repo = CustomerRepository()

        with self.assertRaises(ValueError):
            repo.create("", "ana@example.com")

        with self.assertRaises(ValueError):
            repo.create("Ana Silva", "email-sem-arroba")

        repo.create("Ana Silva", "ana@example.com")
        with self.assertRaises(ValueError):
            repo.create("Ana Duplicada", "ana@example.com")

    def test_persists_customers_when_storage_path_is_used(self):
        storage_path = Path(__file__).parent / "customers_test.json"
        if storage_path.exists():
            storage_path.unlink()

        try:
            repo = CustomerRepository(storage_path=storage_path)
            customer = repo.create("Ana Silva", "ana@example.com")

            reloaded_repo = CustomerRepository(storage_path=storage_path)

            self.assertEqual(customer, reloaded_repo.get(customer.id))
        finally:
            storage_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
