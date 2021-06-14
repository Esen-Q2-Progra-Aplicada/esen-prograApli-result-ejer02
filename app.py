from flask import Flask, render_template, request, redirect, session
from logic.person_logic import PersonLogic
from logic.user_logic import UserLogic
import requests
import bcrypt

app = Flask(__name__)
app.secret_key = "Balthis1_is2_my3_secret4_key23!+"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    data = {}
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        """validaciones de recaptha y base de datos"""
        data["secret"] = "6LeAdQcbAAAAAGNn732kkStupieUDdKjQTl38KL_"
        data["response"] = request.form["g-recaptcha-response"]
        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify", params=data
        )
        if response.status_code == 200:
            messageJson = response.json()
            if messageJson["success"]:
                """si el recaptcha es valido -  success"""

                """ validacion del codigo de base de datos """
                logic = UserLogic()
                userEmail = request.form["email"]
                passwd = request.form["passwd"]
                userDict = logic.getUserByEmail(userEmail)
                salt = userDict["salt"].encode("utf-8")
                hashPasswd = bcrypt.hashpw(passwd.encode("utf-8"), salt)
                dbPasswd = userDict["password"].encode("utf-8")
                if hashPasswd == dbPasswd:
                    """si pasa esta validacion entonces todos nuestros saltos de seguridad estan bien"""

                    """ crear la sesion """
                    session["login_user"] = userEmail
                    session["loggedIn"] = True
                    return redirect("person")
                else:
                    return redirect("login")
            else:
                return redirect("login")
        else:
            return redirect("login")
    return redirect("login")


@app.route("/person")
def person():
    logic = PersonLogic()
    loggedUser = session["login_user"]
    personArray = logic.getAllPersons()
    return render_template("person.html", persons=personArray, loggedUser=loggedUser)


if __name__ == "__main__":
    app.run(debug=True)
