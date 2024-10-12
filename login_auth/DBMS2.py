import mysql.connector
from mysql.connector import Error

# Define connection parameters
db_config = {
    'host': 'localhost',           # Replace with your MySQL server host
    'user': 'root',        # Replace with your MySQL username
    'password': 'Tiger',    # Replace with your MySQL password
    'database': 'chatbot_db'        # Replace with your database name
}

def create_connection():
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connection successful")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_tables(connection):
    """Create tables in the MySQL database."""
    cursor = connection.cursor()
    try:
        # Create `users` table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """)

        # Create `chatbot_responses` table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chatbot_responses (
            response_id INT PRIMARY KEY AUTO_INCREMENT,
            condition_type VARCHAR(50) NOT NULL,
            response_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """)

        # Create `active_sessions` table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS active_sessions (
            session_id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT,
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """)

        # Create `user_interactions` table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_interactions (
            interaction_id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT,
            interaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            trigger_phrase VARCHAR(255),
            response_text TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """)

        # Create `employees` table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INT PRIMARY KEY AUTO_INCREMENT,
            employee_name VARCHAR(100) NOT NULL,
            position VARCHAR(50),
            department VARCHAR(50),
            contact_info VARCHAR(100),
            hire_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """)

        # Create `leave_requests` table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS leave_requests (
            request_id INT PRIMARY KEY AUTO_INCREMENT,
            employee_id INT,
            leave_start DATE,
            leave_end DATE,
            leave_type VARCHAR(50),
            status VARCHAR(20), -- e.g., Approved, Pending, Rejected
            request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        );
        """)

        # Create `office_timings` table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS office_timings (
            office_id INT PRIMARY KEY AUTO_INCREMENT,
            department VARCHAR(50),
            opening_time TIME,
            closing_time TIME,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """)

        print("Tables created successfully")

    except Error as e:
        print(f"Error: {e}")

def insert_sample_data(connection):
    """Insert sample data into the database tables."""
    cursor = connection.cursor()
    try:
        # Insert sample data into `chatbot_responses`
        cursor.executemany("""
        INSERT INTO chatbot_responses (condition_type, response_text) VALUES (%s, %s)
        """, [
            ('leave policies', 'Our leave policy includes 20 annual leaves, 10 sick leaves, and 5 casual leaves per year.'),
            ('general', 'Welcome to the HR chatbot! How can I assist you today?'),
            ('benefits', 'Our benefits package includes health insurance, a retirement savings plan, and performance bonuses.'),
            ('work hours', 'Our standard work hours are from 9 AM to 5 PM, Monday through Friday. Some departments may have different hours.'),
            ('remote work', 'We offer flexible remote work options. Please consult with your manager to discuss potential arrangements.'),
            ('employee handbook', 'You can access the employee handbook in the company portal or request a physical copy from HR.'),
            ('payroll schedule', 'Employees are paid bi-weekly. Payroll is processed every other Friday.'),
            ('training programs', 'We offer various training programs to help you develop your skills. Check the Learning & Development section on the intranet for more details.'),
            ('performance reviews', 'Performance reviews are conducted annually. Your manager will schedule a review meeting to discuss your performance and career development.'),
            ('vacation request', 'To request vacation time, please submit a request through the HR portal or contact your HR representative.'),
            ('sick leave', 'If you need to take sick leave, notify your manager and HR as soon as possible. A doctor\'s note may be required for extended absences.'),
            ('employee referral program', 'Our employee referral program rewards employees who refer successful candidates for open positions. Contact HR for more details.')
        ])

        # Insert sample data into `users`
        cursor.executemany("""
        INSERT INTO users (username, password_hash, first_name, last_name, email) VALUES (%s, %s, %s, %s, %s)
        """, [
            ('Aditya', 'adityakrjha', 'Aditya', 'jha', 'jhaa8933@gmail.com'),
            ('Atul', 'Atul1234', 'Atul', 'Patel', 'atulk4360@gmail.com'),
            ('janmejay', 'singh1234', 'janmejay', 'singh', 'janmejaykumarsingh@gmail.com'),
            ('omkar', 'omkar1234', 'omkar', 'agarwaal', 'omkaraggarwaal00@gmail.com'),
            ('Riddhi', 'riddhi1234', 'riddhi', 'singh', 'singhriddhi237@gmail.com'),
            ('Rose', 'rose1234', 'rose', 'banga', 'rosebanga1306@gmail.com')
        ])

        # Insert sample data into `employees`
        cursor.executemany("""
        INSERT INTO employees (employee_name, position, contact_info, hire_date) VALUES (%s, %s, %s, %s)
        """, [
            ('Aditya', 'Database_manager', 'jhaa8933@gmail.com', '2006-07-09'),
            ('Atul', 'backend_developer', 'atulk4360@gmail.com', '2006-07-09'),
            ('Janmejay', 'backend_manager', 'janmejaykumarsingh@gmail.com', '2006-07-09'),
            ('Omkar', 'frontend_developer', 'omkaraggarwaal00@gmail.com', '2006-07-09'),
            ('Riddhi', 'frontend_manager', 'singhriddhi237@gmail.com', '2006-07-09'),
            ('Rose', 'Networking', 'rosebanga1306@gmail.com', '2006-07-09')
        ])

        # Insert sample data into `office_timings`
        cursor.executemany("""
        INSERT INTO office_timings (department, opening_time, closing_time) VALUES (%s, %s, %s)
        """, [
            ('Engineering', '09:00:00', '17:00:00'),
            ('Human Resources', '09:00:00', '17:00:00')
        ])

        connection.commit()
        print("Sample data inserted successfully")

    except Error as e:
        print(f"Error: {e}")

def main():
    """Main function to connect to the database, create tables, and insert sample data."""
    connection = create_connection()
    if connection:
        create_tables(connection)
        insert_sample_data(connection)
        connection.close()

if __name__ == "__main__":
    main()
