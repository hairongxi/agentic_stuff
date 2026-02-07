---
name: contract-module-extractor
description: Sequentially decompose plain text contracts into modular components with precise boundary detection. Use when Claude needs to analyze contract text files and extract structured modules including: 封面, 目录, 序言, 正文, 盖章签字, and 附件. The skill identifies module boundaries based on content patterns, handles variable module ordering, and outputs JSON format. Supports custom reference patterns for different industries and contract types.
---

# Contract Module Extractor

## Overview

Decompose plain text contracts into sequential modules by analyzing content patterns and determining precise boundaries between sections.

## Module Types

1. **封面**: Contract title, number, parties, dates (optional)
2. **目录**: Table of contents for navigation (optional)
3. **序言**: Background information about contract establishment (optional)
4. **正文**: Tree structure of chapters/sections with clauses (required)
5. **盖章签字**: Party signatures and dates (optional)
6. **附件**: Supplementary content to contract body, may contain multiple attachments (optional)

## Workflow

1. Load contract text file
2. Scan to identify approximate module structure
3. Analyze each module's characteristics to determine precise boundaries
4. Output JSON array of modules with type and text

## Custom Reference Patterns

For industry-specific contract formats, customize patterns in `references/patterns.md`:
- Module start/end markers
- Typical terminology and phrasing
- Industry-specific section headers

Load reference patterns when analyzing non-standard contracts.

## Reference Files

- `references/patterns.md`: Default module detection patterns
- `references/examples.md`: Example contract structures for reference

Load these files when encountering ambiguous module boundaries or unusual contract formats.
