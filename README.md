# MCP Governance

This repository supports hands-on exploration and learning of MuleSoft’s Model Context Protocol (MCP) integration, management, and governance capabilities using MuleSoft MCP Bridge and Anypoint Omni Gateway. Experiments are conducted incrementally to understand product behavior and evaluate capabilities and limitations. Once a set of experiments is complete, technical findings are documented for future reference and reuse.

The experiments use the Brilliant Mule Service Desk API, a simple Spring Boot REST API developed as a reusable reference application for exploring MuleSoft’s agentic capabilities. The application implementation and testing assets are maintained separately in the [service-desk-api](https://github.com/abelisle-mulesoft/service-desk-api) repository.

> [!NOTE]
> Many artifacts and assets in this repository are specific to the Brilliant Mule Service Desk API. However, they can be adapted to work with other APIs to reproduce the same experiments.

## Exploration Scope

This repository supports three areas of exploration:

- **MCP Bridge and Client Integration** - COMPLETED:
  - Exposing REST API operations as MCP tools using MuleSoft MCP Bridge.
  - Configuring MCP tool names, descriptions, and input schemas.
  - Exploring MCP tool discovery and invocation.
  - Integrating MCP-capable AI clients and testing conversational interactions.
  - Documenting MCP Bridge configuration, interoperability observations, and limitations.

- **MCP Management and Governance** - IN PROGRESS:
  - Exploring MCP management and governance policies with Anypoint Omni Gateway.
  - Implementing JWT authentication and persona-based authorization using Cedar policies.
  - Exploring MCP tool access, discovery, and invocation controls.
  - Evaluating MCP data governance, including PII detection, schema validation, and payload optimization.
  - Developing repeatable MCP governance test scenarios.
  - Documenting policy behavior, technical findings, and limitations.

- **MCP Resources and Prompts** - PLANNED:
  - Exploring MCP resources and prompts beyond tool invocation.
  - Understanding resource and prompt discovery and consumption.
  - Evaluating MuleSoft’s management and governance capabilities for MCP resources and prompts.
  - Documenting implementation approaches, findings, and limitations.

## Repository Structure

`api-requests/`
: Reusable Bruno collection containing test scenarios organized by exploration area.

`credentials/`
: Local RSA keys and generated JWTs used for authentication experiments. Generated contents are excluded from Git.

`docs/`
: Documentation covering MCP Bridge, MCP client integration, governance policies, resources and prompts, experiments, and technical findings.

`policies/`
: Cedar authorization policies for different Service Desk personas.

`scripts/`
: Utilities for generating authentication tokens and supporting MCP experiments.

`requirements.txt`
: Python dependencies required by the supporting scripts.

## Prerequisites

Depending on the experiment, the following components and tools are required:

- A running Brilliant Mule Service Desk API.
- MuleSoft MCP Bridge configured to expose selected Service Desk API operations.
- Anypoint Omni Gateway configured to manage the MCP endpoint.
- An MCP-capable client for testing discovery and invocation.
- Bruno for executing repeatable MCP test scenarios.
- Python for running supporting scripts.

## Getting Started

Clone this repository and review the documentation for the exploration area of interest. Each experiment builds on the Brilliant Mule Service Desk API and, where applicable, MuleSoft MCP Bridge and Anypoint Omni Gateway.

## Documentation

The `docs/` directory captures the results of hands-on MCP experiments, including configurations, test scenarios, observations, findings, and limitations.

Documentation is developed incrementally as experiments are completed, with an emphasis on understanding actual product behavior and preserving the knowledge needed to reproduce experiments and demonstrate capabilities.

---

Copyright © 2026 Alan Belisle. Licensed under the [Apache License 2.0](LICENSE.txt).

