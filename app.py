from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
users = {
    "admin": "pass",
    "user2": "password2",
    "user3": "password3"
}

messages = []

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("chat"))
    return render_template("login.html")

@app.route("/chat", methods=["GET", "POST"])
@login_required

def chat():
    if request.method == "POST":
        message = request.form["message"]
        messages.append(f"{session['username']}: {message}")
    is_admin = session['username'] == 'admin'
    return render_template("chat.html", messages=messages, is_admin=is_admin)

@app.route("/send", methods=["POST"])
@login_required
def send():
    if request.method == "POST":
        message = request.form["message"]
        messages.append(f"{session['username']}: {message}")
    return redirect(url_for("chat"))

@app.route("/delete/<int:message_index>", methods=["POST"])
@login_required
def delete_message(message_index):
    if session['username'] == 'admin':
        if 0 <= message_index < len(messages):
            messages.pop(message_index)
    return redirect(url_for("chat"))

@app.route("/delete_all", methods=["POST"])
@login_required
def delete_all():
    if session['username'] == 'admin':
        messages.clear()
    return redirect(url_for("chat"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
