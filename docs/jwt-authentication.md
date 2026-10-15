# JWT Authentication

This document describes the implementation of JWT-based authentication for MCP clients accessing a MuleSoft Omni Gateway.

The initial implementation uses locally generated RSA keys and self-issued JWTs, eliminating the need for an external identity provider or JWKS endpoint.

## RSA Key Pair

An RSA key pair is used to sign and validate JWTs:

- **Private key:** Signs JWTs locally.
- **Public key:** Configured in Omni Gateway to validate JWT signatures.

The RSA key pair uses a 2048-bit key length. JWTs are signed using RS256 (RSA with SHA-256).

### Generate RSA Keys

From the repository root:

```bash
# Generate RSA private key
openssl genpkey -algorithm RSA \
  -pkeyopt rsa_keygen_bits:2048 \
  -out _private/private.pem

# Extract public key
openssl pkey \
  -in _private/private.pem \
  -pubout \
  -out _private/public.pem

# Restrict private key permissions
chmod 600 _private/private.pem
```

### Verify RSA Keys

Verify the private key:

```bash
openssl rsa -in _private/private.pem -check -noout
```

Expected output:

```text
RSA key ok
```

Inspect the public key:

```bash
openssl rsa -pubin -in _private/public.pem -text -noout
```

The output should identify a 2048-bit RSA public key.

> [!NOTE]
> The version of LibreSSL bundled with macOS does not support the `openssl pkey -check` option. Use `openssl rsa -check` instead.

### Key Storage

Both keys are stored locally in `_private/`, which is excluded from Git.

> [!IMPORTANT]
> The private key must never be committed or shared. Only the public key is configured in Omni Gateway.

## JWT Generation

JWTs are generated locally using Python and the PyJWT library. Tokens are signed using the RSA private key and validated using the corresponding public key.

### Dependencies

Create a Python virtual environment and install the required dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The `requirements.txt` file contains:

```text
PyJWT[crypto]>=2.10,<3
```

### Generate a JWT

The `scripts/generate-token.py` utility generates signed JWTs for three personas:

| Persona       | Subject       | Role            |
| ------------- | ------------- | --------------- |
| Administrator | `admin001`    | `administrator` |
| Employee      | `employee001` | `employee`      |
| Support Agent | `support001`  | `support-agent` |

Generate an Employee JWT:

```bash
python scripts/generate-token.py employee
```

The utility reads the RSA private key from `_private/private.pem` and generates a JWT with the following claims:

| Claim   | Value                         | Description                    |
| ------- | ----------------------------- | ------------------------------ |
| `sub`   | `employee001`                 | Identity of the employee       |
| `iss`   | `brilliant-mule`              | Token issuer                   |
| `aud`   | `brilliant-mule-service-desk` | Intended audience              |
| `roles` | `["employee"]`                | Persona used for authorization |
| `iat`   | Current timestamp             | Token issuance time            |
| `exp`   | Current timestamp + 1 hour    | Token expiration time          |

JWTs use the RS256 signing algorithm and expire after one hour.

### Validate a JWT

Generate an Employee JWT and save it locally:

```bash
python scripts/generate-token.py employee > _private/employee.jwt
```

Validate the JWT using the RSA public key:

```bash
python - <<'PY'
from pathlib import Path
import jwt

token = Path("_private/employee.jwt").read_text().strip()
public_key = Path("_private/public.pem").read_bytes()

claims = jwt.decode(
    token,
    public_key,
    algorithms=["RS256"],
    audience="brilliant-mule-service-desk",
    issuer="brilliant-mule",
)

print(claims)
PY
```

Successful validation returns the decoded JWT claims, including the employee identity, role, issuer, audience, and timestamps.

This confirms that the JWT signature can be verified using the public key and that the issuer, audience, and expiration claims are valid.

> [!NOTE]
> Generated JWTs are stored in `_private/`, which is excluded from Git. Tokens should be treated as credentials and regenerated when expired.

## Omni Gateway JWT Validation

The JWT Validation policy authenticates MCP clients by validating their JWTs using the RSA public key generated locally. No external identity provider or JWKS endpoint is required.

