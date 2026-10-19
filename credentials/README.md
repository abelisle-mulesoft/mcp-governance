# Authentication Credentials

This directory contains locally generated RSA keys and JSON Web Tokens (JWTs) used for MCP authentication and authorization experiments. Only this README is tracked in Git; generated keys and JWTs are excluded through `.gitignore`.

## Typical Contents

| File | Purpose |
| ---- | ---- |
| `private.pem` |	RSA private key used to sign JWTs. |
| `public.pem` |	RSA public key used by Omni Gateway to validate JWT signatures. |
| `administrator.jwt` |	Valid JWT for the Administrator persona. |
| `employee.jwt` |	Valid JWT for the Employee persona. |
| `employee-expired.jwt` |	Expired Employee JWT for negative authentication testing. |
| `employee-wrong-audience.jwt` |	Employee JWT with an incorrect audience for negative authentication testing. |
| `support-agent.jwt` |	Valid JWT for the Support Agent persona. |

## Security

Generated keys and JWTs must remain local and must not be committed to Git. JWTs should be regenerated when expired.

For instructions on generating RSA keys, creating JWTs, and configuring Omni Gateway JWT Validation, see [JWT Authentication](../docs/jwt-authentication.md).

---

Copyright © 2026 Alan Belisle. Licensed under the [Apache License 2.0](../LICENSE.txt).
