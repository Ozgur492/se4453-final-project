import os
import psycopg2
from flask import Flask
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

KEY_VAULT_URL = "https://midterm-kv-group9.vault.azure.net/"
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

@app.route('/hello')
def hello():
    try:
        db_host     = secret_client.get_secret("DB-HOST").value
        db_user     = secret_client.get_secret("DB-USER").value
        db_password = secret_client.get_secret("DB-PASSWORD").value
        db_name     = secret_client.get_secret("DB-NAME").value

        conn = psycopg2.connect(
            host=db_host, user=db_user, password=db_password,
            dbname=db_name, sslmode="require"
        )
        conn.close()
        return "Hello! Database connection successful.", 200
    except Exception as e:
        return f"Connection failed: {str(e)}", 500

if __name__ == '__main__':
    app.run()
