from db import init_db, get_menu_data_from_db, get_categories_from_db, get_dishes_for_category, get_db, get_price_from_db
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string
from uuid import uuid4
import secrets
from datetime import datetime

app = Flask(__name__)
init_db()
app.secret_key = secrets.token_hex(24)
menu_db = get_menu_data_from_db

@app.before_request
def ensure_session():
    if 'session_id' not in session:
        session['session_id'] = str(uuid4())

STAFF_EMAIL = "staff@gmail.com"
STAFF_PASSWORD = "Staff@123"
cart_data = [
    {'dish_name': 'Chicken Biryani', 'price': 200, 'quantity': 2},
    {'dish_name': 'Samosa', 'price': 50, 'quantity': 4}
]
staff_data = []
menu_data = {
    'Biryani': [
        {'id': '1', 'name': 'Chicken Biryani', 'price': '₹250'},
        {'id': '2', 'name': 'Mutton Biryani', 'price': '₹400'},
        {'id': '3', 'name': 'Egg Biryani', 'price': '₹180'},
        {'id': '4', 'name': 'Tandoori Chicken Biryani', 'price': '₹300'},
        {'id': '5', 'name': 'Prawn Biryani', 'price': '₹250'}
    ],
    'Starters': [
        {'id': '6', 'name': 'Paneer Tikka', 'price': '₹150'},
        {'id': '7', 'name': 'Veg Pakora', 'price': '₹120'}
    ],
    'Curries': [
        {'id': '8', 'name': 'Butter Chicken', 'price': '₹350'},
        {'id': '9', 'name': 'Dal Makhani', 'price': '₹180'}
    ],
    'Desserts': [
        {'id': '10', 'name': 'Gulab Jamun', 'price': '₹100'},
        {'id': '11', 'name': 'Ras Malai', 'price': '₹120'},
        {'id': '12', 'name': 'Thums Up', 'price': '₹60'},
        {'id': '13', 'name': 'Maaza', 'price': '₹60'},
        {'id': '14', 'name': 'Pepsi', 'price': '₹60'}
    ]
}

@app.route("/staff-login", methods=["GET", "POST"])
def staff_login():
    error_message = ""
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            SELECT id, name, email, password
            FROM Staff
            WHERE email = ?
        ''', (email,))
        staff = cursor.fetchone()
        if staff and staff['password'] == password:
            return redirect(url_for('staff_dashboard', pk=staff['id']))
        else:
            error_message = "Incorrect credentials!"
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Staff Login</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                text-align: center;
            }}
            header {{
                background-color: #4CAF50;
                color: white;
                padding: 20px 0;
            }}
            header img {{
                vertical-align: middle;
                width: 50px;
                margin-right: 10px;
            }}
            header span {{
                font-size: 24px;
                font-weight: bold;
            }}
            .login-container {{
                margin-top: 100px;
                background-color: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                width: 300px;
                margin-left: auto;
                margin-right: auto;
            }}
            .login-container input {{
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 16px;
            }}
            .login-container button {{
                width: 100%;
                padding: 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 18px;
                cursor: pointer;
            }}
            .login-container button:hover {{
                background-color: #45a049;
            }}
            .error-message {{
                color: red;
                font-size: 14px;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <header>
            <img src="/static/img/logo.png" alt="Hotel Logo">
            <span>Hotel Name</span>
        </header>
        <div class="login-container">
            <h2>Staff Login</h2>
            <form method="post">
                <input type="text" name="email" placeholder="Enter Email" required><br>
                <input type="password" name="password" placeholder="Enter Password" required><br>
                <button type="submit">Login</button>
                <button style="margin: 10px; padding: 10px 20px; background-color: #28a745; border: none; color: white;" onclick="window.location.href='/'">Exit</button>
            </form>
            <p class="error-message">{error_message}</p>
        </div>
    </body>
    </html>
    '''

