from flask import Flask, request, redirect, url_for, render_template
import mysql.connector
from db_config import get_db_connection

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Fetch user first (without checking password in SQL)
    cursor.execute("SELECT * FROM user WHERE username = %s;", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and user["password"] == password:  # ✅ Compare password securely in Python
        return redirect(url_for("dashboard"))
    else:
        return "❌ Login failed! Check your username and password."

@app.route("/dashboard")
def dashboard():
    return "✅ Welcome to your dashboard!"

if __name__ == "__main__":
    app.run(debug=True)