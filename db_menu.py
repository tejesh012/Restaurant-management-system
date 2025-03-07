import sqlite3

DATABASE = 'database.db'
menu_data = [
    {'id': '1', 'name': 'Chicken Biryani', 'price': '250', 'category': 'Biryani'},
    {'id': '2', 'name': 'Mutton Biryani', 'price': '400', 'category': 'Biryani'},
    {'id': '3', 'name': 'Egg Biryani', 'price': '80', 'category': 'Biryani'},
    {'id': '4', 'name': 'Tandoori Chicken Biryani', 'price': '300', 'category': 'Biryani'},
    {'id': '5', 'name': 'Prawn Biryani', 'price': '250', 'category': 'Biryani'},
    
    {'id': '6', 'name': 'Paneer Tikka', 'price': '150', 'category': 'Starters'},
    {'id': '7', 'name': 'Veg Pakora', 'price': '120', 'category': 'Starters'},
    
    {'id': '8', 'name': 'Butter Chicken', 'price': '350', 'category': 'Curries'},
    {'id': '9', 'name': 'Dal Makhani', 'price': '180', 'category': 'Curries'},
    
    {'id': '10', 'name': 'Gulab Jamun', 'price': '100', 'category': 'Desserts'},
    {'id': '11', 'name': 'Ras Malai', 'price': '120', 'category': 'Desserts'},
    
    {'id': '13', 'name': 'Maaza', 'price': '60', 'category': 'Drinks'},
    {'id': '14', 'name': 'Pepsi', 'price': '60', 'category': 'Drinks'}
]
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Menu (
        id INTEGER PRIMARY KEY,
        item_name TEXT NOT NULL,
        price TEXT NOT NULL,
        category TEXT NOT NULL
    )
''')
for item in menu_data:
    cursor.execute('''
        INSERT INTO Menu (id, item_name, price, category)
        VALUES (?, ?, ?, ?)
    ''', (item['id'], item['name'], item['price'], item['category']))
conn.commit()
conn.close()
print("Menu data inserted successfully!")
