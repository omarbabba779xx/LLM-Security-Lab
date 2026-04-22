# Changelog

All notable changes to this project are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versioned per [Semantic Versioning](https://semver.org/).

## [2.0.0] — 2024-12-XX

### Added
- **JWT authentication** with short-lived tokens (`/auth/token` endpoint) alongside backward-compatible static tokens.
- **Capability-based RBAC** — fine-grained permissions (`rag:read`, `tool:write_file`, `security:audit`, etc.).
- **Correlation IDs** on every HTTP request via `X-Correlation-ID` header/middleware.
- **Egress control** — allowlist of permitted outbound domains.
- **Layered detection** in all security filters:
  - TF-IDF semantic classifier (no ML dependency).
  - Heuristic scoring with weighted signals.
  - Task allowlist to reduce false positives.
  - Multilingual attack corpus (EN, FR, DE, ES + obfuscated).
- **Detection metrics** (TP/FP/TN/FN, precision, recall, F1) on every detector.
- **Entropy-based secret detection** in addition to regex patterns.
- **JSONL audit export** for SIEM integration (`data/audit_log.jsonl`).
- **Severity levels** on audit log entries (`debug`, `info`, `warning`, `error`, `critical`).
- **CI/CD pipeline** — GitHub Actions with pytest, benchmark, ruff, mypy, bandit, semgrep, pip-audit.
- **CodeQL** analysis (weekly + on push).
- **Dependabot** for pip and GitHub Actions dependencies.
- **SBOM generation** (CycloneDX) in CI.
- **Docker Compose** for one-command demo launch.
- **Fuzzing test suite** for security filters.
- **Load testing** script with response time metrics.
- OSS packaging: `LICENSE` (MIT), `CONTRIBUTING.md`, `CHANGELOG.md`, `ROADMAP.md`.
- `pyproject.toml` with ruff, mypy, pytest, bandit configuration.

### Changed
- All tool policies now require authentication (`require_auth: True`).
- `OutputValidator` patterns enriched (iframe, object, embed, document.cookie, eval, JNDI).
- `DataPoisoningDetector` uses semantic similarity in addition to regex.
- API version bumped to `2.0.0`.

### Fixed
- Absolute Windows paths in `docs/OWASP_LLMSecurity.md` replaced with relative links.

## [1.2.0] — 2024-11-XX

### Added
- Rate limiting via SlowAPI (30/min RAG, 60/min global).
- Audit logging with JSON persistence.
- Optional OpenAI backend with fallback mock.
- `/health` and `/security/audit` endpoints.
- `SECURITY.md` with threat model.
- Professional README with Mermaid diagrams.

## [1.0.0] — 2024-10-XX

### Added
- Initial release: vulnerable + secure RAG/agent lab.
- 5 OWASP LLM attack scenarios with demonstrations.
- FastAPI API with role-based auth.
- Pytest suite (14 tests) + CLI benchmark (21 checks).
