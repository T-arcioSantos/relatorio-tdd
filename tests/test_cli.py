from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import unittest

from customer_crud.cli import main


class CustomerCliTest(unittest.TestCase):
    def setUp(self):
        self.storage_path = Path(__file__).parent / "customers_cli_test.json"
        self.storage_path.unlink(missing_ok=True)

    def tearDown(self):
        self.storage_path.unlink(missing_ok=True)

    def test_add_and_list_customer_using_json_storage(self):
        add_output = StringIO()
        with redirect_stdout(add_output):
            add_exit_code = main(
                [
                    "--db",
                    str(self.storage_path),
                    "add",
                    "--name",
                    "Ana Silva",
                    "--email",
                    "ana@example.com",
                    "--phone",
                    "71999990000",
                ]
            )

        list_output = StringIO()
        with redirect_stdout(list_output):
            list_exit_code = main(["--db", str(self.storage_path), "list"])

        self.assertEqual(0, add_exit_code)
        self.assertEqual(0, list_exit_code)
        self.assertIn("Cliente 1 cadastrado", add_output.getvalue())
        self.assertIn("Ana Silva", list_output.getvalue())
        self.assertIn("ana@example.com", list_output.getvalue())


if __name__ == "__main__":
    unittest.main()
