# Supporting Scripts

This directory contains utility scripts used to support MCP integration, management, and governance experiments.

## Scripts

| File | Description |
| --- | --- |
| `generate-token.py` | Python utility for generating RSA-signed JSON Web Tokens (JWTs) for testing authentication and persona-based authorization with Anypoint Omni Gateway. |

## JWT Generation

The `generate-token.py` utility supports three Service Desk personas: Employee, Support Agent, and Administrator. It also supports generating expired JWTs and JWTs with an incorrect audience for negative authentication testing.

### Prerequisites

Before generating JWTs, ensure that:

- The RSA private key exists at `credentials/private.pem`.
- The Python virtual environment is activated, with dependencies from `requirements.txt` installed.

For instructions on generating the RSA key pair and configuring the Python environment, see [JWT Authentication](../docs/jwt-authentication.md).

### Generating Required JWTs

From the repository root, generate the required JWTs:

```bash
# Valid Employee JWT
python scripts/generate-token.py employee > credentials/employee.jwt

# Employee JWT with an incorrect audience
python scripts/generate-token.py employee --wrong-audience > credentials/employee-wrong-audience.jwt

# Expired Employee JWT
python scripts/generate-token.py employee --expired > credentials/employee-expired.jwt

# Valid Support Agent JWT
python scripts/generate-token.py support-agent > credentials/support-agent.jwt

# Valid Administrator JWT
python scripts/generate-token.py administrator > credentials/administrator.jwt
```

The utility uses the private key `credentials/private.pem` to sign JWTs. The generated tokens are stored in the `credentials/` folder and excluded from Git.

---

Copyright © 2026 Alan Belisle. Licensed under the [Apache License 2.0](../LICENSE.txt).
