# Heading Patterns Reference

## Style Categories

### 1. Traditional Chinese Style (传统中文风格)

Used in formal Chinese contracts and legal documents.

**Patterns:**
- `第xx部分` - First level (Level 1)
- `第xx章` - Chapter (Level 2)
- `第xx节` - Section (Level 3)
- `第xx条` - Article/Clause (Level 4, terminal)

**Example:**
```
第一部分 总则
第一章 合同目的
第一条 定义
第二条 保密义务
```

### 2. Chinese Numeral Style (中文数字风格)

Common in Chinese contracts using traditional numerals.

**Patterns:**
- `一、` - Level 2
- `二、` - Level 2
- `三、` - Level 2

**Example:**
```
一、项目概况
二、服务内容
三、费用标准
```

### 3. Arabic Dot Style (阿拉伯数字风格)

Modern style using Arabic numbers with dots.

**Patterns:**
- `1.` - Level 2 (for 1-10)
- `2.` - Level 2
- `1.1` - Level 3 (subsection)
- `1.1.1` - Level 4 (subsubsection)

**Example:**
```
1. 项目概述
   1.1 项目背景
      1.1.1 建设目标
2. 技术要求
```

### 4. Circled Numeral Style (圆圈数字风格)

Often used for detailed clauses or sub-items.

**Patterns:**
- `①` - Level 4 (terminal)
- `②` - Level 4 (terminal)
- `③` - Level 4 (terminal)

**Example:**
```
第一条 技术要求
① 系统功能
② 性能指标
③ 安全标准
```

## List Item Patterns

These patterns identify items within a clause, not headings.

**Patterns:**
- `(1)` or `（1）` - Parenthesized number
- `①` `②` `③` - Circled numeral (when not used as heading)
- `1、` `2、` `3、` - Number with Chinese comma

**Example within clause:**
```
1.1 甲方委托乙方建设"绍兴市第一中学智慧教育系统"，该系统包括：
(1) 教学管理系统
(2) 学生信息管理系统
(3) 家长互动平台
乙方应严格按照附件一的要求完成系统的设计、开发、部署、调试、验收及相关服务。
```

## Path Structure

The generated path follows Linux-style directory structure:

```
~                             # Root
├── 第一部分                  # Level 1
│   └── 第一章                # Level 2
│       └── 第一条            # Level 3/4 (terminal)
├── 第二部分
│   └── 第二章
│       └── 2.1               # Level 3 (subsection)
│           └── 2.1.1         # Level 4 (terminal)
```

**Path examples:**
- `~/第一部分/第一章/第一条`
- `~/第一部分/第一章/1.1`
- `~/第一部分/2.1/2.1.1`
- `~/第一条/1.1`

## Detection Logic

The parser:
1. Scans first 100 lines to count heading pattern occurrences
2. Selects the most frequent pattern as the document's style
3. Maintains consistent level mapping throughout the document
4. Treats list items as part of the current clause (not separate clauses)

## Edge Cases

- Mixed styles: Parser uses the dominant style detected in early lines
- Missing levels: Path builds incrementally, may skip levels
- Tables/lists within clauses: Treated as part of clause content
- Empty lines: Separate clauses, not included in clause content
