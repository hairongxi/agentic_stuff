---
name: contract-analyzer
description: "Analyze contract documents and extract clause elements by orchestrating multiple specialized skills. Use when Claude needs to process contract files (.docx, .pdf, or already-extracted .txt) to extract structured information through a multi-stage pipeline: 1) Convert document to text if needed using docx or pdf skill, 2) Extract document modules using contract-module-extractor skill, 3) Parse contract clauses using contract-clause-parser skill, 4) Analyze clause elements using contract-clause-element-analyzer skill. The workflow produces sequential output files: *-plaintext.txt, *-modules.json, *-clauses.json, *-elements.json."
---

# Contract Analyzer

## Overview

Analyze contract documents through a structured pipeline that extracts hierarchical information from raw documents to structured clause elements. This skill orchestrates multiple specialized skills to transform contracts into structured data.

## Workflow

Follow this sequential pipeline to analyze a contract:

### Step 1: Convert to Plaintext (if needed)

Determine the input file format:

**If input is .docx or .pdf:**
- Call the appropriate skill to extract text:
  - For .docx files: Use `docx` skill to extract text
  - For .pdf files: Use `pdf` skill to extract text
- Save output as `<original-filename>-plaintext.txt`

**If input is already .txt:**
- Proceed to Step 2 directly
- No conversion needed

### Step 2: Extract Document Modules

- Call `contract-module-extractor` skill with the plaintext file
- Input: `<filename>-plaintext.txt`
- Output: `<filename>-modules.json`

This step decomposes the contract into structural modules:
- Cover (封面)
- Preamble (序言)
- Body (正文)
- Attachments (附件)
- Other sections

### Step 3: Parse Contract Clauses

- Call `contract-clause-parser` skill with the modules JSON file
- Input: `<filename>-modules.json`
- Output: `<filename>-clauses.json`

This step normalizes clauses from the body section, extracting:
- Hierarchical path structure (Linux-style directory format)
- Clause content with metadata
- Handling of tables, lists, and multi-line text

### Step 4: Analyze Clause Elements

- Call `contract-clause-element-analyzer` skill with the clauses JSON file
- Input: `<filename>-clauses.json`
- Output: `<filename>-elements.json`

This step analyzes each clause and extracts key-value pairs across categories:
- 基本信息 (Basic Info)
- 商法 (Commercial Law)
- 交付 (Delivery)
- 财经 (Finance)
- 附件 (Attachments)

## Output Files

The pipeline generates these sequential files:

1. `*-plaintext.txt` - Raw contract text (if converted from docx/pdf)
2. `*-modules.json` - Structural decomposition of the document
3. `*-clauses.json` - Normalized clause structure with paths
4. `*-elements.json` - Extracted key-value elements from clauses

## Error Handling

- If a step fails, stop the pipeline and report the error
- Verify each output file exists before proceeding to the next step
- Validate JSON structure before passing to next skill
- All intermediate files are preserved for debugging

## When to Use This Skill

Use this skill when:
- User asks to "analyze a contract"
- User needs to "extract clauses" from a contract
- User wants to "get contract elements" or "contract key-value pairs"
- User provides a contract file (.docx, .pdf, or .txt) and asks for structured analysis
- User asks to process contracts for clause extraction or element analysis
