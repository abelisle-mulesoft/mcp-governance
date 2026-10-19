#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt

ROOT = Path(__file__).resolve().parent.parent
PRIVATE_KEY = ROOT / "credentials" / "private.pem"

ISSUER = "brilliant-mule"
AUDIENCE = "brilliant-mule-service-desk"

PERSONAS = {
    "employee": "employee001",
    "support-agent": "support001",
    "administrator": "admin001",
}


def generate_token(persona, wrong_audience=False, expired=False):
    now = datetime.now(timezone.utc)

    claims = {
        "sub": PERSONAS[persona],
        "iss": ISSUER,
        "aud": "invalid-audience" if wrong_audience else AUDIENCE,
        "roles": [persona],
        "iat": now - timedelta(hours=2) if expired else now,
        "exp": now - timedelta(hours=1) if expired else now + timedelta(hours=1),
    }

    private_key = PRIVATE_KEY.read_bytes()

    return jwt.encode(
        claims,
        private_key,
        algorithm="RS256",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a signed JWT for an MCP persona."
    )
    parser.add_argument(
        "persona",
        choices=PERSONAS.keys(),
        help="Persona for which to generate a JWT.",
    )
    test_options = parser.add_mutually_exclusive_group()
    test_options.add_argument(
        "--wrong-audience",
        action="store_true",
        help="Generate a JWT with an incorrect audience for negative testing.",
    )
    test_options.add_argument(
        "--expired",
        action="store_true",
        help="Generate an already-expired JWT for negative testing.",
    )

    args = parser.parse_args()
    print(generate_token(args.persona, args.wrong_audience, args.expired))
