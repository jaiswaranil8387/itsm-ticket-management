# ITSM Ticket Management Tool

A web-based IT Service Management (ITSM) application designed to streamline the creation, tracking, and resolution of IT support tickets. Built with Python, Flask, SQLite, and HTML, this tool simulates real-world helpdesk workflows, making it ideal for managing IT incidents and user support requests.

![Python](https://img.shields.io/badge/Python-3.10-blue) ![Flask](https://img.shields.io/badge/Flask-2.3.3-lightgrey) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue) ![HTML](https://img.shields.io/badge/HTML-5-orange) ![CSS](https://img.shields.io/badge/CSS-3-blue) ![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow) ![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple) ![Jinja2](https://img.shields.io/badge/Jinja2-3.1.2-green) ![Werkzeug](https://img.shields.io/badge/Werkzeug-2.3.6-red) ![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-1.21.0-green) ![Gunicorn](https://img.shields.io/badge/Gunicorn-21.2.0-pink) ![Docker](https://img.shields.io/badge/Docker-24.0.5-blue)

## Features
- **Ticket Management**: Create, edit, search, and track tickets with attributes like title, description, priority (High, Medium, Low), and status (Open, In Progress, Resolved).
- **User Authentication**: Secure login system with role-based access control (admin and readonly roles) using hashed passwords.
- **Admin Dashboard**: Admins can manage users (add/remove) and update ticket details, while readonly users can view tickets.
- **Ticket Search**: Search tickets by title for quick access to relevant issues.
- **Data Visualization**: Displays ticket priority and status distributions (via `/get_chart_data` endpoint, compatible with Chart.js).
- **Responsive UI**: Built with HTML and Jinja2 templates for a user-friendly interface, suitable for support staff.

## Technologies
- **Programming Languages**: Python, HTML, JavaScript, SQL
- **Framework**: Flask (Python web framework)
- **Database**: SQLite (lightweight, serverless database)
- **Security**: Werkzeug for password hashing and secure authentication
- **Templating**: Jinja2 for dynamic HTML rendering
- **Frontend**: Bootstrap (implied for responsive design)
- **Version Control**: Git, hosted on GitHub

## Prerequisites
- Python 3.6 or higher
- pip (Python package manager)
- Git
- Docker


## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jaiswaranil8387/itsm-ticket-management.git
   cd src
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Initialize the Database**:
   - The application automatically creates a `tickets.db` SQLite database with sample tickets and a default admin user (username: `admin`, password: `admin123`) on first run.

4. **Create Environment File**:
   - Create a `.env` file in the root directory of the project with the following variables:
     ```
     FLASK_SECRET_KEY=your_secret_key_here
     DB_PASSWORD=your_db_password
     TUNNEL_TOKEN=your_tunnel_token_here_if_using_cloudflare
     
     ```
     Replace the placeholder values with your actual database credentials and a secure secret key.
     
5. **Run the Application**:
   You can run the application in two ways:

   **Option 1: Direct Python Execution**
   ```bash
   python app.py
   ```

   **Option 2: Using Docker Compose**
   ```bash
   docker-compose -f docker-compose-postgres.yaml up --build
   ```
6. **Access the Application**:
   1. For direct python app
      http://localhost:5000
   2. For docker
      http://localhost:5000
      https://uat.aniljaiswar.pp.ua/
   - Log in with the default admin credentials or create new users via the admin dashboard.

## Usage
- **Login**: Use the default admin credentials (username: `admin`, password: `admin123`) or create a new user.
- **Create Tickets**: Admins can add tickets via the "Create Ticket" tab, specifying title, description, and priority.
- **Manage Tickets**: Update ticket status (Open, In Progress, Resolved) or edit ticket details from the ticket list.
- **Search Tickets**: Use the search bar to find tickets by title.
- **Manage Users**: Admins can add or remove users via the "Manage Users" tab.
- **View Analytics**: Check ticket priority and status distributions (requires Chart.js integration for visualization).

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request on GitHub.

Please report bugs or suggest features via the [Issues](https://github.com/jaiswaranil8387/itsm-ticket-management/issues) page.

## License
This project is licensed under the MIT License.

## Contact
For questions or feedback, reach out via [GitHub Issues](https://github.com/jaiswaranil8387/itsm-ticket-management/issues).