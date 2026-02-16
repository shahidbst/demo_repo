import sqlite3
import os
import random
import hashlib

# CWE-798: Hardcoded credentials
USERNAME = "admin"
PASSWORD = "password123"

# Connect to (or create) a local database
conn = sqlite3.connect("agent.db")
cursor = conn.cursor()

# CWE-89: SQL Injection vulnerability
def login(user_input_username, user_input_password):
    query = f"SELECT * FROM users WHERE username = '{user_input_username}' AND password = '{user_input_password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        return "Login successful!"
    return "Login failed."

# CWE-327: Use of weak hashing algorithm (MD5)
def weak_hash(data):
    return hashlib.md5(data.encode()).hexdigest()

# CWE-330: Predictable random number
def generate_token():
    return str(random.randint(1000, 9999))  # Weak entropy

# CWE-22: Path traversal vulnerability
def read_file(filename):
    with open("data/" + filename, "r") as f:
        return f.read()

# CWE-134: Uncontrolled format string
def log_event(event):
    print(event % "!!!")  # if event includes %s or other format codes

# Mock AI processing function
def agent_action(input_command):
    if input_command == "analyze":
        return weak_hash("analyze_task")
    elif input_command.startswith("read"):
        return read_file(input_command.split(" ")[1])
    elif input_command.startswith("token"):
        return generate_token()
    elif input_command.startswith("login"):
        _, user, pwd = input_command.split(" ")
        return login(user, pwd)
    elif input_command.startswith("log"):
        return log_event(input_command.split(" ", 1)[1])
    return "Unknown command"

# Example Usage
if _name_ == "_main_":
    print(agent_action("login admin password123"))  # Vulnerable login
    print(agent_action("read ../../etc/passwd"))    # Path traversal
    print(agent_action("log %s"))                   # Format string vulnerability
    print(agent_action("token"))                    # Weak random token
