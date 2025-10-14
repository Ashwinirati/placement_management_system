from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'               # your MySQL username
app.config['MYSQL_PASSWORD'] = 'Deepa@1995'  # your MySQL password
app.config['MYSQL_DB'] = 'placement_system'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Ensure required tables exist to prevent runtime failures during registration/login
def init_db():
    try:
        # Ensure we have an application context before using mysql.connection
        with app.app_context():
            cur = mysql.connection.cursor()
            # students table
            cur.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
              id INT AUTO_INCREMENT PRIMARY KEY,
              name VARCHAR(255) NOT NULL,
              email VARCHAR(255) NOT NULL UNIQUE,
              password VARCHAR(255) NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            )
            # recruiters table
            cur.execute(
            """
            CREATE TABLE IF NOT EXISTS recruiters (
              id INT AUTO_INCREMENT PRIMARY KEY,
              name VARCHAR(255) NOT NULL,
              email VARCHAR(255) NOT NULL UNIQUE,
              password VARCHAR(255) NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            )
            # jobs table
            cur.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
              id INT AUTO_INCREMENT PRIMARY KEY,
              title VARCHAR(255) NOT NULL,
              description TEXT NOT NULL,
              recruiter_id INT NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (recruiter_id) REFERENCES recruiters(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            )
            # resumes table
            cur.execute(
            """
            CREATE TABLE IF NOT EXISTS resumes (
              id INT AUTO_INCREMENT PRIMARY KEY,
              student_id INT NOT NULL,
              filename VARCHAR(500) NOT NULL,
              filepath VARCHAR(1000) NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            )
            # applications table
            cur.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
              id INT AUTO_INCREMENT PRIMARY KEY,
              student_id INT NOT NULL,
              job_id INT NOT NULL,
              status ENUM('applied','shortlisted','rejected','interview_scheduled','hired') DEFAULT 'applied',
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              UNIQUE KEY uniq_student_job (student_id, job_id),
              FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
              FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            )
            # interviews table
            cur.execute(
            """
            CREATE TABLE IF NOT EXISTS interviews (
              id INT AUTO_INCREMENT PRIMARY KEY,
              application_id INT NOT NULL,
              scheduled_at DATETIME NOT NULL,
              mode VARCHAR(50) DEFAULT 'online',
              notes TEXT,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            )
            mysql.connection.commit()
    except Exception as e:
        # Avoid crashing app startup if DB is not reachable; routes will surface errors
        # You can inspect logs to diagnose DB connectivity
        print(f"[DB INIT] Skipped or failed to init tables: {e}")

# Initialize tables on import
init_db()
