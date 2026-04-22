# Security Policy — LLM Security Lab

## Supported Versions

| Version | Supported |
|---|---|
| 2.x (current) | ✅ Active |
| 1.x | ⚠️ Security fixes only |
| < 1.0 | ❌ End of life |

## Threat Model

This project models an LLM assistant with RAG and agentic tools exposed via a FastAPI API. Threats follow the **OWASP Top 10 for LLM Applications**.

### Actors

| Actor | Capabilities | Objective |
|---|---|---|
| Legitimate user (`reader`) | RAG queries, calculator, file read in sandbox | Get useful answers |
| Contributor (`editor`) | Document ingestion, sandbox file write | Feed the corpus |
| Admin (`admin`) | All roles + audit + (opt-in) vulnerable mode | Operate the system |
| External attacker | Arbitrary prompts, poisoned documents | Injection, exfiltration, RCE, DoS |
| Malicious insider | Stolen valid token | Privilege abuse |

### Attack Surfaces

1. **User prompt** → direct injection
2. **RAG corpus** → indirect injection + data poisoning
3. **Tools** → path traversal, RCE via shell, exfiltration via email/HTTP
4. **LLM output** → XSS, SQLi, template injection at downstream consumer
5. **Authentication** → token theft, replay, privilege escalation

## Implemented Controls

### Preventive

- **AuthN**: Dual mode — JWT short-lived tokens (HS256, configurable TTL) + static API keys for dev
- **AuthZ**: Capability-based RBAC (`rag:read`, `tool:write_file`, `security:audit`, etc.)
- **All tools require authentication** — no unauthenticated tool access
- **Egress control**: Domain allowlist for outbound URLs
- **Opt-in vulnerable mode**: env flag `LLM_LAB_ENABLE_VULNERABLE_DEMO` + admin capability
- **File sandbox**: `pathlib.Path.resolve()` + `relative_to()` confined to `data/`
- **Calculator**: `ast.parse()` restricted to `Add/Sub/Mult/Div/Mod` — no `eval()`
- **Unicode normalization**: NFKD before all regex detection
- **Input validation**: max query/context length, extension whitelist
- **Output validation**: categorized patterns (XSS, SQLi, JNDI, template, code injection)
- **Secret detection**: regex + Shannon entropy scanning + automatic redaction
- **Tenant isolation**: RAG scoped per `user_id`, no cross-tenant leakage
- **Correlation IDs**: every request tagged for traceability

### Detective

- **Layered detection**: regex rules → heuristic scoring → TF-IDF semantic classifier → task allowlist
- **FP/FN metrics**: every detector tracks precision, recall, F1 for measurable evaluation
- **Audit log**: `data/audit_log.json` + `data/audit_log.jsonl` (SIEM-ready) with severity levels
- **Poisoning scan**: regex + semantic similarity at ingestion, quarantine ≥ 0.3 score
- **Health endpoint**: `/health` for external monitoring

### Corrective

- **Rate limiting**: SlowAPI — 30/min on `/rag/query`, 60/min global
- **Quarantine**: suspect documents rejected, logged, never indexed
- **LLM fallback**: if OpenAI unavailable, deterministic mock response

### Supply Chain

- **CI/CD**: GitHub Actions with pytest, ruff, mypy, bandit, semgrep, pip-audit
- **CodeQL**: weekly + on-push static analysis
- **Dependabot**: automated dependency updates
- **SBOM**: CycloneDX generated on every CI run

## What Is **NOT** Covered (Production Gaps)

| Gap | Required Mitigation |
|---|---|
| Token rotation | OIDC/OAuth2 with short-lived + refresh tokens |
| Encryption at rest | KMS-encrypted database instead of local JSON |
| ML detection | Fine-tuned transformer classifier + NLI |
| mTLS | TLS termination + mutual auth |
| SIEM | Export audit → Splunk/ELK + real-time alerting |
| WAF | Reverse proxy (Cloudflare, ModSecurity) |
| Outbound content filtering | LLM moderation pipeline |

## Reporting a Vulnerability

> **⚠️ Do NOT open a public GitHub issue for security vulnerabilities.**

### Private Vulnerability Reporting (Preferred)

Use **GitHub's Private Vulnerability Reporting**:

1. Go to [Security Advisories → New](https://github.com/omarbabba779xx/llm-security-lab/security/advisories/new)
2. Fill in the vulnerability details
3. We will triage within **48 hours** and coordinate a fix

### Email (Alternative)

If private reporting is unavailable, email the maintainer with:
- Description of the vulnerability
- Steps to reproduce
- Impact assessment
- Suggested fix (if any)

### What to Expect

| Timeline | Action |
|---|---|
| **48h** | Acknowledgment of report |
| **7 days** | Triage and severity assessment |
| **30 days** | Fix developed and tested |
| **45 days** | Security advisory published |

### Scope

- Vulnerabilities in `app/secure/` are **in scope** — these should be robust
- Vulnerabilities in `app/vulnerable/` are **intentional** and out of scope
- Infrastructure issues (CI, dependencies) are in scope

## Pre-Deployment Checklist

```bash
# 1. Vulnerable mode disabled
grep -r "LLM_LAB_ENABLE_VULNERABLE_DEMO" .env
# must return: LLM_LAB_ENABLE_VULNERABLE_DEMO=false

# 2. Tokens regenerated
python -c "import secrets; print(secrets.token_urlsafe(32))"

# 3. JWT secret set
echo $LLM_LAB_JWT_SECRET  # must be set, not default

# 4. All tests green
python -m pytest -q
python tests/test_attacks.py

# 5. Security scan clean
bandit -r app/ --severity-level medium
pip-audit --requirement requirements.txt
```
