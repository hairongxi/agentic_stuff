#!/usr/bin/env python3
"""
Contract Module Extractor
Decomposes plain text contracts into modular components.
"""

import re
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Module:
    """Represents a contract module with type and content."""
    type: str
    text: str
    start_line: int
    end_line: int


class ContractModuleExtractor:
    """Extracts modules from contract text based on pattern recognition."""

    def __init__(self, text: str):
        self.text = text
        self.lines = text.split('\n')
        self.modules: List[Module] = []

    def extract(self) -> List[Dict]:
        """Extract all modules and return as JSON-compatible list."""
        self._scan_structure()
        self._determine_boundaries()
        return self._to_json()

    def _scan_structure(self) -> None:
        """Scan contract to identify approximate module structure."""
        self.potential_boundaries = []

        for i, line in enumerate(self.lines):
            stripped = line.strip()

            if not stripped:
                continue

            # Detect module starts based on content patterns
            module_type = self._detect_module_type(stripped, i)
            if module_type:
                self.potential_boundaries.append((i, module_type))

    def _detect_module_type(self, line: str, line_num: int) -> Optional[str]:
        """Detect module type for a given line."""
        # TOC (Table of Contents) - only first line
        toc_patterns = [
            r'^目录\s*$',
            r'^目\s*录\s*$',
            r'^TABLE OF CONTENTS\s*$',
            r'^CONTENTS\s*$',
        ]
        for pattern in toc_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                return '目录'

        # Preamble start
        preamble_patterns = [
            r'^鉴于',
            r'^WHEREAS',
            r'^为了',
            r'^兹就',
            r'^根据',
            r'^依据',
        ]
        for pattern in preamble_patterns:
            if re.match(pattern, line):
                return '序言'

        # Body start (first chapter/section) - but exclude TOC entries
        body_patterns = [
            r'^第[一二三四五六七八九十百]+章',
            r'^第[一二三四五六七八九十百]+条',
            r'^Chapter\s+\d+',
            r'^Article\s+\d+',
        ]
        for pattern in body_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                # Check if this is a TOC entry (followed by dotted line pattern)
                # If line itself contains dotted pattern, it's likely TOC
                if re.search(r'\.{3,}\s*\d+$', line):
                    continue
                # Check if next few lines have TOC pattern
                if line_num + 1 < len(self.lines):
                    next_lines = '\n'.join(self.lines[line_num:line_num+5])
                    if re.search(r'\.{3,}\s*\d+', next_lines):
                        continue

                # Only return if this is the first chapter (avoid treating every chapter as new module)
                if not self.potential_boundaries:
                    return '正文'
                # Check if previous boundary is not also 正文
                if self.potential_boundaries and self.potential_boundaries[-1][1] != '正文':
                    return '正文'

        # Signature start
        signature_patterns = [
            r'^甲方.*[盖章签字签署][:：]',
            r'^乙方.*[盖章签字签署][:：]',
            r'^Party\s*A.*[Signature签字][:：]',
            r'^Party\s*B.*[Signature签字][:：]',
            r'^签字盖章页',
            r'^签署页',
            r'^SIGNATURE\s*PAGE',
        ]
        for pattern in signature_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                return '盖章签字'

        # Attachment start - but exclude TOC entries (lines with dots and page numbers)
        # True attachments usually stand alone and have more content below
        if not re.match(r'^.{1,50}\.{3,}\s*\d+$', line):  # Not a TOC entry
            attachment_patterns = [
                r'^附件[一二三四五六七八九十百0-9]+[\.、:\s]*',
                r'^附件[一二三四五六七八九十百0-9]+\s*[A-Z]*',
                r'^ANNEX\s*\d+',
                r'^APPENDIX\s*\d+',
            ]
            for pattern in attachment_patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    return '附件'

        return None

    def _determine_boundaries(self) -> None:
        """Determine precise boundaries between modules."""
        if not hasattr(self, 'potential_boundaries'):
            self.potential_boundaries = []

        # Sort boundaries by line number
        self.potential_boundaries.sort(key=lambda x: x[0])

        if not self.potential_boundaries:
            # No clear boundaries, try to classify entire document
            content = '\n'.join(self.lines).strip()
            if content:
                module_type = self._classify_module(content, 0, len(self.lines) - 1)
                self.modules.append(Module(
                    type=module_type or '正文',
                    text=content,
                    start_line=0,
                    end_line=len(self.lines) - 1
                ))
            return

        # Find key marker positions
        markers = {
            'toc': None,
            'preamble': None,
            'body': None,
            'signature': None,
            'attachments': []
        }

        for line_num, module_type in self.potential_boundaries:
            if module_type == '目录' and markers['toc'] is None:
                markers['toc'] = line_num
            elif module_type == '序言' and markers['preamble'] is None:
                markers['preamble'] = line_num
            elif module_type == '正文' and markers['body'] is None:
                markers['body'] = line_num
            elif module_type == '盖章签字' and markers['signature'] is None:
                markers['signature'] = line_num
            elif module_type == '附件':
                markers['attachments'].append(line_num)

        # Determine module boundaries
        current_pos = 0
        total_lines = len(self.lines)

        # 封面: from start to first module marker (if any)
        first_marker = min([m for m in [markers['toc'], markers['preamble'], markers['body']] if m is not None], default=None)
        if first_marker and first_marker > current_pos:
            content = '\n'.join(self.lines[current_pos:first_marker]).strip()
            if content:
                self.modules.append(Module(
                    type='封面',
                    text=content,
                    start_line=current_pos,
                    end_line=first_marker - 1
                ))
            current_pos = first_marker

        # 目录: from toc marker to next marker
        if markers['toc'] is not None and markers['toc'] >= current_pos:
            next_marker = markers['preamble'] or markers['body'] or markers['signature'] or markers['attachments'][0] if markers['attachments'] else None
            if next_marker is None:
                next_marker = total_lines
            content = '\n'.join(self.lines[markers['toc']:next_marker]).strip()
            if content:
                self.modules.append(Module(
                    type='目录',
                    text=content,
                    start_line=markers['toc'],
                    end_line=next_marker - 1
                ))
            current_pos = next_marker

        # 序言: from preamble marker to body marker
        if markers['preamble'] is not None and markers['preamble'] >= current_pos:
            next_marker = markers['body'] or markers['signature'] or markers['attachments'][0] if markers['attachments'] else None
            if next_marker is None:
                next_marker = total_lines
            content = '\n'.join(self.lines[markers['preamble']:next_marker]).strip()
            if content:
                self.modules.append(Module(
                    type='序言',
                    text=content,
                    start_line=markers['preamble'],
                    end_line=next_marker - 1
                ))
            current_pos = next_marker

        # 正文: from body marker to signature or attachments
        if markers['body'] is not None and markers['body'] >= current_pos:
            # Determine where body ends
            body_end = None

            # Search limit
            if markers['attachments']:
                search_limit = markers['attachments'][0]
            else:
                search_limit = total_lines

            # Look for signature patterns in body section (more comprehensive search)
            for i in range(markers['body'], search_limit):
                line = self.lines[i].strip()
                # Strong signature indicators
                if re.match(r'^甲方.*[盖章签字签署][:：]', line) or \
                   re.match(r'^乙方.*[盖章签字签署][:：]', line):
                    body_end = i
                    break
                # Additional signature patterns
                if '甲方（盖章）' in line or '乙方（盖章）' in line:
                    body_end = i
                    break
                # Look for signature page markers
                if line.startswith('签字盖章页') or line.startswith('签署页'):
                    body_end = i
                    break

            # If no signature found, body goes to first attachment or end
            if not body_end:
                if markers['attachments']:
                    body_end = markers['attachments'][0]
                else:
                    body_end = total_lines

            # Extract body content
            body_content = '\n'.join(self.lines[markers['body']:body_end]).strip()
            if body_content:
                self.modules.append(Module(
                    type='正文',
                    text=body_content,
                    start_line=markers['body'],
                    end_line=body_end - 1
                ))
            current_pos = body_end

        # 盖章签字: extract if signature section exists
        signature_end = markers['attachments'][0] if markers['attachments'] else None
        if not signature_end:
            signature_end = total_lines

        if signature_end > current_pos:
            # Check if there's signature content
            has_signature = False
            sig_start = current_pos

            for i in range(current_pos, signature_end):
                line = self.lines[i].strip()
                # Strong signature indicators
                if re.match(r'^甲方.*[盖章签字签署][:：]', line) or \
                   re.match(r'^乙方.*[盖章签字签署][:：]', line):
                    has_signature = True
                    if sig_start == current_pos:  # Update start if not set
                        sig_start = i
                    break
                # Additional patterns
                if '甲方（盖章）' in line or '乙方（盖章）' in line:
                    has_signature = True
                    if sig_start == current_pos:
                        sig_start = i
                    break
                if '签字' in line or '签署' in line or '盖章' in line:
                    has_signature = True
                    if sig_start == current_pos:
                        sig_start = i
                    break

            if has_signature:
                sig_content = '\n'.join(self.lines[sig_start:signature_end]).strip()
                if sig_content:
                    self.modules.append(Module(
                        type='盖章签字',
                        text=sig_content,
                        start_line=sig_start,
                        end_line=signature_end - 1
                    ))
                current_pos = signature_end

        # 附件: each attachment
        for i, attachment_line in enumerate(markers['attachments']):
            if attachment_line >= current_pos:
                next_attachment = markers['attachments'][i + 1] if i + 1 < len(markers['attachments']) else None
                next_marker = next_attachment or total_lines
                content = '\n'.join(self.lines[attachment_line:next_marker]).strip()
                if content:
                    self.modules.append(Module(
                        type='附件',
                        text=content,
                        start_line=attachment_line,
                        end_line=next_marker - 1
                    ))
                current_pos = next_marker

    def _classify_module(self, content: str, start_line: int, end_line: int) -> Optional[str]:
        """Classify content into a module type."""
        if not content.strip():
            return None

        lines = content.split('\n')
        line_count = len([l for l in lines if l.strip()])

        # Check for TOC patterns (lines with dots and page numbers)
        if re.search(r'^.{1,50}\.{3,}\s*\d+$', content, re.MULTILINE):
            return '目录'

        # Check for 序言 patterns
        preamble_patterns = [r'^鉴于', r'^WHEREAS', r'^为了', r'^兹就', r'^根据', r'^依据', r'^背景', r'^前言']
        for line in lines[:5]:
            for pattern in preamble_patterns:
                if re.match(pattern, line.strip(), re.IGNORECASE):
                    return '序言'

        # Check for 盖章签字 patterns
        signature_patterns = [
            r'^甲方.*[盖章签字签署][:：]',
            r'^乙方.*[盖章签字签署][:：]',
            r'^Party\s*A.*[Signature签字][:：]',
            r'^Party\s*B.*[Signature签字][:：]',
            r'^授权代表',
            r'^Authorized\s*Representative',
            r'^签字盖章页',
            r'^签署页',
            r'^SIGNATURE\s*PAGE',
        ]
        for pattern in signature_patterns:
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                return '盖章签字'

        # Check for 附件 patterns
        attachment_patterns = [
            r'^附件[一二三四五六七八九十百0-9]+[\.、:\s]*',
            r'^附件[一二三四五六七八九十百0-9]+\s*[A-Z]*',
            r'^ANNEX\s*\d+',
            r'^APPENDIX\s*\d+',
        ]
        for line in lines[:3]:
            for pattern in attachment_patterns:
                if re.match(pattern, line.strip(), re.IGNORECASE):
                    return '附件'

        # Check for 正文 patterns (hierarchical structure)
        chapter_patterns = [
            r'^第[一二三四五六七八九十百]+章',
            r'^第[一二三四五六七八九十百]+条',
            r'^Chapter\s+\d+',
            r'^Article\s+\d+',
        ]
        has_chapters = any(re.match(p, l.strip()) for l in lines for p in chapter_patterns)
        if has_chapters and line_count > 2:
            return '正文'

        # Check for 封面 patterns (at document start)
        if start_line == 0:
            cover_patterns = ['合同', '协议', '编号：', 'no.', '甲方：', '乙方：', '买方：', '卖方：']
            if any(p in lines[0] for p in cover_patterns):
                return '封面'

        # Fallback for empty/short content
        if line_count <= 2:
            return None

        # Final fallback
        return '正文' if has_chapters else None

    def _to_json(self) -> List[Dict]:
        """Convert modules to JSON format."""
        return [{'type': m.type, 'text': m.text} for m in self.modules]

    def load_reference_patterns(self, reference_file: str) -> None:
        """Load custom reference patterns from file."""
        # This can be extended to load industry-specific patterns
        pass


def extract_modules(text: str) -> List[Dict]:
    """Main function to extract modules from contract text."""
    extractor = ContractModuleExtractor(text)
    return extractor.extract()


def main():
    """Command-line interface."""
    import sys
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    if len(sys.argv) < 2:
        print("Usage: python extract_modules.py <contract_file.txt>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        text = f.read()

    modules = extract_modules(text)
    print(json.dumps(modules, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
