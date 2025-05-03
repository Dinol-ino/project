from flask import Flask, request, redirect, url_for, render_template
import mysql.connector
from db_config import get_db_connection

app = Flask(__name__)

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return redirect(url_for("auth.login"))
    except mysql.connector.IntegrityError:
        return "❌ Username already exists!"
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)