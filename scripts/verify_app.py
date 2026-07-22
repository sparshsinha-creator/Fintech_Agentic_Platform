"""Verify application startup and route registration."""

from app.main import app

openapi = app.openapi()
print("OpenAPI paths:")
for path in sorted(openapi["paths"].keys()):
    methods = list(openapi["paths"][path].keys())
    print(f"  {methods} {path}")

total = sum(len(v) for v in openapi["paths"].values())
print(f"Total endpoints: {total}")
