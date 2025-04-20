from flask import Flask, render_template, request, jsonify
from db_config import get_db_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/portfolio/<int:user_id>')
def get_portfolio(user_id):
    print(f"Received User ID: {user_id}")

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                p.portfolio_name,
                s.symbol,
                h.quantity,
                h.avg_buy_price,
                s.current_price,
                (s.current_price - h.avg_buy_price) * h.quantity AS profit_loss
            FROM Holdings h
            JOIN Stocks s ON h.stock_id = s.stock_id
            JOIN Portfolios p ON h.portfolio_id = p.portfolio_id
            WHERE p.user_id = %s;
        """, (user_id,))
        results = cursor.fetchall()
        print(f"Query Results: {results}")
        conn.close()
        return jsonify(results)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
