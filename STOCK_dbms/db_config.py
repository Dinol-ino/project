import mysql.connector

def get_db_connection():
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='D!nol!no77',
            database='stock_portfolio'
        )
        return conn