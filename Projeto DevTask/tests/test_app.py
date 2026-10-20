import tempfile
import unittest
from pathlib import Path

import app


class TaskRoutesTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        app.DATABASE = Path(self.temp_dir.name) / "test.db"
        app.criar_tabela()
        self.client = app.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()
        app.DATABASE = app.BASE_DIR / "devtask.db"

    def test_home_shows_empty_task_list(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Nenhuma tarefa por aqui", response.data)

    def test_add_task_and_show_it(self):
        response = self.client.post(
            "/adicionar",
            data={"titulo": "Estudar Flask", "descricao": "Criar um projeto"},
        )

        self.assertEqual(response.status_code, 302)
        page = self.client.get("/")
        self.assertIn(b"Estudar Flask", page.data)
        self.assertIn(b"Criar um projeto", page.data)

    def test_blank_title_is_rejected(self):
        response = self.client.post("/adicionar", data={"titulo": "   "})

        self.assertEqual(response.status_code, 302)
        self.assertIn(b"Digite um t", self.client.get("/").data)

    def test_task_can_be_completed_and_deleted(self):
        self.client.post("/adicionar", data={"titulo": "Tarefa de teste"})
        with app.conectar_banco() as connection:
            task_id = connection.execute(
                "SELECT id FROM tarefas"
            ).fetchone()["id"]

        toggled = self.client.post(f"/alternar/{task_id}")
        self.assertEqual(toggled.status_code, 302)
        self.assertIn(b"Conclu", self.client.get("/").data)

        deleted = self.client.post(f"/excluir/{task_id}")
        self.assertEqual(deleted.status_code, 302)
        self.assertNotIn(b"Tarefa de teste", self.client.get("/").data)


if __name__ == "__main__":
    unittest.main()
