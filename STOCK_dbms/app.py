from flask import Flask, render_template, jsonify
from flask_login import LoginManager, login_required, current_user
from auth import auth_bp, User
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = "super_secret_key"
app.register_blueprint(auth_bp)  # ✅ Register authentication Blueprint

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, password FROM user WHERE id = %s;", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return User(result["id"], result["username"], result["password"]) if result else None

@app.route("/")
def index():
    return render_template("login.html")  # ✅ Default page redirects to login

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("index.html", username=current_user.username)  # ✅ Now serves portfolio dashboard

@app.route("/portfolio/<int:user_id>")
@login_required
def get_portfolio(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM portfolios WHERE user_id = %s;", (user_id,))
    portfolio = cursor.fetchall()
    conn.close()
    
    return jsonify(portfolio) if portfolio else jsonify([])  # ✅ Returns JSON portfolio data

if __name__ == "__main__":
    app.run(debug=True)