# Secure Coding Review – Python Vulnerability Assessment

A beginner-friendly college cybersecurity mini-project that demonstrates how common Python security weaknesses can be identified and corrected.

## Project Goal

The project follows this workflow:

**Vulnerable Code → Security Scan → Vulnerability Report → Secure Code → Re-test**

The vulnerable application contains four intentionally unsafe patterns:

- Hardcoded secret
- Unsafe `eval()`
- SQL injection
- Unsafe file path handling

The secure version demonstrates safer alternatives.

## Technologies

- Python 3
- SQLite
- Bandit
- Git / GitHub

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/secure-coding-review.git
cd secure-coding-review
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## How to Run

### Vulnerable demo

```bash
python vulnerable_app.py
```

This file is intentionally insecure and is included only for security-learning purposes.

### Secure demo

Windows Command Prompt:

```bash
set APP_API_SECRET=DEMO_SECRET_FOR_LOCAL_TESTING_ONLY
python secure_app.py
```

PowerShell:

```powershell
$env:APP_API_SECRET="DEMO_SECRET_FOR_LOCAL_TESTING_ONLY"
python secure_app.py
```

Linux/macOS:

```bash
export APP_API_SECRET="DEMO_SECRET_FOR_LOCAL_TESTING_ONLY"
python secure_app.py
```

The value above is only a dummy local-development value. Do not replace it with a real credential in the repository.

## Security Audit

Run the complete Bandit audit:

```bash
python run_audit.py
```

Or run Bandit directly:

```bash
python -m bandit -r vulnerable_app.py secure_app.py
```

The vulnerable application is expected to produce findings. After correcting the issues, review the secure file again.

## Manual Re-test

Confirm that:

- No real secret exists in the source code.
- `eval()` is not used for user input.
- SQL uses parameters rather than string concatenation.
- File access is restricted to `allowed_files`.
- Invalid input is rejected.
- User-facing errors do not expose database or system details.
- Bandit is run against both versions.

## Project Structure

```text
secure-coding-review/
├── vulnerable_app.py
├── secure_app.py
├── run_audit.py
├── SECURITY_REVIEW.md
├── README.md
├── requirements.txt
├── .gitignore
└── allowed_files/
    └── sample.txt
```

## GitHub Safety

This repository is designed to be public-source friendly:

- No real passwords
- No API keys
- No personal information
- `.env` is ignored
- Virtual environments are ignored
- Python cache files are ignored

The hardcoded value in `vulnerable_app.py` is an explicitly fake training value and must never be replaced with a real secret.

## Git Commands

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git init
git add .
git commit -m "Initial secure coding review project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/secure-coding-review.git
git push -u origin main
```

## Educational Note

This project is intended for defensive cybersecurity education and secure coding practice. The vulnerable code should never be deployed as a real application.
