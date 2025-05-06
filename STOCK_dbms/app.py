from flask import Flask, render_template, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from auth import auth_bp, User
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = "super_secret_key"
app.register_blueprint(auth_bp)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT user_id, name, email FROM users WHERE user_id = %s;", (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return User(result["user_id"], result["name"], result["email"])
        else:
            return None
    except Exception as e:
        print(f"Error loading user: {e}")
        conn.close()
        return None

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("index.html", username=current_user.username)

@app.route("/portfolio/<int:user_id>")
@login_required
def get_portfolio(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT p.portfolio_id, p.portfolio_name, 
                   s.symbol, s.company_name, s.current_price, 
                   h.quantity, h.avg_buy_price, 
                   (s.current_price - h.avg_buy_price) * h.quantity AS profit_loss
            FROM portfolios p
            LEFT JOIN holdings h ON p.portfolio_id = h.portfolio_id
            LEFT JOIN stocks s ON h.stock_id = s.stock_id
            WHERE p.user_id = %s;
        """, (user_id,))
        
        portfolio_data = cursor.fetchall()

        clean_data = [
            item for item in portfolio_data 
            if item['avg_buy_price'] is not None and 
               item['quantity'] is not None and 
               item['current_price'] is not None
        ]

        total_investment = sum(item['avg_buy_price'] * item['quantity'] for item in clean_data)
        total_value = sum(item['current_price'] * item['quantity'] for item in clean_data)
        total_profit_loss = total_value - total_investment

        conn.close()

        return jsonify({
            "portfolio_data": portfolio_data,
            "total_investment": total_investment,
            "total_value": total_value,
            "total_profit_loss": total_profit_loss
        })

    except Exception as e:
        print(f"Error fetching portfolio data: {e}")
        conn.close()
        return jsonify({"error": "Failed to fetch portfolio data"}), 500

@app.route("/stock_history/<int:stock_id>")
@login_required
def get_stock_history(stock_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT date, close_price
            FROM price_history
            WHERE stock_id = %s;
        """, (stock_id,))

        price_history = cursor.fetchall()
        conn.close()

        if not price_history:
            return jsonify({"error": "No price history found for this stock"}), 404
        
        return jsonify(price_history)

    except Exception as e:
        print(f"Error fetching stock history: {e}")
        conn.close()
        return jsonify({"error": "Failed to fetch stock history"}), 500

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True)