### Policy Configuration

Apply the JWT Validation policy to the MCP server instance in Anypoint API Manager.

| Setting                    | Value                             |
| -------------------------- | --------------------------------- |
| JWT origin                 | HTTP Bearer Authentication Header |
| JWT Signing Method         | RSA                               |
| JWT Signing Key Length     | 256                               |
| JWT Key origin             | Text                              |
| JWT Key                    | Base64-encoded RSA public key     |
| Skip Client Id Validation  | Enabled                           |
| Validate Audience Claim    | Enabled                           |
| Audience                   | `brilliant-mule-service-desk`     |
| Expiration Claim Mandatory | Enabled                           |
| Not Before Claim Mandatory | Disabled                          |
| Validate Custom Claim      | Disabled                          |
| Claims to headers          | Not configured                    |

The JWT Key field requires the Base64-encoded public key without the PEM delimiters (`BEGIN PUBLIC KEY` and `END PUBLIC KEY`). To extract the Base64-encoded public key without the PEM delimiters:

```bash
sed '/-----BEGIN PUBLIC KEY-----/d; /-----END PUBLIC KEY-----/d' \
  _private/public.pem | tr -d '\n'
echo
```

The `echo` command adds a terminating newline, preventing Zsh from displaying its `%` end-of-output indicator immediately after the key.

### Policy Ordering

The working inbound policy order is:

1. JWT Validation
2. MCP Support
3. MCP Schema Validation
4. MCP Transcoding Router

> [!NOTE]
> **Finding:** The MCP Bridge automatically provisions MCP Support, MCP Schema Validation, and MCP Transcoding Router in a specific order. When JWT Validation was inserted after MCP Support and MCP Schema Validation, unauthenticated requests were accepted. Moving JWT Validation ahead of the MCP policies resolved the issue. This demonstrates that policy ordering is significant when combining conventional security policies with the MCP policy stack.

### Troubleshooting

During the initial configuration, JWT Validation failed to initialize because the RSA public key contained an unexpected trailing `%` character.

The gateway logs reported:

```text
RsaPublicKeyParseFailed(
  "Public key parsing error: invalid data:
   Invalid symbol 37, offset 392."
)
```

The `%` character originated from Zsh's end-of-output indicator and was inadvertently included when copying the public key.

Removing the character resolved the parsing error.

> [!NOTE]
> **Finding:** A policy can appear as applied in API Manager even when its configuration fails to initialize on the gateway. Gateway logs should be reviewed when a policy does not behave as expected.

## Authentication Testing

JWT authentication was tested against the Service Desk MCP endpoint using `curl` and the MCP `tools/list` operation.

### Test Request

The following request includes an Employee JWT in the HTTP Authorization header:

```bash
curl -sS -i -X POST "$MCP_URL" \
  -H "Authorization: Bearer $(cat _private/employee.jwt)" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'
```

The `Authorization` header was omitted when testing unauthenticated requests.

### Test Results

| Scenario | HTTP Status | Result |
| --- | --- | --- |
| Missing JWT | 400 Bad Request | Rejected — `JWT Token is required.` |
| Valid Employee JWT | 200 OK | Accepted — MCP tool catalog returned |
| Expired Employee JWT | 401 Unauthorized | Rejected — `Invalid token.` |
| Incorrect audience | 401 Unauthorized | Rejected — `Invalid token.` |

The expired and incorrect-audience JWTs were generated using the same RSA private key as the valid Employee JWT, with their respective claims modified.

### Findings

- Omni Gateway successfully validates locally generated, RS256-signed JWTs using a statically configured RSA public key.
- Requests without a JWT are rejected.
- Expired JWTs and JWTs containing an incorrect audience are rejected.
- JWT Validation returns HTTP 400 for missing tokens and HTTP 401 for invalid tokens.
- Successful JWT authentication alone does not restrict access to individual MCP tools. Tool-level authorization will be implemented separately using MCP Attribute-Based Access Control.

Issuer validation was not configured or tested in the initial implementation.
