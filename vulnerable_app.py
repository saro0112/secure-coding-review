"""
Intentionally vulnerable application for security training.

DO NOT use this code in production.
The vulnerabilities are included so Bandit and manual review can identify them.
"""

import sqlite3

# VULNERABILITY: hardcoded secret (Bandit B105)
API_SECRET = "DEMO_SECRET_DO_NOT_USE_IN_PRODUCTION"


def calculate_expression(expression):
    """VULNERABILITY: eval() executes arbitrary Python expressions."""
    return eval(expression)


def find_user(username):
    """VULNERABILITY: SQL injection through string concatenation."""
    connection = sqlite3.connect("vulnerable_users.db")
    cursor = connection.cursor()

    query = "SELECT id, username FROM users WHERE username = '" + username + "'"
    cursor.execute(query)

    result = cursor.fetchone()
    connection.close()
    return result


def read_file(filename):
    """VULNERABILITY: unrestricted path supplied by the user."""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


if __name__ == "__main__":
    print("Vulnerable Security Review Demo")
    print("This application intentionally contains security weaknesses.")

    user_input = input("Enter a Python expression to evaluate: ")
    try:
        print("Result:", calculate_expression(user_input))
    except Exception as error:
        print("Error:", error)

    username = input("Enter a username to search: ")
    try:
        print("User:", find_user(username))
    except sqlite3.Error as error:
        print("Database error:", error)

    filename = input("Enter a file path to read: ")
    try:
        print(read_file(filename))
    except OSError as error:
        print("File error:", error)
