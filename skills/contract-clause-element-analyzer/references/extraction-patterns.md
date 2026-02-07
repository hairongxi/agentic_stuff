# Key-Value Extraction Patterns

## Overview

This guide provides patterns and examples for extracting key-value pairs from contract clauses.

## General Extraction Principles

1. **Identify the topic**: What is this clause about?
2. **Extract measurable values**: Dates, amounts, percentages, quantities
3. **Use clear key names**: Specific and descriptive (not generic like "value")
4. **Source attribution**: Include brief original text reference
5. **Multiple values**: If clause has multiple key-value pairs, extract all

## 1. 基本信息 (Basic Info)

### Contract Parties

**Clause**: 甲方：XX公司，乙方：YY有限公司

**Output**:
```markdown
### 合同主体
甲方: XX公司
乙方: YY有限公司
出处：甲方：XX公司
```

### Contract Date

**Clause**: 本合同于2024年1月1日签订

**Output**:
```markdown
### 签订日期
签订日期: 2024-01-01
出处：本合同于2024年1月1日
```

## 2. 商法 (Commercial Law)

### Contract Validity

**Clause**: 本合同有效期为【1】年，自签订之日起计算

**Output**:
```markdown
### 合同有效期
有效期: 1
单位: 年
出处：本合同有效期为【1】年
```

### Breach Penalty

**Clause**: 如乙方逾期交货，每逾期一日需支付违约金【500】元

**Output**:
```markdown
### 逾期违约金
每日违约金: 500
单位: 元
出处：如乙方逾期交货
```

### Dispute Resolution

**Clause**: 双方发生争议时，应提交【北京市】人民法院解决

**Output**:
```markdown
### 争议解决
管辖地: 北京市
出处：应提交【北京市】人民法院解决
```

## 3. 交付 (Delivery)

### Delivery Timeline

**Clause**: 乙方应在合同签订后【15】天内完成交货

**Output**:
```markdown
### 交货日期
交货日期: 15
单位: 天
出处：乙方应在合同签订后【15】天内完成交货
```

### Delivery Location

**Clause**: 货物应送达至甲方指定的【上海市浦东新区XX路XX号】

**Output**:
```markdown
### 交货地点
交货地点: 上海市浦东新区XX路XX号
出处：货物应送达至甲方指定的
```

### Quantity

**Clause**: 货物数量为【1000】件，每件规格为【50cm × 30cm × 20cm】

**Output**:
```markdown
### 货物数量
数量: 1000
单位: 件
规格: 50cm × 30cm × 20cm
出处：货物数量为【1000】件
```

## 4. 财经 (Finance)

### Total Amount

**Clause**: 本合同总金额为人民币【50,000】元整

**Output**:
```markdown
### 合同总金额
合同总金额: 50,000
单位: 元
出处：本合同总金额为人民币【50,000】元
```

### Payment Milestones

**Clause**: 合同签订后【3】日内支付【30%】预付款，交货验收合格后支付剩余【70%】

**Output**:
```markdown
### 付款里程碑
预付款比例: 30%
预付款期限: 3
尾款比例: 70%
付款条件: 交货验收合格
出处：合同签订后【3】日内支付【30%】预付款
```

### Payment Method

**Clause**: 付款方式为银行转账，账户信息：【6222 XXXX XXXX XXXX XXXX】

**Output**:
```markdown
### 付款方式
付款方式: 银行转账
账号: 6222 XXXX XXXX XXXX XXXX
出处：付款方式为银行转账
```

## 5. 附件 (Attachments)

### Attached Documents

**Clause**: 本合同附件包括：附件1-产品规格书，附件2-验收标准

**Output**:
```markdown
### 合同附件
附件1: 产品规格书
附件2: 验收标准
出处：本合同附件包括
```

## Special Patterns

### Date Formats

**Clause**: 2024年3月15日前完成

**Output**:
```markdown
### 完成日期
完成日期: 2024-03-15
出处：2024年3月15日前完成
```

### Percentage with Amount

**Clause**: 预付款为合同总额的【30%】，即【15,000】元

**Output**:
```markdown
### 预付款
预付款比例: 30%
预付款金额: 15,000
单位: 元
出处：预付款为合同总额的【30%】
```

### Multiple Key-Values in One Clause

**Clause**: 合同编号：【HT-2024-001】，签订日期：【2024-01-15】，总金额：【100,000】元

**Output**:
```markdown
### 基本信息汇总
合同编号: HT-2024-001
签订日期: 2024-01-15
总金额: 100,000
单位: 元
出处：合同编号：【HT-2024-001】
```

## Extraction Tips

1. **Bracket indicators**: Content in 【】 brackets is typically a value to extract
2. **Context preservation**: Keep "出处" (source) text minimal but identifiable
3. **Unit specification**: Always include units when applicable (元, 天, %, 件, etc.)
4. **Date normalization**: Convert date formats to consistent format (YYYY-MM-DD)
5. **Amount formatting**: Preserve original formatting with commas, remove currency symbols in value
6. **Topic naming**: Use clear, descriptive topic names based on clause content
7. **Split long clauses**: If clause contains distinct topics, split into multiple entries

## Common Key Names

| Category | Common Key Names |
|----------|-----------------|
| 基本信息 | 合同编号, 甲方, 乙方, 签订日期, 有效期 |
| 商法 | 违约金, 管辖地, 争议解决, 不可抗力, 终止条件 |
| 交付 | 交货日期, 交货地点, 数量, 规格, 验收标准 |
| 财经 | 合同金额, 预付款比例, 付款里程碑, 付款方式, 账号 |
| 附件 | 附件名称, 附录内容, 补充文档 |
