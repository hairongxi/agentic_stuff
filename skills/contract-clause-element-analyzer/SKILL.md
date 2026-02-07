---
name: contract-clause-element-analyzer
description: Analyze business contract clauses and extract key elements into structured key-value format. Use when Claude needs to analyze contract text files (.txt) and transform them into structured markdown with clause topics and key-value pairs. Supports five main categories: 基本信息 (Basic Info), 商法 (Commercial Law), 交付 (Delivery), 财经 (Finance), and 附件 (Attachments). Each clause is analyzed to identify its topic and extract relevant key-value pairs (e.g., payment milestones with date/percentage pairs), including the supported clauses.
---

# Contract Analyzer

## Workflow

1. **Read input file**: User provides a text file containing contract content
2. **Analyze clauses**: Identify individual clauses in the contract
3. **Categorize each clause**: Determine which category the clause belongs to:
   - 基本信息 (Basic Info)
   - 商法 (Commercial Law)
   - 交付 (Delivery)
   - 财经 (Finance)
   - 附件 (Attachments)
4. **Extract key-value pairs and supported clauses**: For each clause, identify the topic and extract relevant key-value pairs and supported clauses.
5. **Generate markdown output**: Format results as markdown with structure:
   ```markdown
   ### [Clause Topic]
   [Key]: [Value]
   出处：[Original text snippet]
   ```

## Clause Categorization

For detailed categorization rules and examples, see [references/clause-categories.md](references/clause-categories.md).

## Key-Value Extraction Patterns

For specific patterns and examples of key-value extraction for different clause types, see [references/extraction-patterns.md](references/extraction-patterns.md).

## Output Format

Generate markdown output with:
- H3 headings for clause topics
- Key-value pairs in format `[Key]: [Value]`
- Source attribution: `出处：[Original text]`
- Group by chapter category when possible
- For complete contract analysis, organize by section/numbering

**Complete Contract Output Example:**
```markdown
# 合同关键信息分析

## 基本信息

### 合同主体
甲方: XX公司
乙方: YY有限公司
出处：甲方：XX公司

### 签订日期
签订日期: 2024-01-01
出处：本合同于2024年1月1日

## 交付

### 交货日期
交货日期: 15
单位: 天
出处：乙方应在合同签订后【15】天内

## 财经

### 合同总金额
合同总金额: 50,000
单位: 元
出处：本合同总金额为人民币【50,000】元
```

## Example

**Input Clause:**
```
4.交货日期：乙方应在合同签订后【15】天内完成交货，并附上双方约定的、记录货物相关事项的资料。
```

**Output:**
```markdown
### 交货日期
交货日期: 15
单位: 天
出处：乙方应在合同签订后
```

## Tips

- Use bracketed content 【】 as key indicators for values
- Identify clause topics from section headers or main subjects
- Extract dates, percentages, amounts, and other measurable values as keys
- Keep source attribution concise but identifiable
- When clause spans multiple topics, split into multiple entries