@app.route("/staff-dashboard/<int:pk>", methods=["GET", "POST"])
def staff_dashboard(pk):
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'Delete Dish':
            category = request.form['category']
            dish_id = request.form['id']
            cursor.execute('''
                DELETE FROM Menu
                WHERE id = ? AND category = ?
            ''', (dish_id, category))
            db.commit()
        elif action == 'Edit Dish':
            category = request.form['category']
            dish_id = request.form['id']
            new_name = request.form['new_name']
            new_price = request.form['new_price']
            cursor.execute('''
                UPDATE Menu
                SET item_name = ?, price = ?
                WHERE id = ? AND category = ?
            ''', (new_name, new_price, dish_id, category))
            db.commit()
        elif action == 'Delete Staff':
            staff_id = request.form['staff_id']
            cursor.execute('''
                DELETE FROM Staff
                WHERE id = ?
            ''', (staff_id,))
            db.commit()
        elif action == 'Edit Profile':
            id = pk 
            new_name = request.form['staff_name']
            new_age = request.form['staff_age']
            new_mobile = request.form['staff_mobile']
            new_email = request.form['staff_email']
            new_pass = request.form['staff_pass']
            new_dob = request.form['staff_dob']
            new_admin = request.form['staff_admin']
            new_role = request.form['staff_role']
            cursor.execute('''
                UPDATE Staff
                SET name = ?, age = ?, mobile_number = ?, email = ?, password = ?, dob = ?, admin = ?, role = ?
                WHERE id = ?
            ''', (new_name, new_age, new_mobile, new_email, new_pass, new_dob, new_admin, new_role, id))
            db.commit()
        elif action == 'Add Dish':
            category = request.form['category']
            dish_name = request.form['dish_name']
            dish_price = request.form['dish_price']
            cursor.execute('''
                INSERT INTO Menu (category, item_name, price)
                VALUES (?, ?, ?)
            ''', (category, dish_name, dish_price))
            db.commit()
        elif action == 'Add Staff':
            staff_id = request.form['staff_id']
            staff_name = request.form['staff_name']
            staff_age = request.form['staff_age']
            staff_mobile = request.form['staff_mobile']
            staff_email = request.form['staff_email']
            staff_pass = request.form['staff_pass']
            staff_dob = request.form['staff_dob']
            staff_admin = request.form['staff_admin']
            staff_role = request.form['staff_role']
            cursor.execute('''
                INSERT INTO Staff (staff_id, name, age, mobile_number, email, password, dob, admin, role)
                VALUES (?, ?, ?, ?, ? , ? , ? , ? , ? )
            ''', (staff_id, staff_name, staff_age, staff_mobile, staff_email, staff_pass, staff_dob, staff_admin, staff_role))
            db.commit()
    cursor.execute('''
        SELECT id, name, role, age, admin
        FROM Staff
        WHERE id = ?
    ''', (pk,))
    staff_member = cursor.fetchone()
    cursor.execute('''
        SELECT id, name, role, age, admin, mobile_number, staff_id, email, password, dob 
        FROM Staff
        WHERE id = ?
    ''', (pk,))
    staff_member_pk = cursor.fetchone()
    if not staff_member:
        return redirect('/staff-login')
    menu_data = {}
    cursor.execute('SELECT * FROM Menu')
    dishes = cursor.fetchall()
    for dish in dishes:
        if dish['category'] not in menu_data:
            menu_data[dish['category']] = []
        menu_data[dish['category']].append(dish)
    menu_html = ""
    for category, items in menu_data.items():
        menu_html += f"<h3>{category}</h3>"
        menu_html += """
        <table border="1" style="width:100%; margin: 10px 0;">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Rating</th>
                <th>Price</th>
                <th>Actions</th>
            </tr>
        """
        for dish in items:
            avg_review = dish['review']/dish['no_of_reviews']
            stars = "★" * int(round(avg_review)) + "☆" * (5 - int(round(avg_review)))
            menu_html += f"""
            <tr>
                <td>{dish['id']}</td>
                <td>{dish['item_name']}</td>
                <td>{stars} {avg_review}</td>
                <td>{dish['price']}</td>
                <td>
                    <form action="/staff-dashboard/{pk}" method="POST" style="display:inline;">
                        <input type="hidden" name="category" value="{category}">
                        <input type="hidden" name="id" value="{dish['id']}">
                        <input type="submit" name="action" value="Delete Dish">
                    </form>
                    <form action="/staff-dashboard/{pk}" method="POST" style="display:inline;">
                        <input type="hidden" name="category" value="{category}">
                        <input type="hidden" name="id" value="{dish['id']}">
                        <input type="text" name="new_name" placeholder="New Name" required>
                        <input type="text" name="new_price" placeholder="New Price" required>
                        <input type="submit" name="action" value="Edit Dish">
                    </form>
                </td>
            </tr>
            """
        menu_html += "</table>"
    menu_html += f"""
        <br>
        <br>
        <h2>Add a new item to Menu</h2>
        <form action="/staff-dashboard/{pk}" method="POST" style="display:inline;">
        <label for="category">Choose a Category:</label>
            <select id="category" name="category">
    """
    for category, items in menu_data.items():
        
        menu_html += f"""
                <option value="{category}">{category}</option>
        """
    menu_html += f"""
            </select>
            <br>
            <br>
            <label for="dish_name">Dish Name:</label><br>
            <input type="text" id="staff_id" name="dish_name" required><br>
            <br>
            <label for="dish_price">Price:</label><br>
            <input type="number" id="dish_price" name="dish_price" required><br>
            <br>
            <br>
            <input type="submit" name="action" value="Add Dish">
        </form>
    """
    profile_html = f"""
        <h3>Staff Profile</h3>
        <p><strong>Name:</strong> {staff_member_pk['name']}</p>
        <p><strong>Role:</strong> {staff_member_pk['role']}</p>
        <p><strong>Age:</strong> {staff_member_pk['age']}</p>
        <p><strong>Mobile Number:</strong> {staff_member_pk['mobile_number']}</p>
        <p><strong>Date of Birth:</strong> {staff_member_pk['dob']}</p>
        <br>
        <hr>
        <br>
        """
    profile_html_edit = f"""
        <h3>Edit Profile</h3>
        <form action="/staff-dashboard/{pk}" method="POST">
            <input type="hidden" name="id" value="{staff_member_pk['id']}">
            <label for="staff_name">Name:</label><br>
            <input type="text" id="staff_name" name="staff_name" value="{staff_member_pk['name']}" required><br>
            
            <label for="staff_age">Age:</label><br>
            <input type="number" id="staff_age" name="staff_age" value="{staff_member_pk['age']}" required><br>
            
            <label for="staff_mobile">Mobile:</label><br>
            <input type="text" id="staff_mobile" name="staff_mobile" value="{staff_member_pk['mobile_number']}" required><br>
            
            <label for="staff_email">Email:</label><br>
            <input type="email" id="staff_email" name="staff_email" value="{staff_member_pk['email']}" required><br>
            
            <label for="staff_pass">Password:</label><br>
            <input type="password" id="staff_pass" name="staff_pass" value="{staff_member_pk['password']}" required><br>
            
            <label for="staff_dob">Date of Birth:</label><br>
            <input type="date" id="staff_dob" name="staff_dob" value="{staff_member_pk['dob']}" required><br>
            
            <label for="staff_admin">Admin:</label><br>
            <input type="number" id="staff_admin" name="staff_admin" value="{staff_member_pk['admin']}" min="0" max="1" required><br>
            
            <label for="staff_role">Role:</label><br>
            <input type="text" id="staff_role" name="staff_role" value="{staff_member_pk['role']}" required><br>
            
            <input type="submit" name="action" value="Edit Profile">
        </form>
        """
    if staff_member and staff_member['admin'] == 1: 
        staff_admin_page = f"""
            <button onclick="toggleSection('staff-section')">Staff</button>
        """
    else:
        staff_admin_page = "" 
    staff_html = f"""
        <h3>Staff Members</h3>
        <table border="1" style="width:100%; margin: 10px 0;">
            <tr>
                <th>Staff ID</th>
                <th>Name</th>
                <th>Role</th>
                <th>Age</th>
                <th>Actions</th>
            </tr>
        """
    cursor.execute('SELECT id, name, role, age FROM Staff')
    staff_data = cursor.fetchall()
    for staff in staff_data:
        staff_html += f"""
        <tr>
            <td>{staff['id']}</td>
            <td>{staff['name']}</td>
            <td>{staff['role']}</td>
            <td>{staff['age']}</td>
            <td>
                <form action="/staff-dashboard/{pk}" method="POST" style="display:inline;">
                    <input type="hidden" name="staff_id" value="{staff['id']}">
                    <input type="submit" name="action" value="Delete Staff">
                </form>
            </td>
        </tr>
        """
    staff_html += "</table>"
    cursor.execute('''
        SELECT 
            o.id AS order_id,  -- Fetch order_id
            o.date, o.time, o.session_id, o.table_no,
            m.item_name AS item_name, c.quantity, m.price AS item_price, 
            (c.quantity * m.price) AS item_total_price, 
            o.total_price AS order_total_price
        FROM `Order` o
        JOIN `Cart` c ON o.session_id = c.session_id
        JOIN `Menu` m ON c.item = m.id
        ORDER BY o.date DESC, o.time DESC
    ''')
    orders = cursor.fetchall()
    orders_by_session = {}
    for order in orders:
        session_id = order[3]  
        table_no = order[4] 
        if (session_id, table_no) not in orders_by_session:
            orders_by_session[(session_id, table_no)] = []
        orders_by_session[(session_id, table_no)].append(order)
    order_html = """
        <h1>Order History</h1>
    """
    for (session_id, table_no), grouped_orders in orders_by_session.items():
        order_id = grouped_orders[0][0] 
        order_total_price = grouped_orders[0][9] 
        order_date = grouped_orders[0][1]  
        order_time = grouped_orders[0][2]
        order_html += f"""
        <p><strong>Time: {order_time}, Date: {order_date}, Table No: {table_no}</strong></p>
        <p>Total Order Price: ₹{order_total_price:.2f}</p>
        <form action="/bill/{pk}/{order_id}" method="get" style="display: inline;">
            <button type="submit" style="margin: 5px; padding: 8px 16px; background-color: #007bff; border: none; color: white; cursor: pointer;">
                Show Bill Now
            </button>
        </form>
        <table border="1" style="width: 100%; margin-top: 10px;">
            <tr>
                <th>Item Name</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Total Price</th>
            </tr>
        """
        for order in grouped_orders:
            order_html += f"""
                <tr>
                    <td>{order[5]}</td> <!-- item_name -->
                    <td>{order[6]}</td> <!-- quantity -->
                    <td>{order[7]:.2f}</td> <!-- price -->
                    <td>{order[8]:.2f}</td> <!-- item_total_price -->
                </tr>
            """
        order_html += "</table><hr><br>"
    staff_html += f"""
    <h3>Add a New Staff Member</h3>
    <form action="/staff-dashboard/{pk}" method="POST">
        <label for="staff_id">Staff ID:</label><br>
        <input type="text" id="staff_id" name="staff_id" required><br>
        <label for="staff_name">Name:</label><br>
        <input type="text" id="staff_name" name="staff_name" required><br>
        <label for="staff_age">Age:</label><br>
        <input type="text" id="staff_role" name="staff_age" required><br>
        <label for="staff_mobile">Mobile:</label><br>
        <input type="text" id="staff_role" name="staff_mobile" required><br>
        <label for="staff_email">Email:</label><br>
        <input type="text" id="staff_role" name="staff_email" required><br>
        <label for="staff_pass">Password:</label><br>
        <input type="text" id="staff_role" name="staff_pass" required><br>
        <label for="staff_dob">DoB:</label><br>
        <input type="text" id="staff_role" name="staff_dob" placeholder="YYYY-MM-DD" required><br>
        <label for="staff_admin">admin:</label><br>
        <input type="text" id="staff_role" name="staff_admin" required><br>
        <label for="staff_role">Role:</label><br>
        <input type="text" id="staff_role" name="staff_role" required><br>
        <input type="submit" name="action" value="Add Staff">
    </form>
    """
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Staff Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            header {{
                background-color: #4CAF50;
                color: white;
                padding: 20px 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 50px;
            }}
            header img {{
                vertical-align: middle;
                width: 50px;
                margin-right: 10px;
            }}
            header span {{
                font-size: 24px;
                font-weight: bold;
            }}
            .buttons-container {{
                display: flex;
                justify-content: flex-end;
                padding: 20px;
            }}
            .buttons-container button {{
                padding: 10px 20px;
                font-size: 16px;
                margin-left: 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            .buttons-container button:hover {{
                background-color: #45a049;
            }}
            .section {{
                display: none;
                background-color: white;
                padding: 20px;
                margin: 20px auto;
                width: 50%;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
            }}
            .section.active {{
                display: block;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }}
            th {{
                background-color: #4CAF50;
                color: white;
            }}
        </style>
    </head>
    <body>
        <header>
            <img src="/static/img/logo.png" alt="Hotel Logo">
            <span>Hotel Name</span>
            <div class="buttons-container">
                <button onclick="toggleSection('menu-section')">Menu</button>
                {staff_admin_page}
                <button onclick="toggleSection('order-section')">Order</button>
                <button onclick="toggleSection('profile-section')">Profile</button>
                <button onclick="location.href='/staff-login'">Logout</button>
            </div>
        </header>
        <div id="menu-section" class="section active">
            {menu_html}
        </div>
        <div id="staff-section" class="section">
            {staff_html}
        </div>
        <div id="order-section" class="section">
            {order_html}
        </div>
        <div id="profile-section" class="section">
            {profile_html}
            {profile_html_edit}
        </div>
        <script>
            function toggleSection(sectionId) {{
                var sections = document.querySelectorAll('.section');
                sections.forEach(function(section) {{
                    section.classList.remove('active');
                }});
                document.getElementById(sectionId).classList.add('active');
            }}
        </script>
    </body>
    </html>
    '''

@app.route("/bill/<int:pk>/<int:order_id>", methods=["GET"])
def generate_bill(pk, order_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT 
            o.id AS order_id, o.date, o.time, o.total_price, o.table_no,
            m.item_name AS item_name, c.quantity, m.price AS item_price, 
            (c.quantity * m.price) AS item_total_price
        FROM `Order` o
        JOIN `Cart` c ON o.session_id = c.session_id
        JOIN `Menu` m ON c.item = m.id
        WHERE o.id = ?
    ''', (order_id,))
    order_details = cursor.fetchall()
    cursor.close()
    if not order_details:
        return "<h1>Order not found</h1>", 404
    cart_html = ""
    subtotal = 0
    for item in order_details:
        cart_html += f"""
            <tr>
                <td>{item[5]}</td> <!-- item_name -->
                <td>{item[6]}</td> <!-- quantity -->
                <td>₹{item[7]:.2f}</td> <!-- item_price -->
                <td>₹{item[8]:.2f}</td> <!-- item_total_price -->
            </tr>
        """
        subtotal += item[8]
    gst = subtotal * 0.02 
    final_price = subtotal + gst
    bill_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hotel Invoice</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f7f7f7;
            }}
            .invoice-container {{
                max-width: 800px;
                margin: 0 auto;
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .header p {{
                margin: 5px 0;
                font-size: 14px;
                color: #666;
            }}
            .details, .items, .total {{
                margin-bottom: 20px;
            }}
            .items table {{
                width: 100%;
                border-collapse: collapse;
            }}
            .items table th, .items table td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            .items table th {{
                background-color: #f4f4f4;
                font-weight: bold;
            }}
            .total {{
                text-align: right;
            }}
            .total h3 {{
                margin: 0;
                font-size: 20px;
                color: #333;
            }}
        </style>
    </head>
    <body>
        <div class="invoice-container">
            <div class="header">
                <h1>Hotel Name</h1>
                <p>123 Luxury Lane, Downtown City</p>
                <p>Phone: +1-234-567-890 | Email: contact@hotelabc.com</p>
            </div>

            <div class="details">
                <table>
                    <tr>
                        <td><strong>Date:</strong> {order_details[0][1]}</td>
                        <td><strong>Invoice Number:</strong> INV{order_id}</td>
                    </tr>
                    <tr>
                        <td><strong>Time:</strong> {order_details[0][2]}</td>
                        <td><strong>Table Number:</strong> {order_details[0][4]}</td>
                    </tr>
                </table>
            </div>

            <div class="items">
                <h2>Bill Details</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Item</th>
                            <th>Quantity</th>
                            <th>Price</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {cart_html}
                    </tbody>
                </table>
            </div>

            <div class="total">
                <h3>Subtotal: ₹{subtotal:.2f}</h3>
                <h3>GST (2%): ₹{gst:.2f}</h3>
                <h3><strong>Total Amount: ₹{final_price:.2f}</strong></h3>
                <br>
                <button style="margin: 10px; padding: 10px 20px; background-color: #28a745; border: none; color: white;" onclick="window.print()">Print Page</button>
                <button style="margin: 10px; padding: 10px 20px; background-color: #28a745; border: none; color: white;" onclick="window.location.href='/staff-dashboard/{pk}'">Back</button>
                <br>
            </div>
            <div class="footer">
                <p>Thank you for staying with us!</p>
                <p>We look forward to serving you again.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(bill_template)

@app.route("/")
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hotel Management System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }
            header {
                background-color: #4CAF50;
                color: white;
                padding: 20px 0;
                font-size: 24px;
            }
            .container {
                display: flex;
                justify-content: space-around;
                align-items: center;
                margin: 50px auto;
                width: 80%;
            }
            .hotel-image {
                width: 40%;
            }
            .buttons {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            .button {
                padding: 15px 30px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <header>
            <img src="/static/img/logo.png" alt="Hotel Logo" style="vertical-align: middle; width: 50px;">
            <span>Hotel Name</span>
        </header>
        <div class="container">
            <img src="/static/img/bg.jpeg" alt="Hotel Picture" class="hotel-image">
            <div class="buttons">
                <button class="button" onclick="window.location.href='/staff-login'">Staff Login</button>
                <button class="button" onclick="window.location.href='/customer-login'">Customer Login</button>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route("/customer-login")
def customer_login():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Customer Dashboard</title>
    </head>
    <body>
        <h1 style="text-align:center;">Hotel Name</h1>
        <div style="text-align:center;">
            <img src="/static/img/logo.png" alt="Hotel Logo" style="width: 10%; margin-top: 20px;">
        </div>
        <div style="text-align:center; margin-top: 20px;">
            <h2>Customer Dashboard</h2>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; margin-top: 50px;">
            <button style="margin: 10px; padding: 10px 20px; background-color: #63a4ff; border: none; color: white;" onclick="window.location.href='/menu'">Show Menu</button>
            <button style="margin: 10px; padding: 10px 20px; background-color: #28a745; border: none; color: white;" onclick="window.location.href='/'">Exit</button>
        </div>
    </body>
    </html>
    '''

@app.route("/menu")
def show_menu():
    categories = get_categories_from_db()
    category_buttons = ''.join([f'<button onclick="window.location.href=\'/category/{category}\'">{category.capitalize()}</button>' for category in categories])
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Menu</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            header {{
                background-color: #4CAF50;
                color: white;
                padding: 20px 0;
                font-size: 24px;
            }}
            .menu-container {{
                display: flex;
                justify-content: space-between;
                margin: 30px;
            }}
            .categories {{
                width: 20%;
                text-align: left;
                padding-right: 20px;
            }}
            .categories button {{
                margin: 10px 0;
                padding: 15px 30px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
            }}
            .categories button:hover {{
                background-color: #45a049;
            }}
            .dish-grid {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
                width: 75%;
            }}
            .dish-card {{
                width: 200px;
                padding: 10px;
                background-color: white;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
                border-radius: 10px;
                text-align: center;
            }}
            .dish-card img {{
                width: 100%;
                height: auto;
                border-radius: 5px;
            }}
            .dish-card h3 {{
                margin-top: 10px;
                font-size: 18px;
            }}
            .dish-card p {{
                margin-top: 5px;
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <header>
            <img src="/static/img/logo.png" alt="Hotel Logo" style="vertical-align: middle; width: 50px;">
            <span>Hotel Name</span>
        </header>
        <h2>Select a Category</h2>
        <div class="menu-container">
            <!-- Left-side categories -->
            <div class="categories">
                {category_buttons}
                <button style="margin: 10px; padding: 10px 20px; background-color: grey; border: none; color: white;" onclick="window.location.href='/'">Exit</button>
            </div>
            
            <!-- Right-side dishes -->
            <div class="dish-grid">
                <!-- Dishes will be dynamically inserted here -->
            </div>
        </div>
    </body>
    </html>
    '''
    return html_content

@app.route("/category/<category_name>", methods=["GET", "POST"])
def category_page(category_name):
    categories = get_categories_from_db()  
    category_buttons = ''.join([f'<button onclick="window.location.href=\'/category/{category}\'">{category.capitalize()}</button>' for category in categories])
    if request.method == "POST":
        item_id = request.form.get("item_id")
        quantity = int(request.form.get("quantity", 1)) 
        session_id = session.get('session_id')
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, item_name, price, review, no_of_reviews FROM Menu WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        if item:
            cursor.execute("SELECT id, quantity FROM Cart WHERE item = ? AND session_id = ?", (item_id, session_id))
            existing_item = cursor.fetchone()
            if existing_item:
                cursor.execute("DELETE FROM Cart WHERE item = ? AND session_id = ?", (item_id, session_id))
            cursor.execute(
                "INSERT INTO Cart (item, quantity, price, session_id) VALUES (?, ?, ?, ?)",
                (item["id"], quantity, item["price"] * quantity, session_id)
            )
            db.commit()
    category_data = get_dishes_for_category(category_name.capitalize())
    if not category_data:
        return f"<h2>No dishes found for category: {category_name}</h2>"
    dishes_html = ""
    for dish in category_data:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT quantity FROM Cart WHERE item = ? AND session_id = ?", (dish['id'], session['session_id']))
        cart_item = cursor.fetchone()
        quantity_value = cart_item['quantity'] if cart_item else 0
        avg_review = (dish['review']/dish['no_of_reviews']) if (dish['no_of_reviews'] > 0) else 0
        stars = "★" * int(round(avg_review)) + "☆" * (5 - int(round(avg_review)))
        dishes_html += f'''
        <div class="dish-card">
            <img src="/static/img/{dish['id']}.jpg" alt="{dish['item_name']}">
            <h3>{dish['item_name']}</h3>
            <h3>{stars} {avg_review}</h3>
            <h3>₹{dish['price']:.2f}</h3>
            <form action="/category/{category_name}" method="POST" style="margin-top: 10px;">
                <input type="hidden" name="session_id" value="{session['session_id']}" >
                <input type="hidden" name="item_id" value="{dish['id']}" >
                <label for="quantity_{dish['id']}">Quantity:</label>
                <input type="number" id="quantity_{dish['id']}" name="quantity" value="{quantity_value}" min="0" style="width: 60px; margin-left: 5px;">
                <br><br>
                <button type="submit">Add to Cart</button>
            </form>
        </div>
        '''
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{category_name.capitalize()} - Menu</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            header {{
                background-color: #4CAF50;
                color: white;
                padding: 20px 0;
                font-size: 24px;
                position: relative;
            }}
            .cart-button {{
                position: absolute;
                right: 20px;
                top: 20px;
                background-color: #FF5733;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
            }}
            .cart-button:hover {{
                background-color: #FF4500;
            }}
            .menu-container {{
                display: flex;
                justify-content: space-between;
                margin: 30px;
            }}
            .categories {{
                width: 20%;
                text-align: left;
                padding-right: 20px;
            }}
            .categories button {{
                margin: 10px 0;
                padding: 15px 30px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
            }}
            .categories button:hover {{
                background-color: #45a049;
            }}
            .dish-grid {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
                width: 75%;
            }}
            .dish-card {{
                width: 200px;
                padding: 10px;
                background-color: white;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
                border-radius: 10px;
                text-align: center;
            }}
            .dish-card img {{
                width: 100%;
                height: auto;
                border-radius: 5px;
            }}
            .dish-card h3 {{
                margin-top: 10px;
                font-size: 18px;
            }}
            .dish-card p {{
                margin-top: 5px;
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <header>
            <img src="/static/img/logo.png" alt="Hotel Logo" style="vertical-align: middle; width: 50px;">
            <span>Hotel Name</span>
            <button class="cart-button" onclick="window.location.href='/cart'">Cart</button>
        </header>
        <h2>{category_name.capitalize()}</h2>
        <div class="menu-container">
            <div class="categories">
                {category_buttons}
                <button style="margin: 10px; padding: 10px 20px; background-color: grey; border: none; color: white;" onclick="window.location.href='/'">Exit</button>
            </div>
            <div class="dish-grid">
                {dishes_html}
            </div>
        </div>
    </body>
    </html>
    '''
    return html_content

@app.route("/cart", methods=["GET", "POST"])
def cart_page():
    session_id = session.get('session_id')
    db = get_db()
    cursor = db.cursor() 
    if request.method == "POST":
        current_datetime = datetime.now() 
        date = current_datetime.date()  
        time = current_datetime.strftime("%H:%M:%S")
        cart_table_no = request.form.get("cart_table_no")   
        cursor.execute('''
            SELECT SUM(m.price * c.quantity) 
            FROM Cart c
            JOIN Menu m ON c.item = m.id
            WHERE c.session_id = ?
        ''', (session_id,))
        total_price = cursor.fetchone()[0]
        cursor.execute('''
            INSERT INTO `Order` (session_id, total_price, date, time, table_no )
            VALUES (?, ?, ?, ?, ?)
        ''', (session_id, total_price, date, time, cart_table_no))
        db.commit()
        return redirect(url_for('bill_page'))
    cursor.execute('''
        SELECT m.item_name, c.quantity, m.price
        FROM Cart c
        JOIN Menu m ON c.item = m.id
        WHERE c.session_id = ?
    ''', (session_id,))
    cart_items = cursor.fetchall()
    if not cart_items:
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cart - Hotel</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }}
                header {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px 0;
                    font-size: 24px;
                    position: relative;
                }}
                .cart-table {{
                    width: 80%;
                    margin: 20px auto;
                    border-collapse: collapse;
                    text-align: left;
                }}
                .cart-table th, .cart-table td {{
                    border: 1px solid #ddd;
                    padding: 10px;
                }}
                .cart-table th {{
                    background-color: #4CAF50;
                    color: white;
                }}
                .total-price {{
                    margin-top: 20px;
                    font-size: 20px;
                    font-weight: bold;
                }}
                .order-button {{
                    margin-top: 30px;
                    padding: 10px 20px;
                    font-size: 18px;
                    background-color: #FF5733;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }}
                .order-button:hover {{
                    background-color: #FF4500;
                }}
            </style>
        </head>
        <body>
            <header>
                <img src="/static/img/logo.png" alt="Hotel Logo" style="vertical-align: middle; width: 50px;">
                <span>Hotel Name</span>
            </header>
            <h2>Cart</h2>
            <h3>Your Cart is empty</h3>
            <button class="order-button" onclick="window.location.href='/category/Biryani'">Go Back</button>
        </body>
        </html>
        '''
    cart_html = ""
    total_price = 0
    for idx, item in enumerate(cart_items, start=1):
        item_name, quantity, price = item
        total_item_price = price * quantity
        total_price += total_item_price
        cart_html += f'''
        <tr>
            <td>{idx}</td>
            <td>{item_name}</td>
            <td>₹{price:.2f}</td>
            <td>{quantity}</td>
            <td>₹{total_item_price:.2f}</td>
        </tr>
        '''
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cart - Hotel</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            header {{
                background-color: #4CAF50;
                color: white;
                padding: 20px 0;
                font-size: 24px;
                position: relative;
            }}
            .cart-table {{
                width: 80%;
                margin: 20px auto;
                border-collapse: collapse;
                text-align: left;
            }}
            .cart-table th, .cart-table td {{
                border: 1px solid #ddd;
                padding: 10px;
            }}
            .cart-table th {{
                background-color: #4CAF50;
                color: white;
            }}
            .total-price {{
                margin-top: 20px;
                font-size: 20px;
                font-weight: bold;
            }}
            .order-button {{
                margin-top: 30px;
                padding: 10px 20px;
                font-size: 18px;
                background-color: #FF5733;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            .order-button:hover {{
                background-color: #FF4500;
            }}
        </style>
    </head>
    <body>
        <header>
            <img src="/static/img/logo.png" alt="Hotel Logo" style="vertical-align: middle; width: 50px;">
            <span>Hotel Name</span>
        </header>
        <h2>Cart</h2>
        <table class="cart-table">
            <thead>
                <tr>
                    <th>S.No</th>
                    <th>Dish Name</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Total Price</th>
                </tr>
            </thead>
            <tbody>
                {cart_html}
            </tbody>
        </table>
        <div class="total-price">
            Total Price: ₹{total_price:.2f}
        </div>
        <form method="POST">
            <label for="cart_table_no">Table no:</label>
            <input type="number" id="cart_table_no" name="cart_table_no" required>
            <button class="order-button" type="submit">Order Now</button>
        </form>
        <button class="order-button" onclick="window.location.href='/category/Biryani'">Go Back</button>
    </body>
    </html>
    '''

@app.route("/bill")
def bill_page():
    session_id = session.get('session_id')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT m.item_name, c.quantity, c.price
        FROM Cart c
        JOIN Menu m ON c.item = m.id
        WHERE c.session_id = ?
    ''', (session_id,))
    cart_items = cursor.fetchall()
    if not cart_items:
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bill - Hotel</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }}
                header {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px 0;
                    font-size: 24px;
                }}
                .order-button {{
                    margin-top: 30px;
                    padding: 10px 20px;
                    font-size: 18px;
                    background-color: #FF5733;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }}
                .order-button:hover {{
                    background-color: #FF4500;
                }}
            </style>
        </head>
        <body>
            <header>
                <span>Hotel Name</span>
            </header>
            <h2>Bill</h2>
            <h3>Your cart is empty!</h3>
            <button class="order-button" onclick="window.location.href='/category/Biryani'">Go Back</button>
        </body>
        </html>
        '''
    prices = get_price_from_db() 
    cart_html = ""
    total_price = 0 
    for idx, item in enumerate(cart_items, start=1):
        item_name, quantity, _ = item 
        item_price = prices.get(item_name, 0)
        item_total = item_price * quantity
        total_price += item_total 
        gst = total_price * 0.02
        final_price = gst+total_price
        cart_html += f'''
        <tr>
            <td>{item_name}</td>
            <td>{quantity}</td>
            <td>₹{item_price:.2f}</td>
            <td>₹{item_price * quantity:.2f}</td>
        </tr>
        '''
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hotel Invoice</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f7f7f7;
            }}
            .invoice-container {{
                max-width: 800px;
                margin: 0 auto;
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .header p {{
                margin: 5px 0;
                font-size: 14px;
                color: #666;
            }}
            .details, .items, .total {{
                margin-bottom: 20px;
            }}
            .items table {{
                width: 100%;
                border-collapse: collapse;
            }}
            .items table th, .items table td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            .items table th {{
                background-color: #f4f4f4;
                font-weight: bold;
            }}
            .total {{
                text-align: right;
            }}
            .total h3 {{
                margin: 0;
                font-size: 20px;
                color: #333;
            }}
        </style>
    </head>
    <body>
        <div class="invoice-container">
            <div class="header">
                <h1>Hotel Name</h1>
                <p>123 Luxury Lane, Downtown City</p>
                <p>Phone: +1-234-567-890 | Email: contact@hotelabc.com</p>
            </div>

            <div class="details">
                <table>
                    <tr>
                        <td><strong>Date:</strong> {datetime.now().strftime("%Y-%m-%d")}</td>
                        <td><strong>Invoice Number:</strong> INV12345</td>
                    </tr>
                </table>
            </div>

            <div class="items">
                <h2>Bill Details</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Item</th>
                            <th>Quantity</th>
                            <th>Price</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {cart_html}
                    </tbody>
                </table>
            </div>

            <div class="total">
                <h3>Subtotal: ₹{total_price:.2f}</h3>
                <h3>GST (2%): ₹{gst:.2f}</h3>
                <h3><strong>Total Amount: ₹{final_price:.2f}</strong></h3>
                <br>
                <button style="margin: 10px; padding: 10px 20px; background-color: #28a745; border: none; color: white;" onclick="window.print()">Print Page</button>
                <br>
                <button style="margin: 10px; padding: 10px 20px; background-color: #28a745; border: none; color: white;" class="order-button" onclick="window.location.href='/review'">Review</button>
            </div>
            <div class="footer">
                <p>Thank you for staying with us!</p>
                <p>We look forward to serving you again.</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route("/review", methods=["GET", "POST"])
def review_page():
    db = get_db()
    cursor = db.cursor()
    session_id = session.get('session_id')
    if request.method == "POST":
        item_id = request.form.get("item_id")
        new_review = float(request.form.get("review"))
        cursor.execute('''
            UPDATE Menu
            SET review = review + ?,
                no_of_reviews = no_of_reviews + 1
            WHERE id = ?
        ''', (new_review, item_id))
        db.commit()
        return redirect(url_for('review_page'))
    cursor.execute('''
        SELECT m.id, m.item_name, m.category, m.price, m.review, m.no_of_reviews
        FROM Menu m
        JOIN Cart c ON m.id = c.item
        WHERE c.session_id = ?
    ''', (session_id,))
    menu_items = cursor.fetchall()
    review_html = ""
    for item in menu_items:
        item_id, item_name, category, price, review, no_of_reviews = item
        average_review = (review / no_of_reviews) if no_of_reviews > 0 else 0
        stars = "★" * int(round(average_review)) + "☆" * (5 - int(round(average_review)))
        review_html += f'''
        <tr>
            <td>{item_name}</td>
            <td>{category}</td>
            <td>₹{price:.2f}</td>
            <td>{stars} ({average_review:.1f}/5)</td>
            <td>
                <form method="POST" style="display:inline;">
                    <input type="hidden" name="item_id" value="{item_id}">
                    <select name="review" required>
                        <option value="" disabled selected>Rate</option>
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                    </select>
                    <button type="submit">Submit</button>
                </form>
            </td>
        </tr>
        '''
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reviews - Hotel</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            header {{
                background-color: #4CAF50;
                color: white;
                padding: 20px 0;
                font-size: 24px;
                position: relative;
            }}
            .review-table {{
                width: 80%;
                margin: 20px auto;
                border-collapse: collapse;
                text-align: left;
            }}
            .review-table th, .review-table td {{
                border: 1px solid #ddd;
                padding: 10px;
            }}
            .review-table th {{
                background-color: #4CAF50;
                color: white;
            }}
            .form-container {{
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <header>
            <img src="/static/img/logo.png" alt="Hotel Logo" style="vertical-align: middle; width: 50px;">
            <span>Hotel</span>
        </header>
        <h2>Dish Reviews</h2>
        <table class="review-table">
            <thead>
                <tr>
                    <th>Dish Name</th>
                    <th>Category</th>
                    <th>Price</th>
                    <th>Review</th>
                    <th>Rate</th>
                </tr>
            </thead>
            <tbody>
                {review_html}
            </tbody>
        </table>
            <button style="margin: 10px; padding: 10px 20px; background-color: #28a745; border: none; color: white;" onclick="window.location.href='/'">Exit</button>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(debug=True)

