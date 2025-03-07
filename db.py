from flask import Flask, g
import sqlite3
import os

app = Flask(__name__)
DATABASE = os.path.join(os.getcwd(), "database.db")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    print("creating a new db")
    if not os.path.exists("database.db"):
        with open("database.db", 'w') as file:
            pass 
    else:
        print(f"The file \"database.db\" already exists.")
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS 'Menu' (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price FLOAT NOT NULL,
                    review FLOAT DEFAULT 0.0,
                    no_of_reviews INTEGER DEFAULT 0
                )
            ''')
        except Exception as e:
            print(f"Error creating Menu table: {e}")
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS 'Staff' (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    staff_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    mobile_number TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    dob DATE NOT NULL,
                    admin INTEGER DEFAULT 0,
                    role TEXT NOT NULL
                )
            ''')
        except Exception as e:
            print(f"Error creating Staff table: {e}")
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS 'Cart' (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    price FLOAT NOT NULL,
                    session_id INTEGER NOT NULL,
                    FOREIGN KEY (item) REFERENCES Menu (id)
                )
            ''')
        except Exception as e:
            print(f"Error creating Cart table: {e}")
        db.commit()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS `Order` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    total_price FLOAT NOT NULL,
                    table_no INTEGER NOT NULL,
                    date DATE,
                    time TIME
                )
            ''')

            print("Order table created successfully.")
        except Exception as e:
            print(f"Error creating Order table: {e}")
        db.commit()

def get_menu_data_from_db():
    db = get_db()  
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Menu") 
    data = cursor.fetchall()  
    return data

def get_categories_from_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT category FROM Menu")
    categories = cursor.fetchall()
    return [row['category'] for row in categories]

def get_dishes_for_category(category_name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Menu WHERE category = ?", (category_name,))
    dishes = cursor.fetchall()
    return dishes

def get_price_from_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT item_name, price FROM Menu")
    prices = cursor.fetchall()
    return {row['item_name']: row['price'] for row in prices}
