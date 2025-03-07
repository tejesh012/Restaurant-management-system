import sqlite3

DATABASE = 'database.db'
staff_data = [
    {'staff_id': 'S1', 'name': 'Koushik', 'age': 25, 'mobile_number': '1234567890', 'email': 'Staff@gmail.com', 'password': 'admin', 'dob': '1999-12-12', 'admin': 1, 'role': 'Admin'},
    {'staff_id': 'S2', 'name': 'ABC', 'age': 21, 'mobile_number': '0321654987', 'email': 'Staff2@gmail.com', 'password': 'admin', 'dob': '2003-05-12', 'admin': 0, 'role': 'Staff'},
    {'staff_id': 'S3', 'name': 'XYZ', 'age': 21, 'mobile_number': '9876543210', 'email': 'Staff3@gmail.com', 'password': 'admin', 'dob': '2003-06-15', 'admin': 0, 'role': 'Staff'},
    {'staff_id': 'S4', 'name': 'Staff_1', 'age': 21, 'mobile_number': '1212121232', 'email': 'Staff4@gmail.com', 'password': 'admin', 'dob': '2003-01-01', 'admin': 0, 'role': 'Staff'}
]
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Staff (
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
for staff in staff_data:
    cursor.execute('''
        INSERT INTO Staff (staff_id, name, age, mobile_number, email, password, dob, admin, role)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (staff['staff_id'], staff['name'], staff['age'], staff['mobile_number'], staff['email'], staff['password'], staff['dob'], staff['admin'], staff['role']))
conn.commit()
conn.close()

print("Staff data inserted successfully!")
