from flask import Flask, request, redirect, url_for, abort, render_template, session
from json import dumps
import os
from werkzeug.utils import secure_filename
import pickle

app = Flask(__name__, template_folder="templates")
# It's important to use session
app.secret_key = "$$$581489*@Abscaracha"

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

# Database
with open("database.pickle", "rb") as db:
    data_base = pickle.load(db)

def check_username(form: dict, banco: list):
    username = form["username"]
    # Search the username in banco
    for user in banco:
        if user["username"] == username:
            return True
    else:
        return False

def check_passwd(form: dict, banco: list):
    password = form["userpassword"]
    for user in banco:
        if user["password"] == password:
            return True
    else:
        return False

@app.route("/")
def index():
    username = None
    if "username" in session:
        username = session["username"]

    return render_template("index.html", username=username)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # Check the username
        valid_usernam = check_username(request.form, data_base)
        # Check the password
        valid_passwd = check_passwd(request.form, data_base)
        # Verifica as credenciais do usuário
        if valid_usernam and valid_passwd:
            session["username"] = request.form['username']
            return redirect(url_for("index"), code=302)
        else:
            abort(401)
    else:
        return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        data_base.append(dumps(request.form))
        print(data_base)

        with open("database.pickle", "wb") as db:
            pickle.dump(data_base, db)
        
        redirect(url_for("login"), code=302)

        if request.files["image"]:
            return redirect(url_for("upload"))

        return render_template("login.html")
    else:
        return render_template("register.html")


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if (request.files["image"]):
        file = request.files["image"]
        savePath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(savePath)
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)