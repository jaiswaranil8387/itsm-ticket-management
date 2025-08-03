from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
from datetime import datetime
from collections import Counter
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT,
            status TEXT,
            created_at TEXT
        )
    ''')

    # ✅ Check if tickets already exist
    cursor.execute('SELECT COUNT(*) FROM tickets')
    count = cursor.fetchone()[0]

    if count == 0:
        # Insert sample tickets only if table is empty
        sample_tickets = [
            ('Login Failure', 'User reports login issue on portal', 'High', 'Open', '2025-07-20 10:00:00'),
            ('Application Crash', 'App crashes during data import', 'High', 'In Progress', '2025-07-20 11:15:00'),
            ('Report Generation Issue', 'Report not generating correctly', 'Medium', 'Open', '2025-07-20 12:30:00'),
            ('UI Glitch', 'Minor display issue on dashboard', 'Low', 'Resolved', '2025-07-20 09:45:00')
        ]
        cursor.executemany('''
            INSERT INTO tickets (title, description, priority, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_tickets)
    
        # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('admin', 'readonly')) NOT NULL
        )
    ''')

    # Optional: Add default admin if none exists
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        from werkzeug.security import generate_password_hash
        cursor.execute('''
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        ''', ('admin', generate_password_hash('admin123'), 'admin'))


    conn.commit()
    conn.close()


# Add a new ticket
def add_ticket(title, description, priority):
    if priority not in ['High', 'Medium', 'Low']:
        priority = 'Low'  # Default if invalid
    status = 'Open'
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tickets (title, description, priority, status, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, description, priority, status, created_at))
    conn.commit()
    conn.close()
    return priority

# Update ticket status
def update_ticket_status(ticket_id, new_status):
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tickets SET status = ? WHERE id = ?', (new_status, ticket_id))
    conn.commit()
    conn.close()

# Update ticket title, description, and priority
def update_ticket(ticket_id, title, description, priority):
    if priority not in ['High', 'Medium', 'Low']:
        priority = 'Low'  # Default if invalid
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tickets SET title = ?, description = ?, priority = ? WHERE id = ?', (title, description, priority, ticket_id))
    conn.commit()
    conn.close()
    return priority

# Get all tickets
def get_all_tickets():
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tickets')
    tickets = cursor.fetchall()
    conn.close()
    return tickets

# Search tickets by title
def search_tickets_by_title(query):
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tickets WHERE title LIKE ?', ('%' + query + '%',))
    tickets = cursor.fetchall()
    conn.close()
    return tickets

# Get a single ticket by ID
def get_ticket_by_id(ticket_id):
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,))
    ticket = cursor.fetchone()
    conn.close()
    return ticket

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        conn = sqlite3.connect('tickets.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password, role FROM users WHERE username = ?', (uname,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], pwd):
            session['username'] = uname
            session['role'] = user[1]
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.before_request
def require_login():
    allowed_routes = ['login', 'static']
    if 'username' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('login'))

# Flask routes
@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get('search_query', '') if request.method == 'POST' else ''
    
    if query:
        tickets = search_tickets_by_title(query)
    else:
        tickets = get_all_tickets()

    # Avoid crash when no tickets exist
    priorities = [ticket[3] for ticket in tickets if len(ticket) > 3]
    statuses = [ticket[4] for ticket in tickets if len(ticket) > 4]

    priority_counts = dict(Counter(priorities))
    status_counts = dict(Counter(statuses))

    return render_template(
        'index.html',
        tickets=tickets,
        search_query=query,
        priority_counts=priority_counts,
        status_counts=status_counts,
        active_tab='home',
        role=session.get('role')
    )

@app.route("/home")
def home():
    tickets = get_all_tickets()

    priorities = [ticket[3] for ticket in tickets]  # assuming 3rd index is priority
    statuses = [ticket[4] for ticket in tickets]    # assuming 4th index is status

    priority_counts = dict(Counter(priorities))
    status_counts = dict(Counter(statuses))

    return render_template("index.html",
                           tickets=tickets,
                           priority_counts=priority_counts,
                           status_counts=status_counts,
                           active_tab='home',
                           role=session.get('role'))

@app.route("/get_chart_data")
def get_chart_data():
    tickets = get_all_tickets()

    priorities = [ticket[3] for ticket in tickets]  # assuming 3rd index is priority
    statuses = [ticket[4] for ticket in tickets]    # assuming 4th index is status

    priority_counts = dict(Counter(priorities))
    status_counts = dict(Counter(statuses))

    return jsonify({
        'priority_counts': priority_counts,
        'status_counts': status_counts
    })

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('search_query', '')     if request.method == 'POST' else ''
    if query:
        tickets = search_tickets_by_title(query)
    else:
        tickets = get_all_tickets()
    return render_template('index.html', tickets=tickets, search_query=query, active_tab='search')
    
@app.route('/incident')
def incident():
    tickets = get_all_tickets()
    return render_template('index.html', tickets=tickets, active_tab='incident')

@app.route('/add_ticket', methods=['POST'])
def add_ticket_route():
    if session.get('role') != 'admin':
        flash('Unauthorized: Only admin can create tickets.', 'danger')
        return redirect(url_for('index'))

    title = request.form.get('title')
    description = request.form.get('description')
    priority = request.form.get('priority')
    if title and description and priority:
        priority = add_ticket(title, description, priority)
        flash(f'Ticket submitted with {priority} priority!', 'success')
    else:
        flash('Please fill in all fields.', 'danger')
    return redirect(url_for('index'))

@app.route('/update_status/<int:ticket_id>/<status>')
def update_status_route(ticket_id, status):
    if session.get('role') != 'admin':
        flash('Unauthorized: Only admin can update status.', 'danger')
        return redirect(url_for('index'))
        
    if status in ['Open', 'In Progress', 'Resolved']:
        update_ticket_status(ticket_id, status)
        flash(f'Ticket {ticket_id} marked as {status}.', 'success')
    else:
        flash('Invalid status.', 'danger')
    return redirect(url_for('index'))

@app.route('/edit_ticket/<int:ticket_id>', methods=['GET', 'POST'])
def edit_ticket_route(ticket_id):
    if session.get('role') != 'admin':
        flash('Unauthorized: Only admin can edit tickets.', 'danger')
        return redirect(url_for('index'))
       
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        flash('Ticket not found.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        if title and description and priority:
            priority = update_ticket(ticket_id, title, description, priority)
            flash(f'Ticket {ticket_id} updated with {priority} priority!', 'success')
        else:
            flash('Please fill in all fields.', 'danger')
        return redirect(url_for('index'))
    
    tickets = get_all_tickets()
    return render_template('index.html', tickets=tickets, edit_ticket=ticket, active_tab='create', role=session.get('role'))

@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if session.get('role') != 'admin':
        flash("Unauthorized access", "danger")
        return redirect(url_for('index'))

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    # Fetch existing users for display
    cursor.execute('SELECT username, role FROM users')
    users = cursor.fetchall()  # Fetch all rows
    print(f"Fetched users: {users}")  # Debug print to check data
    users_list = [{'username': row[0], 'role': row[1]} for row in users]  # Convert to list of dicts

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        action = request.form.get('action')

        valid_roles = ['admin', 'readonly']

        if action == 'add':
            if not username or not password or not role:
                flash("Please fill all fields.", "danger")
            elif role not in valid_roles:
                flash("Invalid role selected.", "danger")
            else:
                hashed_pw = generate_password_hash(password)
                try:
                    cursor.execute(
                        'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                        (username, hashed_pw, role)
                    )
                    flash(f"User '{username}' added as {role}.", 'success')
                    # Refresh users list after addition
                    cursor.execute('SELECT username, role FROM users')
                    users = cursor.fetchall()
                    users_list = [{'username': row[0], 'role': row[1]} for row in users]
                except sqlite3.IntegrityError:
                    flash(f"User '{username}' already exists.", 'warning')

        elif action == 'remove':
            if not username:
                flash("No username provided for deletion.", "warning")
            else:
                cursor.execute('DELETE FROM users WHERE username = ?', (username,))
                flash(f"User '{username}' removed.", 'info')
                # Refresh users list after deletion
                cursor.execute('SELECT username, role FROM users')
                users = cursor.fetchall()
                users_list = [{'username': row[0], 'role': row[1]} for row in users]

        conn.commit()

    conn.close()
    return render_template('index.html', users=users_list, active_tab='manage_users', role=session.get('role'))
    
@app.route('/existing_users', methods=['GET', 'POST'])
def existing_users():
    if session.get('role') != 'admin':
        flash("Unauthorized access", "danger")
        return redirect(url_for('index'))

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    # Fetch existing users for display
    cursor.execute('SELECT username, role FROM users')
    users = cursor.fetchall()  # Fetch all rows
    conn.close()
    users_list = [{'username': row[0], 'role': row[1]} for row in users]
    return jsonify(users_list)

# Initialize database and run app
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)