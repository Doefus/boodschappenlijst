from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE {DATABASE_NAME} DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

def create_table(cursor):
    create_table_query = (
        "CREATE TABLE IF NOT EXISTS items ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  item VARCHAR(255) NOT NULL,"
        "  created_at DATETIME NOT NULL"
        ") ENGINE=InnoDB")
    cursor.execute(create_table_query)

def init_db():
    try:
        cnx = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD
        )
        cursor = cnx.cursor()

        try:
            cnx.database = DATABASE_NAME
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
                cnx.database = DATABASE_NAME
            else:
                print(err)
                exit(1)

        create_table(cursor)

        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print(err)
        exit(1)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    text = data.get('textInput')

    try:
        cnx = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME
        )
        cursor = cnx.cursor()
        add_item = ("INSERT INTO items (item, created_at) "
                    "VALUES (%s, %s)")
        data_item = (text, datetime.now())
        cursor.execute(add_item, data_item)
        cnx.commit()
        cursor.close()
        cnx.close()
        print(f"Received text: {text}")
        return jsonify({'message': 'Text received successfully'})
    except mysql.connector.Error as err:
        print(err)
        return jsonify({'message': 'Database error occurred'}), 500

@app.route('/items', methods=['GET'])
def get_items():
    try:
        cnx = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME
        )
        cursor = cnx.cursor()
        query = "SELECT id, item, created_at FROM items"
        cursor.execute(query)
        items = cursor.fetchall()
        cursor.close()
        cnx.close()
        return jsonify(items)
    except mysql.connector.Error as err:
        print(err)
        return jsonify({'message': 'Database error occurred'}), 500

@app.route('/delete_item', methods=['POST'])
def delete_item():
    data = request.get_json()
    item_id = data.get('item_id')

    try:
        cnx = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME
        )
        cursor = cnx.cursor()
        delete_item_query = "DELETE FROM items WHERE id = %s"
        cursor.execute(delete_item_query, (item_id,))
        cnx.commit()
        cursor.close()
        cnx.close()
        return jsonify({'message': 'Item deleted successfully'})
    except mysql.connector.Error as err:
        print(err)
        return jsonify({'message': 'Database error occurred'}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
