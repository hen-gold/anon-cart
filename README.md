# Anon Cart - SF Purchase Flow Context

This repository contains context-driven development artifacts for the **SF Purchase Flow (DOM2-6162)** epic, organizing information from multiple sources into structured documentation.

## Overview

- **Epic**: DOM2-6162 - SF Purchase Flow
- **Goal**: Rebuild Storefront purchase flow to create modern, intuitive, scalable purchase experience
- **Status**: 10% complete (4 done, 3 in progress, 4 PR pending, 30 backlog)
- **Type**: Brownfield project (existing codebase)

## Repository Structure

```
anon-cart/
├── conductor/              # Context-driven development artifacts
│   ├── index.md           # Navigation hub
│   ├── product.md         # Product vision and goals
│   ├── product-guidelines.md # Communication standards
│   ├── tech-stack.md      # Technology choices
│   ├── workflow.md        # Development practices
│   ├── tracks.md          # Work unit registry
│   ├── sources/           # Source data organization
│   │   ├── jira/          # Jira epic and issues
│   │   ├── docs/          # Google Docs and Sheets
│   │   ├── bed/           # Backend repository analysis
│   │   └── fed/           # Frontend repository analysis
│   └── tracks/            # Individual track directories
└── README.md              # This file
```

## Sources (Read-Only)

All sources are read-only. This repository only contains documentation extracted from:

- **BED Repository**: [premium-server/premium-cart](https://github.com/wix-private/premium/blob/6f4fed7906410a9b9d7c05e782dbba67dbabec5a/premium-server/premium-cart)
- **FED Repository**: [premium-cart-anonymous](https://github.com/wix-private/premium-cart-anonymous)
- **Jira Epic**: [DOM2-6162](https://wix.atlassian.net/browse/DOM2-6162)
- **Master Document**: [Domains Storefront Cart - Master Document](https://docs.google.com/document/d/1WaJH6C4jCMAqGaF-UoUGPFtkieWxfASaTZBMRUfi0mM/edit)
- **Dependencies**: [Dependencies Spreadsheet](https://docs.google.com/spreadsheets/d/1DugSrwbNke5ExpA201Tp_IdQeb715DxKrf2gR8ltmSc/edit)
- **Slack Channel**: [Team Communication Channel](https://wix.slack.com/archives/C0A6AMMMTFY) - Main team communication channel (Channel ID: C0A6AMMMTFY)

## Getting Started

1. Navigate to [conductor/index.md](conductor/index.md) for an overview of all artifacts
2. Review [conductor/product.md](conductor/product.md) for product vision
3. Check [conductor/tracks.md](conductor/tracks.md) for work unit registry

## Context-Driven Development

This repository follows the [Context-Driven Development](https://github.com/wshobson/agents) methodology, treating project context as a first-class artifact managed alongside code.
