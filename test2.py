import sqlite3
import os
import random
import hashlib
import logging

# CWE-798: Hardcoded credentials
DEFAULT_ADMIN = {
    "username": "superuser",
    "password": "admin1234"
}

# CWE-312: Store sensitive data in plain text
USER_DB_PATH = "users.db"

logging.basicConfig(level=logging.INFO)

# Initialize DB
def init_db():
    conn = sqlite3.connect(USER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    return conn

# CWE-89: SQL Injection
def unsafe_login(conn, username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor = conn.cursor()
    cursor.execute(query)
    user = cursor.fetchone()
    return user is not None

# CWE-327: Weak hashing
def weak_md5_hash(data):
    return hashlib.md5(data.encode()).hexdigest()

# CWE-330: Weak random generator
def generate_otp():
    return str(random.randint(100000, 999999))

# CWE-22: Path Traversal
def unsafe_read_file(filename):
    path = os.path.join("data", filename)
    with open(path, "r") as f:
        return f.read()

# CWE-134: Format string
def log_unfiltered(message):
    logging.info(message % "ALERT")

# CWE-306: No auth check on admin-only function
def reset_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users;")
    conn.commit()
    print("All users deleted!")  # No auth check

# Main AI logic dispatcher
def agent_dispatch(conn, command: str):
    if command.startswith("login"):
        _, user, pwd = command.split()
        if unsafe_login(conn, user, pwd):
            return "Welcome!"
        return "Access Denied"
    elif command.startswith("readfile"):
        _, filename = command.split()
        return unsafe_read_file(filename)
    elif command == "otp":
        return generate_otp()
    elif command == "log_alert":
        log_unfiltered("Unauthorized attempt %s")
        return "Logged alert"
    elif command == "reset":
        reset_all_data(conn)
        return "Data Reset Triggered"
    else:
        return "Command not recognized"

if _name_ == "_main_":
    conn = init_db()
    cursor = conn.cursor()

    # Insert hardcoded user (if DB empty)
    cursor.execute("SELECT COUNT(*) FROM users;")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       (DEFAULT_ADMIN['username'], DEFAULT_ADMIN['password']))
        conn.commit()

    print(agent_dispatch(conn, "login superuser admin1234"))
    print(agent_dispatch(conn, "readfile ../../etc/passwd"))
    print(agent_dispatch(conn, "otp"))
    print(agent_dispatch(conn, "log_alert"))
    print(agent_dispatch(conn, "reset"))  # No auth
