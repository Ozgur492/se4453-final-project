import os
import psycopg2
from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello():
    db_host     = os.environ.get("DB_HOST")
    db_user     = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_name     = os.environ.get("DB_NAME")

    try:
        conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            dbname=db_name,
            sslmode="require"
        )
        conn.close()
        return "Hello! Database connection successful.", 200
    except Exception as e:
        return f"Connection failed: {str(e)}", 500

if __name__ == '__main__':
    app.run()
