import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage_pkm.db'
db = SQLAlchemy(app)


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    tipo = db.Column(db.String(80), nullable=False)

    def __init__(self,nome,tipo):
        self.nome = nome
        self.tipo = tipo

with app.app_context():
    db.create_all()

#lista = [{"id": 1, "nome": "Articuno", "tipo": "Voador/Gelo"},
#         {"id": 2, "nome": "Zapdos", "tipo": "Voador/Elétrico"},
#         {"id": 3, "nome": "Moltres", "tipo": "Voador/Fogo"}]


@app.route("/")
def start():
    listar = Pokemon.query.all()
    return render_template("listar_pkm.html", listagem = listar)


@app.route("/cadastro")
def abrir_form():
    return render_template("cadastro_pkm.html")

@app.route("/", methods=["POST"])
def inserir_pkm():
    listar = Pokemon.query.all()
    nome = request.form['nome']
    tipo = request.form['tipo']
    for pkm in listar:
        if nome == pkm.nome:
            return render_template("listar_pkm.html", ja_cadastrado = "0", listagem = listar)
        
    cadastrar = Pokemon(nome = nome, tipo = tipo)
    db.session.add(cadastrar)
    db.session.commit()
    return redirect("/")
    
    

if __name__ == "__main__":
    app.run(host = "localhost", debug = True)