# Contract Module Detection Patterns

## Module Recognition Patterns

### 1. 封面

**Start Indicators:**
- Document starts with title in large font or centered
- Lines containing: "合同"、"协议书"、"协议" followed by title
- Contract number patterns: "编号："、"No."、"合同编号："
- Party information: "甲方："、"乙方："、"买方："、"卖方："
- Date formats: "日期："、"签订日期："、"签署日期："
- Location: "地点："、"签署地点："

**End Indicators:**
- Blank line before main content
- "目录" section start
- "第一条" or "Chapter 1" start

**Content Characteristics:**
- Typically 1-2 pages
- Contains metadata not part of main terms
- May include: contract type, number, parties, dates, location, currency

---

### 2. 目录

**Start Indicators:**
- Line containing: "目录"、"目 录"、"TABLE OF CONTENTS"、"CONTENTS"
- Often centered or in special formatting
- May be followed by dotted lines and page numbers

**End Indicators:**
- Blank line before main content
- "第一条" or "Chapter 1" start
- "第一章" start

**Content Characteristics:**
- Lists chapter/section titles with page numbers
- Structure: "第一章 xxx...x", "1.1 xxx...x", "附件一 xxx...x"
- May span multiple pages for long contracts

---

### 3. 序言

**Start Indicators:**
- Phrases indicating background:
  - "鉴于"
  - "WHEREAS"
  - "为了"
  - "兹就"
  - "根据"
  - "依据"
- May include "背景"、"前言" section titles

**End Indicators:**
- First clause start: "第一条"、"Article 1"、"1."
- "第一章" start
- Statement: "双方达成如下协议："、"Both parties agree as follows:"

**Content Characteristics:**
- Explains why contract is being made
- Describes relationship between parties
- States purpose and objectives
- No numbered clauses typically

---

### 4. 正文

**Start Indicators:**
- First numbered clause:
  - "第一条"
  - "Article 1"
  - "1."
  - "Chapter 1"
  - "第一章"
  - "第一条："
- May start with "本合同条款如下：" preceding numbered sections

**End Indicators:**
- Signature section markers:
  - "甲方（盖章）："
  - "乙方（盖章）："
  - "签字："
  - "签署："
  - "SIGNATURE"
- Attachment markers:
  - "附件"
  - "ANNEX"
  - "APPENDIX"
  - "附件一"
- Concluding phrases:
  - "本合同一式"
  - "本合同自"
  - "本协议未尽事宜"

**Content Characteristics:**
- Hierarchical structure: 章 -> 节 -> 条 -> 款
- Numbered clauses throughout
- Contains substantive terms and conditions
- May include: definitions, obligations, rights, termination, breach, etc.

---

### 5. 盖章签字

**Start Indicators:**
- Party signature areas:
  - "甲方："
  - "乙方："
  - "甲方（盖章）："
  - "乙方（盖章）："
  - "Authorized Representative:"
  - "授权代表："
- Section titles:
  - "签字盖章页"
  - "签署页"
  - "SIGNATURE PAGE"
  - "授权签字"

**End Indicators:**
- End of document
- Next attachment section start
- Page break followed by "附件" or "ANNEX"

**Content Characteristics:**
- Party names and signature areas
- Date lines: "日期："、"Date："
- May include: company seal area, representative signature, date
- Often blank in printed drafts

---

### 6. 附件

**Start Indicators:**
- Attachment markers:
  - "附件"
  - "附件一"
  - "附件1"
  - "ANNEX"
  - "ANNEX 1"
  - "APPENDIX"
  - "APPENDIX A"
  - "附件A"
- May appear in main body as references: "见附件一"

**End Indicators:**
- Next attachment marker
- End of document

**Content Characteristics:**
- Each attachment is a separate module
- Supplements main contract body
- May include: technical specifications, schedules, forms, additional terms
- Typically labeled as: 附件一、附件二、Attachment A、Attachment B

---

## Boundary Detection Strategy

### Sequential Analysis

1. **Top-down approach**: Scan from beginning to identify module order
2. **Pattern matching**: Use multiple indicators (not just one) for reliability
3. **Context awareness**: Consider surrounding text to validate boundaries
4. **Fallback rules**: When patterns are ambiguous, use heuristics based on typical contract structure

### Common Ambiguities

**封面 vs 正文 start**:
- If no clear cover, look for first numbered clause as 正文 start
- Document beginning with 第一章 indicates no separate 封面

**序言 vs 正文 start**:
- 序言 contains background context (鉴于, 为了, etc.)
- 正文 starts with numbered clauses or substantive terms

**正文 end vs 签字页 start**:
- Look for signature indicators in final pages
- Check for concluding phrases before signatures
- Multiple signature blocks indicate 签字页

**Multiple attachments**:
- Each "附件" marker starts new module
- Include all content between markers

### Confidence Levels

**High confidence** (use as primary boundary):
- Clear section headers with standard formatting
- Multiple pattern matches (e.g., both "甲方（盖章）：" and "乙方（盖章）：" present)
- Page breaks combined with section markers

**Medium confidence** (use with supporting indicators):
- Single pattern match
- Phrases that could appear in multiple contexts
- Unusual formatting

**Low confidence** (require additional context):
- Ambiguous markers
- Non-standard terminology
- Conflicting indicators

When low confidence, examine:
- Paragraph structure
- Content characteristics
- Typical contract flow
