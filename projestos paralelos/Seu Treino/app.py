from flask import Flask, redirect, render_template, url_for

app = Flask(__name__, static_folder="css", static_url_path="/css")


@app.route("/")
def inicio():
    return redirect(url_for("focofit"))


@app.route("/focofit")
def focofit():
    return render_template("index.html")


@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


@app.route("/entrar", methods=["POST"])
def entrar():
    return redirect(url_for("pagina_inicial"))


@app.route("/pagina-inicial")
def pagina_inicial():
    return render_template("pagina_inicial.html")


@app.route("/calendario")
def calendario():
    return render_template("calendario.html")


@app.route("/perfil")
def perfil():
    return render_template("perfil.html")


@app.route("/pagamento")
def pagamento():
    return render_template("pagamento.html")


@app.route("/pagina-em-branco")
def pagina_em_branco():
    return redirect(url_for("pagina_inicial"), code=301)


if __name__ == "__main__":
    app.run(debug=True)
