from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import UserMixin, login_user, logout_user
import mysql.connector
from db_config import get_db_connection

auth_bp = Blueprint("auth", __name__)

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id  # ✅ Matches `id` column in `user` table
        self.username = username
        self.password = password

    @staticmethod
    def get_user_by_username(username):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, password FROM user WHERE username = %s;", (username,))
        result = cursor.fetchone()
        conn.close()
        return User(result["id"], result["username"], result["password"]) if result else None

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.get_user_by_username(username)

        if user and user.password == password:
            login_user(user)
            return redirect(url_for("dashboard"))  # ✅ Redirects to dashboard
        else:
            return "❌ Login failed! Check your username and password."

    return render_template("login.html")