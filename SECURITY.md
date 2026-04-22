# Politique de sécurité — LLM Security Lab

## Threat model

Ce projet modélise un assistant LLM avec RAG et outils agentiques exposé via une API. Les menaces considérées suivent le **OWASP Top 10 for LLM Applications**.

### Acteurs

| Acteur | Capacités | Objectif |
|---|---|---|
| Utilisateur légitime (`reader`) | lecture RAG, calculatrice, lecture fichiers sandbox | obtenir des réponses utiles |
| Contributeur (`editor`) | ingestion de documents, écriture fichiers sandbox | alimenter le corpus |
| Admin (`admin`) | tous les rôles + audit + (opt-in) mode vulnérable | opérer le système |
| Attaquant externe | prompts arbitraires, documents empoisonnés | injection, exfiltration, RCE, DoS |
| Insider malveillant | jeton valide volé | abus de privilèges |

### Surfaces attaquées

1. **Prompt utilisateur** → injection directe
2. **Corpus RAG** → injection indirecte + poisoning
3. **Outils** → path traversal, RCE via shell, exfiltration par email/HTTP
4. **Sortie LLM** → XSS, SQLi, template injection chez le consommateur

## Contrôles implémentés

### Préventifs

- **AuthN** : `X-API-Key` validé côté serveur, pas de confiance dans le body client
- **AuthZ** : rôles `reader`/`editor`/`admin`, permissions par outil
- **Opt-in vulnérable** : flag `LLM_LAB_ENABLE_VULNERABLE_DEMO` + rôle admin
- **Sandbox fichiers** : `pathlib.Path.resolve()` + `relative_to()` sur `data/`
- **Calculatrice** : `ast.parse()` restreint à `Add/Sub/Mult/Div/Mod`, pas d'`eval()`
- **Normalisation Unicode** : NFKD avant toute regex de détection
- **Validation input** : longueurs max query/contexte, extensions whitelist
- **Validation output** : patterns XSS, SQLi, JNDI, template
- **Détection secrets** : regex OpenAI/GitHub/AWS/JWT + redaction
- **Isolement** : RAG scopé par `user_id`, pas de fuite cross-tenant

### Détectifs

- **Audit log** : `data/audit_log.json` — toute requête RAG, exécution d'outil, quarantaine
- **Scan poisoning** : à l'ingestion, score + quarantaine ≥ 1 match
- **Health endpoint** : `/health` pour supervision externe

### Correctifs

- **Rate limiting** : SlowAPI, 30/min sur `/rag/query`, 60/min global
- **Quarantaine** : documents suspects rejetés, journalisés, jamais indexés
- **Fallback LLM** : si OpenAI indisponible, bascule sur mock déterministe

## Ce qui n'est **pas** couvert

| Manque | Mitigation nécessaire en prod |
|---|---|
| Rotation des jetons | OIDC/OAuth2 + short-lived tokens |
| Chiffrement au repos | DB chiffrée (KMS) au lieu de JSON local |
| Détection ML | Classifieur de prompts + NLI sur documents |
| mTLS | Terminaison TLS + mutual auth |
| SIEM | Export audit → Splunk/ELK + alerting |
| WAF | Reverse proxy (Cloudflare, Nginx) |
| Content filtering sortant | Pipeline de modération côté LLM |

## Signalement de vulnérabilité

Ce dépôt étant un laboratoire pédagogique, merci d'ouvrir une issue publique sur GitHub pour toute vulnérabilité identifiée. **Ne pas** déployer le mode vulnérable (`LLM_LAB_ENABLE_VULNERABLE_DEMO=true`) sur un réseau accessible.

## Vérifications avant mise en ligne

```bash
# 1. Mode vulnérable désactivé
grep -r "LLM_LAB_ENABLE_VULNERABLE_DEMO" .env
# doit renvoyer: LLM_LAB_ENABLE_VULNERABLE_DEMO=false

# 2. Jetons régénérés
python -c "import secrets; print(secrets.token_urlsafe(32))"

# 3. Tests verts
python -m pytest -q
python tests/test_attacks.py
```
