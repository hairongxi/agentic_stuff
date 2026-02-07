---
name: contract-clause-parser
description: Parse contract documents and extract clauses with hierarchical path structure. Use when working with Chinese legal contracts or similar documents to: (1) Extract clauses with path identifiers following Linux-style directory format (~ as root), (2) Automatically detect heading styles (traditional Chinese, Arabic numerals, etc.), (3) Map chapter/section/article structure to directory hierarchy, (4) Handle complex clause content including tables, lists, and multi-line text, (5) Output structured JSON with path and clause fields for further processing.
---

# Contract Clause Parser

## Quick Start

Parse a contract document:

```bash
python scripts/parse_contract.py <input.txt> <output.json>
```

**Output format:**
```json
[
  {"path": "~/第一条/1.1", "clause": "1.1 甲方委托乙方建设..."},
  {"path": "~/第一条/1.2", "clause": "1.2 本合同标的总金额为..."}
]
```

## How It Works

The parser:
1. **Detects heading style** from the document (scans first 100 lines)
2. **Builds path hierarchy** mapping chapters/sections/articles to directory levels
3. **Extracts clauses** as terminal nodes in the path tree
4. **Handles complex content** including tables, lists, multi-line paragraphs

## When to Use the Script

Use `scripts/parse_contract.py` for all parsing tasks. The script handles:
- Heading style detection (Chinese numerals, Arabic numbers, traditional legal format)
- Path construction following Linux conventions (~ as root)
- List item recognition within clauses
- Multi-line clause content aggregation

## Supported Heading Styles

The parser automatically detects and handles:
- Traditional legal: 第xx部分/章/节/条
- Chinese numerals: 一、二、三
- Arabic dots: 1. 2. 3. (with subsections 1.1, 1.2, 1.1.1)
- Circled numerals: ①②③ (as terminal clauses)

**For detailed pattern reference**, see [heading_patterns.md](references/heading_patterns.md)

## Path Structure

- Root: `~`
- Hierarchy: Each heading level becomes a directory
- Terminal: Clause content at leaf nodes

**Examples:**
- `~/第一部分/第一章/第一条` - Traditional legal style
- `~/第一章/1.1/1.1.1` - Arabic decimal style
- `~/第一条/1.1` - Mixed style

## Edge Cases

- **Mixed heading styles**: Parser uses dominant style from early document
- **List items**: Treated as part of clause content, not separate clauses
- **Tables/lists**: Included in clause text preservation
- **Empty lines**: Separate clauses, not included in content
