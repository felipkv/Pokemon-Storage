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
            return render_template("listar_pkm.html", ja_cadastrado = "ja_cadastrado", listagem = listar)
        
    cadastrar = Pokemon(nome = nome, tipo = tipo)
    db.session.add(cadastrar)
    db.session.commit()
    return redirect("/")
    
@app.route("/buscar", methods=["POST"])
def buscar_pkm():   
    nome = request.form['nome']
    #buscar = Pokemon.query.filter(Pokemon.nome == nome).first()
    buscar = Pokemon.query.filter_by(nome=nome).first()
    if not buscar:
        listar = Pokemon.query.all()
        return render_template("listar_pkm.html", not_found = "not_found", listagem = listar)
    
    return render_template("buscar_pkm.html", buscar = buscar)

@app.route("/editar", methods=["POST"])
def editar_pkm():
    if request.form['_method'] == 'PUT':
        old_nome = request.form['old_nome']
        nome = request.form['nome']
        tipo = request.form['tipo']
        buscar = Pokemon.query.filter_by(nome=old_nome).first()
        buscar.nome = nome
        buscar.tipo = tipo

        db.session.commit()

        return redirect("/")
    
@app.route("/deletar", methods=["POST"])
def deletar_pkm():
    nome = request.form['nome']
    buscar = Pokemon.query.filter_by(nome=nome).first() ## para poder mexer no banco é necessário sempre uma instância da entrada que você quer, e não a string direto vindo do form. Por isso a query
    
    db.session.delete(buscar)
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(host = "localhost", debug = True)