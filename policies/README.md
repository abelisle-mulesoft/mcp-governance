# Authorization Policies

This directory contains copies of the Cedar rules used to configure the MCP Attribute-Based Access Control (ABAC) policy during experiments with persona-based access control for MCP tools.

## Policies

| File | Description |
| --- | --- |
| `administrator.cedar` | Grants the Administrator persona access to all configured Service Desk MCP tools. |
| `employee.cedar` | Permits the Employee persona to list, retrieve, and create incidents, and add comments. |
| `support-agent.cedar` | Permits the Support Agent persona to perform Employee operations, assign incidents, and update incidents. |

The Cedar rules are formatted for readability. When configuring the MCP ABAC policy in Anypoint API Manager, the expressions must be entered as single-line strings.

For implementation details, authorization scenarios, and test results, see [MCP Authorization](../docs/mcp-authorization.md).

---

Copyright © 2026 Alan Belisle. Licensed under the [Apache License 2.0](../LICENSE.txt).
