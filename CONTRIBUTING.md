# Contributing to LLM Security Lab

Thank you for your interest in contributing! This project is an educational security lab, and contributions that improve the coverage of OWASP LLM risks, add new attack/defense demonstrations, or enhance documentation are especially welcome.

## How to Contribute

### 1. Fork & Clone

```bash
git clone https://github.com/<your-fork>/llm-security-lab.git
cd llm-security-lab
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create a Branch

```bash
git checkout -b feat/your-feature-name
```

### 3. Make Changes

- Follow existing code style (PEP 8, type hints, docstrings).
- Add tests for new features — both pytest and benchmark checks.
- Do not weaken existing tests or remove security controls.
- Run linting: `ruff check app/ tests/`

### 4. Test

```bash
python -m pytest -q
python tests/test_attacks.py
```

All tests must pass before submitting a PR.

### 5. Commit & Push

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
feat: add German prompt injection patterns
fix: correct path traversal edge case on Windows
docs: update OWASP mapping for LLM04
test: add fuzzing corpus for OutputValidator
```

### 6. Open a Pull Request

- Describe the change and the OWASP risk it addresses.
- Reference related issues if applicable.
- Ensure CI passes (lint, test, security scan).

## Code of Conduct

Be respectful and constructive. This is an educational project — questions and beginner contributions are welcome.

## Security Issues

**Do NOT open a public issue for security vulnerabilities.** Use [GitHub Private Vulnerability Reporting](https://github.com/omarbabba779xx/llm-security-lab/security/advisories/new) instead. See [SECURITY.md](SECURITY.md) for details.

## Areas Where Help Is Needed

- Additional multilingual attack patterns (Arabic, Chinese, Japanese, Korean)
- More advanced obfuscation techniques (token splitting, Unicode tricks)
- Integration tests with real LLM APIs
- Performance benchmarks and optimization
- Documentation translations
