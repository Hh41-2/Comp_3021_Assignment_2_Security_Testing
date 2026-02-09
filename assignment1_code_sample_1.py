import os
import pymysql
from urllib.request import urlopen
from dotenv import load_dotenv
import subprocess
from urllib.parse import urlparse
import urllib.request
import urllib.error

load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def get_user_input():
    user_input = input('Enter your name: ')
    return user_input

def send_email(to, subject, body):
    subprocess.run(
        ["mail", "-s", subject, to],
        input=body,
        text=True,
        check=True,
    )

def get_data():
    url = 'https://insecure-api.com/get-data'

    if urlparse(url).scheme != "https":
        raise ValueError("Refusing to call non-HTTPS URL")
    
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Request failed: {e}") from e

def save_to_db(data):
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query, (data, "Another Value"))
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)