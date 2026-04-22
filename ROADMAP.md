# Roadmap

## Completed (v2.0)

- [x] JWT short-lived tokens + capability RBAC
- [x] Layered detection (regex + scoring + TF-IDF classifier + allowlist)
- [x] Multilingual attack corpus (EN/FR/DE/ES + obfuscated)
- [x] FP/FN metrics on all detectors
- [x] Entropy-based secret scanning
- [x] All tools behind mandatory auth
- [x] Correlation IDs + JSONL audit export
- [x] Egress control (domain allowlist)
- [x] CI: GitHub Actions, CodeQL, Dependabot, SBOM
- [x] OSS packaging (LICENSE, CONTRIBUTING, CHANGELOG)
- [x] Docker Compose
- [x] Fuzzing + load test suites

## Planned (v2.1)

- [ ] ML-based prompt injection classifier (fine-tuned transformer)
- [ ] NLI-based contradiction detection for data poisoning
- [ ] OIDC/OAuth2 integration (Keycloak, Auth0)
- [ ] SQLite/PostgreSQL persistence backend
- [ ] SIEM export (Splunk HEC, ELK, Loki)
- [ ] Web UI dashboard for attack/defense visualization
- [ ] Arabic, Chinese, Japanese, Korean attack corpus
- [ ] Adversarial robustness evaluation (GCG, AutoDAN)
- [ ] SLSA provenance attestation on releases

## Planned (v3.0)

- [ ] Multi-agent scenario (agent-to-agent injection)
- [ ] Real-time content filtering pipeline
- [ ] WAF integration (ModSecurity rules)
- [ ] mTLS with client certificate auth
- [ ] Canary token system for data exfiltration detection
- [ ] Automated red-team evaluation framework
