import re
import json
from typing import List, Dict, Tuple, Optional
from pathlib import Path


class ContractParser:
    def __init__(self):
        self.heading_patterns = [
            # Markdown格式 ## 第一条
            (re.compile(r'^##\s*(第[一二三四五六七八九十百千万\d]+[部分章节条])'), 'part'),
            # 第xx部分/章/节/条
            (re.compile(r'^(第[一二三四五六七八九十百千万\d]+[部分章节条])'), 'part'),
            # 中文数字 一、二、三、
            (re.compile(r'^([一二三四五六七八九十]+、)'), 'chinese_num'),
            # 阿拉伯数字 1. 2. 3.
            (re.compile(r'^(\d+\.)(?!\d)'), 'arabic_dot'),
            # 圆圈数字 ①②③
            (re.compile(r'^([①②③④⑤⑥⑦⑧⑨⑩]+)'), 'circled_num'),
            # 小节 1.1 1.2 1.3
            (re.compile(r'^(\d+\.\d+)(?!\d)'), 'subsection'),
            # 更深层次 1.1.1 1.1.2
            (re.compile(r'^(\d+\.\d+\.\d+)(?!\d)'), 'subsubsection'),
        ]
        
        self.list_patterns = [
            re.compile(r'^(\s*[(（][一二三四五六七八九十\d]+[)）])'),
            re.compile(r'^(\s*[①②③④⑤⑥⑦⑧⑨⑩]+)'),
            re.compile(r'^(\s*\d+[、.])'),
        ]
        
        self.style_detected = None
        self.root_path = "~"
    
    def detect_style(self, lines: List[str]) -> str:
        style_counts = {}
        
        for line in lines[:100]:
            if not line.strip():
                continue
            
            for pattern, style_name in self.heading_patterns:
                if pattern.match(line):
                    weight = 1
                    if style_name == 'part':
                        weight = 5
                    elif style_name in ['chinese_num', 'arabic_dot']:
                        weight = 3
                    style_counts[style_name] = style_counts.get(style_name, 0) + weight
                    break
        
        if not style_counts:
            return 'unknown'
        
        return max(style_counts.items(), key=lambda x: x[1])[0]
    
    def get_heading_level(self, line: str) -> Optional[Tuple[int, str]]:
        for pattern, style_name in self.heading_patterns:
            match = pattern.match(line)
            if match:
                heading_text = match.group(1)
                
                if style_name == 'part':
                    if '部分' in heading_text:
                        return (1, heading_text)
                    elif '章' in heading_text:
                        return (2, heading_text)
                    elif '节' in heading_text:
                        return (3, heading_text)
                    elif '条' in heading_text:
                        return (1, heading_text)
                
                elif style_name == 'chinese_num':
                    return (2, heading_text)
                
                elif style_name == 'arabic_dot':
                    num = int(heading_text.rstrip('.'))
                    if num <= 10:
                        return (2, heading_text)
                    else:
                        return (3, heading_text)
                
                elif style_name == 'subsection':
                    return (2, heading_text)
                
                elif style_name == 'subsubsection':
                    return (3, heading_text)
                
                elif style_name == 'circled_num':
                    return (3, heading_text)
        
        return None
    
    def is_list_item(self, line: str) -> bool:
        for pattern in self.list_patterns:
            if pattern.match(line):
                return True
        return False
    
    def parse(self, input_file: str, output_file: str) -> None:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        self.style_detected = self.detect_style(lines)
        
        result = []
        current_path = []
        current_clause_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            if not stripped:
                continue
            
            heading_info = self.get_heading_level(stripped)
            
            if heading_info:
                level, heading = heading_info
                
                if current_clause_lines:
                    clause_text = '\n'.join(current_clause_lines).strip()
                    clause_text = clause_text.lstrip('#').lstrip()
                    if clause_text:
                        path_str = '/'.join([self.root_path] + current_path)
                        result.append({
                            "path": path_str,
                            "clause": clause_text
                        })
                    current_clause_lines = []
                
                if len(current_path) >= level:
                    current_path = current_path[:level-1]
                
                current_path.append(heading)
                current_clause_lines.append(line)
            elif current_path:
                current_clause_lines.append(line)
        
        if current_clause_lines:
            clause_text = '\n'.join(current_clause_lines).strip()
            clause_text = clause_text.lstrip('#').lstrip()
            if clause_text:
                path_str = '/'.join([self.root_path] + current_path)
                result.append({
                    "path": path_str,
                    "clause": clause_text
                })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)


def main():
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python parse_contract.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    parser = ContractParser()
    parser.parse(input_file, output_file)
    print("Contract parsed successfully.")


if __name__ == "__main__":
    main()
