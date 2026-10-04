"""
Secure version of the training application.

The application demonstrates:
- Environment variables for secrets
- No eval()
- Parameterized SQL queries
- Input validation
- Restricted file access
- Safe exception handling
"""

import os
import re
import sqlite3
from pathlib import Path


ALLOWED_DIR = Path(__file__).resolve().parent / "allowed_files"
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{1,50}$")


def get_api_secret():
    """Read the secret from the environment instead of source code."""
    return os.getenv("APP_API_SECRET")


def validate_username(username):
    """Allow only a small, predictable username format."""
    if not isinstance(username, str) or not USERNAME_PATTERN.fullmatch(username):
        raise ValueError("Invalid username format.")
    return username


def find_user(username):
    """Use a parameterized query to prevent SQL injection."""
    username = validate_username(username)

    connection = sqlite3.connect("secure_users.db")
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, username FROM users WHERE username = ?",
            (username,),
        )
        return cursor.fetchone()
    except sqlite3.Error:
        # Do not expose database internals to the user.
        raise RuntimeError("Unable to complete the database operation.")
    finally:
        connection.close()


def read_allowed_file(filename):
    """Read only files that remain inside the application's allowed directory."""
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("A file name is required.")

    requested_path = (ALLOWED_DIR / filename).resolve()

    try:
        requested_path.relative_to(ALLOWED_DIR)
    except ValueError:
        raise ValueError("File access is restricted to the allowed directory.")

    if not requested_path.is_file():
        raise FileNotFoundError("Requested file was not found.")

    try:
        return requested_path.read_text(encoding="utf-8")
    except OSError:
        raise RuntimeError("Unable to read the requested file.")


def calculate_expression(expression):
    """
    Safe replacement for eval().

    This example intentionally supports only basic integer arithmetic
    using a strict whitelist. It is not a general-purpose expression parser.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be text.")

    expression = expression.strip()

    if len(expression) > 30 or not re.fullmatch(r"[0-9+\-*/% ()]+", expression):
        raise ValueError("Only basic arithmetic characters are allowed.")

    # A tiny educational parser using Python's AST avoids eval().
    import ast
    import operator

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](
                evaluate(node.left), evaluate(node.right)
            )
        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](evaluate(node.operand))
        raise ValueError("Unsupported arithmetic expression.")

    try:
        tree = ast.parse(expression, mode="eval")
        return evaluate(tree)
    except (SyntaxError, ValueError, ZeroDivisionError, TypeError):
        raise ValueError("Invalid arithmetic expression.")


if __name__ == "__main__":
    print("Secure Coding Review Demo")

    secret = get_api_secret()
    print("Secret configured:", "yes" if secret else "no")

    expression = input("Enter a basic arithmetic expression: ")
    try:
        print("Result:", calculate_expression(expression))
    except ValueError:
        print("Invalid expression.")

    username = input("Enter a username to search: ")
    try:
        print("User:", find_user(username))
    except (ValueError, RuntimeError):
        print("Unable to complete the user search.")

    filename = input("Enter a file name from the allowed_files directory: ")
    try:
        print(read_allowed_file(filename))
    except (ValueError, FileNotFoundError, RuntimeError):
        print("Unable to read the requested file.")
