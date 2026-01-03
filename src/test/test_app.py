import pytest
import sys
import os
import psycopg2
from unittest.mock import patch, MagicMock
from werkzeug.security import generate_password_hash


# 1. SETUP: Add parent directory to path to import 'app.py'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app  # noqa: E402


# 2. FIXTURES
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'test_secret_key'
    with app.test_client() as client:
        yield client
@pytest.fixture
def mock_db():
    """
    Mocks psycopg2.connect. Returns the mock cursor so we can spy on .execute() calls.
    """
    with patch('app.psycopg2.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Configure connect() to return mock_conn
        mock_connect.return_value = mock_conn
        # Configure conn.cursor() to return mock_cursor
        mock_conn.cursor.return_value = mock_cursor
        
        yield mock_cursor
# Helper function to find specific SQL statements in the execution history
def assert_sql_executed(mock_cursor, partial_query):
    """
    Iterates through all calls to cursor.execute() and returns True 
    if any of them contain the partial_query string.
    """
    calls = mock_cursor.execute.call_args_list
    query_found = any(partial_query in str(call.args[0]) for call in calls)
    
    if not query_found:
        # Print executed queries for debugging if assertion fails
        executed_queries = [str(call.args[0]) for call in calls]
        print(f"\n[DEBUG] Expected SQL containing: '{partial_query}'")
        print(f"[DEBUG] Actual SQL executed: {executed_queries}")
    
    assert query_found, f"SQL query containing '{partial_query}' was not executed."
# ----------------------------------------------------------------------
# 3. TESTS: Core Routes
# ----------------------------------------------------------------------
def test_health_check(client, mock_db):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_index_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_login_success(client, mock_db):
    hashed_pw = generate_password_hash('admin123')
    mock_db.fetchone.return_value = (hashed_pw, 'admin')

    response = client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Logged in successfully' in response.data


def test_login_failure(client, mock_db):
    hashed_pw = generate_password_hash('correct_password')
    mock_db.fetchone.return_value = (hashed_pw, 'admin')

    response = client.post('/login', data={
        'username': 'admin',
        'password': 'WRONG_PASSWORD'
    }, follow_redirects=True)

    assert b'Invalid credentials' in response.data


def test_logout(client):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
    response = client.get('/logout', follow_redirects=True)
    assert b'You have been logged out' in response.data

# ----------------------------------------------------------------------
# 4. TESTS: Ticket Management
# ----------------------------------------------------------------------


def test_dashboard_loads_tickets(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    # Prepare mock data for RealDictCursor behavior simulation
    # Note: In the actual app, you use RealDictCursor, but MagicMock usually returns tuples/lists.
    # For this test, verifying the data presence is enough.
    mock_tickets = [
        {'id': 1, 'title': 'Test Ticket', 'description': 'Desc',
         'priority': 'High', 'status': 'Open', 'created_at': '2025-01-01'}
    ]
    mock_db.fetchall.return_value = mock_tickets

    response = client.get('/')
    assert response.status_code == 200
    # Since we mocked the return, we assume the HTML renders these values
    # Note: The template expects a list of tuples or objects depending on cursor factory.
    # Given app.py: cursor = conn.cursor(cursor_factory=RealDictCursor)
    # The mock needs to return dicts, which we did.


def test_add_ticket_admin(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    response = client.post('/add_ticket', data={
        'title': 'New Bug',
        'description': 'Something broke',
        'priority': 'High'
    }, follow_redirects=True)

    assert response.status_code == 200
    # Check that INSERT was called (even if SELECT was called after)
    assert_sql_executed(mock_db, "INSERT INTO tickets")


def test_add_ticket_unauthorized(client, mock_db):
    # FIX: Added mock_db argument so it doesn't try to connect to real DB
    with client.session_transaction() as sess:
        sess['username'] = 'viewer'
        sess['role'] = 'readonly'

    response = client.post('/add_ticket', data={
        'title': 'Hack Attempt',
        'description': 'Should fail',
        'priority': 'High'
    }, follow_redirects=True)

    # Should verify that NO insert happened
    calls = mock_db.execute.call_args_list
    insert_calls = [str(call.args[0]) for call in calls
                    if "INSERT INTO tickets" in str(call.args[0])]
    assert len(insert_calls) == 0, "Readonly user should not trigger INSERT query"
    assert b'Unauthorized' in response.data


def test_update_ticket_status(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    response = client.get('/update_status/1/Resolved', follow_redirects=True)

    assert response.status_code == 200
    assert_sql_executed(mock_db, "UPDATE tickets SET status")


def test_edit_ticket_logic(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    # Mock fetching the ticket (GET)
    mock_ticket = {'id': 1, 'title': 'Old Title', 'description': 'Old Desc',
                   'priority': 'Low', 'status': 'Open', 'created_at': '2025-01-01'}
    mock_db.fetchone.return_value = mock_ticket

    client.post('/edit_ticket/1', data={
        'title': 'Updated Title',
        'description': 'Updated Desc',
        'priority': 'Medium'
    }, follow_redirects=True)

    assert_sql_executed(mock_db, "UPDATE tickets SET title")

# ----------------------------------------------------------------------
# 5. TESTS: User Management
# ----------------------------------------------------------------------


def test_manage_users_add(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    client.post('/manage_users', data={
        'action': 'add',
        'username': 'newuser',
        'password': 'password123',
        'role': 'readonly'
    }, follow_redirects=True)

    # Verify SQL execution instead of fragile HTML parsing
    assert_sql_executed(mock_db, "INSERT INTO users")


def test_manage_users_remove(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    client.post('/manage_users', data={
        'action': 'remove',
        'username': 'baduser'
    }, follow_redirects=True)

    assert_sql_executed(mock_db, "DELETE FROM users")


# ----------------------------------------------------------------------
# 6. TESTS: Search & Charts
# ----------------------------------------------------------------------


def test_search_functionality(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    mock_tickets = [
        {'id': 1, 'title': 'Found Me', 'description': 'Desc',
         'priority': 'Low', 'status': 'Open', 'created_at': '2025-01-01'}
    ]
    mock_db.fetchall.return_value = mock_tickets

    client.post('/search', data={'search_query': 'Found'}, follow_redirects=True)

    # Verify the correct SQL query was generated
    assert_sql_executed(mock_db, "SELECT * FROM tickets WHERE title ILIKE")


def test_chart_data_api(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'

    mock_tickets = [
        {'id': 1, 'title': 'A', 'description': 'D', 'priority': 'High',
         'status': 'Open', 'created_at': '...'},
        {'id': 2, 'title': 'B', 'description': 'D', 'priority': 'Low',
         'status': 'Resolved', 'created_at': '...'}
    ]
    mock_db.fetchall.return_value = mock_tickets

    response = client.get('/get_chart_data')
    assert response.status_code == 200
    json_data = response.json

    assert json_data['priority_counts']['High'] == 1
    assert json_data['status_counts']['Resolved'] == 1


def test_incident_route(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    mock_tickets = [{'id': 1, 'title': 'Incident Ticket', 'description': 'Desc',
                     'priority': 'High', 'status': 'Open', 'created_at': '2025-01-01'}]
    mock_db.fetchall.return_value = mock_tickets

    response = client.get('/incident')
    assert response.status_code == 200
    assert b'Incident Ticket' in response.data


def test_home_route(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    mock_tickets = [{'id': 1, 'title': 'Home Ticket', 'description': 'Desc',
                     'priority': 'Low', 'status': 'Open', 'created_at': '2025-01-01'}]
    mock_db.fetchall.return_value = mock_tickets

    response = client.get('/home')
    assert response.status_code == 200
    assert b'Home Ticket' in response.data


def test_existing_users(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    mock_users = [('admin', 'admin'), ('viewer', 'readonly')]
    mock_db.fetchall.return_value = mock_users

    response = client.get('/existing_users')
    assert response.status_code == 200
    json_data = response.json
    assert len(json_data) == 2
    assert json_data[0]['username'] == 'admin'


def test_require_login(client):
    response = client.get('/')  # Protected route
    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_index_authenticated(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    mock_tickets = [{'id': 1, 'title': 'Auth Ticket', 'description': 'Desc',
                     'priority': 'Medium', 'status': 'In Progress', 'created_at': '2025-01-01'}]
    mock_db.fetchall.return_value = mock_tickets

    response = client.get('/')
    assert response.status_code == 200
    assert b'Auth Ticket' in response.data


def test_search_empty_query(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    mock_tickets = [{'id': 1, 'title': 'Empty Search', 'description': 'Desc',
                     'priority': 'Low', 'status': 'Open', 'created_at': '2025-01-01'}]
    mock_db.fetchall.return_value = mock_tickets

    response = client.post('/search', data={'search_query': ''}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Empty Search' in response.data


def test_health_check_db_failure(client):
    with patch('app.get_db_connection', side_effect=Exception('DB Error')):
        response = client.get('/health')
        assert response.status_code == 503
        assert response.json['status'] == 'unhealthy'


def test_logout_enhanced(client):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
    response = client.get('/logout', follow_redirects=True)
    assert b'You have been logged out' in response.data
    # Enhanced: Check session is cleared
    with client.session_transaction() as sess:
        assert 'username' not in sess


def test_edit_ticket_logic_enhanced(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    # Mock fetching the ticket (GET)
    mock_ticket = {'id': 1, 'title': 'Old Title', 'description': 'Old Desc',
                   'priority': 'Low', 'status': 'Open', 'created_at': '2025-01-01'}
    mock_db.fetchone.return_value = mock_ticket

    client.post('/edit_ticket/1', data={
        'title': 'Updated Title',
        'description': 'Updated Desc',
        'priority': 'Medium'
    }, follow_redirects=True)

    # Enhanced: Check full UPDATE query
    assert_sql_executed(mock_db,
                        "UPDATE tickets SET title = %s, description = %s, priority = %s WHERE id = %s")


def test_manage_users_add_duplicate(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    # Mock IntegrityError for duplicate username on INSERT only
    def mock_execute(query, *args, **kwargs):
        if "INSERT INTO users" in query:
            raise psycopg2.IntegrityError
        return None

    mock_db.execute.side_effect = mock_execute

    response = client.post('/manage_users', data={
        'action': 'add',
        'username': 'admin',  # Duplicate
        'password': 'password123',
        'role': 'readonly'
    }, follow_redirects=True)

    assert b'already exists' in response.data


def test_update_status_invalid(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    response = client.get('/update_status/1/InvalidStatus', follow_redirects=True)

    assert b'Invalid status' in response.data
    # Ensure no UPDATE was executed
    calls = mock_db.execute.call_args_list
    update_calls = [call for call in calls
                    if "UPDATE tickets SET status" in str(call.args[0])]
    assert len(update_calls) == 0


def test_edit_ticket_get_form(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    # Mock fetching the ticket for GET request
    mock_ticket = {'id': 1, 'title': 'Test Ticket', 'description': 'Desc',
                   'priority': 'High', 'status': 'Open', 'created_at': '2025-01-01'}
    mock_db.fetchone.return_value = mock_ticket

    response = client.get('/edit_ticket/1')
    assert response.status_code == 200
    assert b'Test Ticket' in response.data


def test_edit_ticket_not_found(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    # Mock ticket not found
    mock_db.fetchone.return_value = None

    response = client.get('/edit_ticket/999', follow_redirects=True)
    assert b'Ticket not found' in response.data


def test_manage_users_get_page(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    mock_users = [('admin', 'admin'), ('user1', 'readonly')]
    mock_db.fetchall.return_value = mock_users

    response = client.get('/manage_users')
    assert response.status_code == 200
    assert b'manage_users' in response.data


def test_manage_users_add_invalid_role(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    response = client.post('/manage_users', data={
        'action': 'add',
        'username': 'testuser',
        'password': 'password123',
        'role': 'invalid_role'
    }, follow_redirects=True)

    assert b'Invalid role selected' in response.data


def test_manage_users_add_missing_fields(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    response = client.post('/manage_users', data={
        'action': 'add',
        'username': '',
        'password': '',
        'role': ''
    }, follow_redirects=True)

    assert b'Please fill all fields' in response.data


def test_manage_users_remove_missing_username(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    response = client.post('/manage_users', data={
        'action': 'remove',
        'username': ''
    }, follow_redirects=True)

    assert b'No username provided for deletion' in response.data


def test_manage_users_unauthorized(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'readonly_user'
        sess['role'] = 'readonly'

    response = client.get('/manage_users', follow_redirects=True)
    assert b'Unauthorized access' in response.data


def test_existing_users_unauthorized(client, mock_db):
    with client.session_transaction() as sess:
        sess['username'] = 'readonly_user'
        sess['role'] = 'readonly'

    response = client.get('/existing_users', follow_redirects=True)
    assert b'Unauthorized access' in response.data
