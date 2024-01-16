from flask import Flask, request, redirect, url_for, abort, render_template, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usuario.sqlite3"

db = SQLAlchemy(app)

# It's important to use session
app.secret_key = "$$$581489*@Abscaracha"


class Usuarios(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column("nome", db.String(150))
    sobrenome = db.Column("sobrenome", db.String(150))
    email = db.Column("email", db.String(150))
    senha = db.Column("senha", db.String(150))
    dataDeAniversario = db.Column("data_de_aniversario", db.Date)
    genero = db.Column("genero", db.String(30))

    def __init__(self, nome, sobrenome, email, senha, dataDeAniversario, genero):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha
        self.dataDeAniversario = dataDeAniversario
        self.genero = genero


def check_email_exists(email: dict, banco):
    query = Usuarios.query.where(Usuarios.email == email)
    return bool(query.count())


def check_passwd_exists(password, banco):
    query = Usuarios.query.where(Usuarios.senha == password)
    return bool(query.count())


# Decorator to import libs in HTML code
@app.template_filter()
def import_lib(lib_name):
  return __import__(lib_name)

@app.route("/")
def index():
    username = None
    if "username" in session:
        username = session["username"]
    return render_template("index.html", username=username)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # Check the email
        valid_email= check_email_exists(request.form["useremail"], Usuarios)
        # Check the password
        valid_passwd = check_passwd_exists(request.form["userpassword"], Usuarios)
        # Verifica as credenciais do usuário
        if valid_email and valid_passwd:
            # Query to search username using email
            query = Usuarios.query.where(Usuarios.email == request.form['useremail'])
            username = query.first().nome
            session["username"] = username
            return redirect(url_for("index"), code=302)
        else:
            abort(401)
    else:
        return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        usuario = Usuarios(
            request.form["username"],
            request.form["userlastname"],
            request.form["useremail"],
            request.form["userpassword"],
            datetime.strptime(request.form["userbirthday"], "%Y-%m-%d"),
            request.form["usergender"],
            )
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for("login"))
    else:
        return render_template("register.html")


@app.route("/table")
def table():
    usuarios = Usuarios.query.all()
    return render_template("table.html", usuarios=usuarios, datetime = import_lib("datetime"))

@app.route("/delete/<useremail>")
def delete(useremail):
    usuario = Usuarios.query.where(Usuarios.email == useremail).first()
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for("table"))

@app.route("/edit/<useremail>", methods=["POST", "GET"])
def edit(useremail):
    usuario = Usuarios.query.where(Usuarios.email == useremail).first()
    if request.method == "POST":
        usuario.nome = request.form["username"]
        usuario.sobrenome = request.form["userlastname"]
        usuario.email = request.form["useremail"]
        usuario.senha = request.form["userpassword"]
        usuario.aniversario = request.form["userbirthday"]
        usuario.genero = request.form["usergender"]
        db.session.commit()
        return redirect(url_for("table"))
    return render_template("edit.html", usuario=usuario, datetime=import_lib("datetime"))

@app.route("/logout")
def logout():
    # Remove the username from the session
    session.pop("username", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)