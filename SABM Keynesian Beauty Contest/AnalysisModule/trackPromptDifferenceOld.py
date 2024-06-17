import os
import json
import re
from datetime import datetime
from difflib import SequenceMatcher
from typing import List, Dict
import sys

def find_record_folders(base_path: str) -> List[str]:
    record_folders = []
    for root, dirs, files in os.walk(base_path):
        for folder in dirs:
            if re.match(r'^Record_\d{6}_\d{6}_gpt-4-0314.*$', folder):
                record_folders.append(os.path.join(root, folder))
    return sorted(
        record_folders,
        key=lambda x: datetime.strptime(os.path.basename(x).split('_')[1] + os.path.basename(x).split('_')[2], '%y%m%d%H%M%S')
    )

def load_json(file_path: str) -> Dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def wrap_text(text: str, width: int = 100) -> str:
    wrapped_lines = []
    current_line = ''
    in_tag = False
    tag_buffer = ''

    for char in text:
        if char == '<':
            in_tag = True
            tag_buffer += char
            continue
        elif char == '>':
            in_tag = False
            tag_buffer += char
            current_line += tag_buffer
            tag_buffer = ''
            continue

        if in_tag:
            tag_buffer += char
        else:
            if len(current_line) >= width:
                wrapped_lines.append(current_line)
                current_line = char
            else:
                current_line += char

    if current_line:
        wrapped_lines.append(current_line)

    return '<br>'.join(wrapped_lines)

def highlight_diffs(text1: str, text2: str) -> str:
    s = SequenceMatcher(None, text1, text2)
    result = []
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'equal':
            result.append(text1[i1:i2])
        elif tag == 'replace':
            result.append('<span style="background-color: #ffcccc;">{}</span>'.format(text1[i1:i2]))
            result.append('<span style="background-color: #ccffcc;">{}</span>'.format(text2[j1:j2]))
        elif tag == 'delete':
            result.append('<span style="background-color: #ffcccc;">{}</span>'.format(text1[i1:i2]))
        elif tag == 'insert':
            result.append('<span style="background-color: #ccffcc;">{}</span>'.format(text2[j1:j2]))
    
    highlighted_text = ''.join(result)
    highlighted_text = highlighted_text.replace('\n', '<br>')
    return wrap_text(highlighted_text, width=100)

def generate_diff_html(json1: Dict, json2: Dict) -> str:
    json1_str = json.dumps(json1, indent=4, ensure_ascii=False, sort_keys=True).replace('\n', '<br>')
    json2_str = json.dumps(json2, indent=4, ensure_ascii=False, sort_keys=True).replace('\n', '<br>')
    json1_lines = json1_str.split('<br>')
    json2_lines = json2_str.split('<br>')

    s = SequenceMatcher(None, json1_lines, json2_lines)
    result = []
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'equal':
            result.extend([line for line in json1_lines[i1:i2]])
        elif tag == 'replace':
            for line1, line2 in zip(json1_lines[i1:i2], json2_lines[j1:j2]):
                result.append(highlight_diffs(line1, line2))
        elif tag == 'delete':
            result.extend(['<span style="background-color: #ffcccc;">' + line + '</span>' for line in json1_lines[i1:i2]])
        elif tag == 'insert':
            result.extend(['<span style="background-color: #ccffcc;">' + line + '</span>' for line in json2_lines[j1:j2]])

    return '<br>'.join(result)

def compare_json(json1: Dict, json2: Dict) -> str:
    json1_str = json.dumps(json1, indent=4, ensure_ascii=False, sort_keys=True)
    json2_str = json.dumps(json2, indent=4, ensure_ascii=False, sort_keys=True)
    if json1_str == json2_str:
        return None
    else:
        return generate_diff_html(json1, json2)

def generate_html_report(differences: List[Dict[str, str]], output_file: str) -> None:
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<html><body><h1 style="font-family: Consolas;">JSON Comparison Report</h1>')
        for diff in differences:
            if 'diff' not in diff or not diff['diff']:
                f.write('<h4 style="font-family: Consolas;">{}</h4>'.format(diff['folders'][0]))
            else:
                f.write('<h2 style="font-family: Consolas;">{}</h2>'.format(' vs '.join(diff['folders'])))
                f.write('<pre style="font-family: Consolas;">{}</pre>'.format(diff['diff']))
        f.write('</body></html>')

def main(base_path: str, output_file: str) -> None:
    record_folders = find_record_folders(base_path)
    differences = []
    
    for i in range(1, len(record_folders)):
        prev_folder = os.path.join(record_folders[i - 1], 'config', 'config_prompt.json')
        curr_folder = os.path.join(record_folders[i], 'config', 'config_prompt.json')
        
        if os.path.exists(prev_folder) and os.path.exists(curr_folder):
            prev_json = load_json(prev_folder)
            curr_json = load_json(curr_folder)
            diff = compare_json(prev_json, curr_json)
            if diff:
                differences.append({
                    'folders': [os.path.basename(record_folders[i - 1]), os.path.basename(record_folders[i])],
                    'diff': diff
                })
            else:
                differences.append({
                    'folders': [os.path.basename(record_folders[i - 1])],
                })

    generate_html_report(differences, output_file)

if __name__ == "__main__":
    sys.path.append(".")
    base_path = './output'
    output_file = './AnalysisModule/results/comparison_report.html'
    main(base_path, output_file)
