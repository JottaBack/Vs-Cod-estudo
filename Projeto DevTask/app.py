from contextlib import contextmanager
from pathlib import Path
import sqlite3

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "devtask-chave-local"

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "devtask.db"


@contextmanager
def conectar_banco():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    try:
        with conexao:
            yield conexao
    finally:
        conexao.close()


def criar_tabela():
    with conectar_banco() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT DEFAULT '',
                concluida INTEGER NOT NULL DEFAULT 0
            )
        """)


criar_tabela()


@app.route("/")
def inicio():
    with conectar_banco() as conexao:
        tarefas = conexao.execute(
            "SELECT * FROM tarefas ORDER BY id DESC"
        ).fetchall()

    total = len(tarefas)
    concluidas = sum(tarefa["concluida"] for tarefa in tarefas)
    pendentes = total - concluidas
    progresso = round(concluidas / total * 100) if total else 0

    return render_template(
        "index.html",
        tarefas=tarefas,
        total=total,
        concluidas=concluidas,
        pendentes=pendentes,
        progresso=progresso,
    )


@app.route("/adicionar", methods=["POST"])
def adicionar():
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()

    if not titulo:
        flash("Digite um título para a tarefa.")
        return redirect(url_for("inicio"))

    if len(titulo) > 120 or len(descricao) > 500:
        flash("O título ou a descrição ultrapassou o limite.")
        return redirect(url_for("inicio"))

    with conectar_banco() as conexao:
        conexao.execute(
            "INSERT INTO tarefas (titulo, descricao) VALUES (?, ?)",
            (titulo, descricao),
        )

    flash("Tarefa adicionada!")
    return redirect(url_for("inicio"))


@app.route("/alternar/<int:tarefa_id>", methods=["POST"])
def alternar(tarefa_id):
    with conectar_banco() as conexao:
        conexao.execute(
            """
            UPDATE tarefas
            SET concluida = CASE concluida
                WHEN 0 THEN 1 ELSE 0
            END
            WHERE id = ?
            """,
            (tarefa_id,),
        )

    return redirect(url_for("inicio"))


@app.route("/excluir/<int:tarefa_id>", methods=["POST"])
def excluir(tarefa_id):
    with conectar_banco() as conexao:
        conexao.execute(
            "DELETE FROM tarefas WHERE id = ?",
            (tarefa_id,),
        )

    flash("Tarefa excluída.")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
