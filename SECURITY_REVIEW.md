# Security Review

## Project

**Secure Coding Review – Python Vulnerability Assessment**

This project compares intentionally vulnerable Python code with a corrected version. Bandit is used for static security analysis.

## Vulnerability Summary

| ID | Vulnerability | File | Severity | Impact |
|---|---|---|---|---|
| V-01 | Hardcoded secret | `vulnerable_app.py` | High | Secrets stored in source can be exposed through Git history, source sharing, or unauthorized access. |
| V-02 | Unsafe `eval()` | `vulnerable_app.py` | High | Untrusted input can be interpreted as Python code, potentially allowing arbitrary code execution. |
| V-03 | SQL injection | `vulnerable_app.py` | High | User input is concatenated into SQL, allowing unintended SQL syntax to alter a query. |
| V-04 | Unsafe file path handling | `vulnerable_app.py` | High | A user-controlled path can access files outside the intended application area. |

> Severity values are educational project classifications, not a formal CVSS score.

## Detailed Review

### V-01: Hardcoded Secret

**Problem:** A secret is directly written in the Python source.

**Security impact:** Anyone who can read the source or repository may obtain the secret. Git history can also preserve previously committed secrets.

**Remediation:** Read secrets from environment variables or a dedicated secrets manager. Never commit real credentials.

**Secure implementation:** `secure_app.py` reads `APP_API_SECRET` using `os.getenv()`.

### V-02: Unsafe `eval()`

**Problem:** `eval()` interprets input as Python code.

**Security impact:** If untrusted input reaches `eval()`, an attacker may execute operations that the application never intended to permit.

**Remediation:** Do not use `eval()` for user input. Parse only the expected syntax and implement a strict allowlist.

**Secure implementation:** `secure_app.py` parses a small arithmetic grammar with Python's `ast` module and an operator allowlist.

### V-03: SQL Injection

**Problem:** The vulnerable application builds SQL by concatenating a username into the query string.

**Security impact:** Special SQL syntax supplied as input can change the meaning of the database query.

**Remediation:** Use parameterized/prepared SQL statements.

**Secure implementation:** The secure version uses SQLite placeholders (`?`) and passes the username separately.

### V-04: Unsafe File Path Handling

**Problem:** The vulnerable application accepts an arbitrary path directly from the user.

**Security impact:** A user may request files outside the application's intended directory.

**Remediation:** Resolve the requested path and verify that it is inside a predefined allowed directory before reading it.

**Secure implementation:** `read_allowed_file()` uses `Path.resolve()` and `Path.relative_to()` to enforce the directory boundary.

## Secure Coding Recommendations

1. Never commit passwords, API keys, tokens, or private keys.
2. Prefer environment variables or a secrets manager for application secrets.
3. Avoid dynamic code execution such as `eval()` and `exec()`.
4. Use parameterized SQL queries.
5. Validate input according to an allowlist where possible.
6. Normalize and validate filesystem paths before access.
7. Return generic user-facing errors and keep sensitive details out of error messages.
8. Keep dependencies updated.
9. Run static analysis tools such as Bandit during development.
10. Review security findings manually; automated scanners do not replace human review.
11. Use `.gitignore` to prevent local secrets and generated files from entering Git.
12. Run security checks before pushing code to a public repository.

## Expected Audit Workflow

```text
Vulnerable Code
      ↓
Run Bandit
      ↓
Vulnerability Findings
      ↓
Manual Security Review
      ↓
Secure Code Changes
      ↓
Run Bandit Again
      ↓
Review Remaining Findings
```

## Re-test

Run:

```bash
python run_audit.py
```

The vulnerable application should generate security findings. The secure application should have substantially fewer or no findings related to the vulnerabilities demonstrated in this project.

A clean Bandit result does not automatically prove that software is secure. Manual review and functional testing are still required.
