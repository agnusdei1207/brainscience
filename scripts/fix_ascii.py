import os
import glob
import unicodedata

def get_char_width(c):
    if c in '▶◀▼▲■':
        return 1
    if 0x2500 <= ord(c) <= 0x257F:
        return 1
    status = unicodedata.east_asian_width(c)
    if status in ('W', 'F'):
        return 2
    return 1

def get_str_width(s):
    return sum(get_char_width(c) for c in s)

def pad_str(s, target_width):
    w = get_str_width(s)
    if w < target_width:
        pad_char = '─' if s and s[-1] == '─' else ' '
        return s + pad_char * (target_width - w)
    return s

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
    except:
        return

    out_lines = []
    i = 0
    changed = False
    while i < len(lines):
        line = lines[i]
        if line.startswith('```text'):
            out_lines.append(line)
            i += 1
            box_lines = []
            while i < len(lines) and not lines[i].startswith('```'):
                box_lines.append(lines[i])
                i += 1
            
            if box_lines:
                max_w = 0
                for bl in box_lines:
                    if bl.startswith('┌') and bl.endswith('┐'):
                        w = get_str_width(bl[1:-1])
                    elif bl.startswith('├') and bl.endswith('┤'):
                        w = get_str_width(bl[1:-1])
                    elif bl.startswith('└') and bl.endswith('┘'):
                        w = get_str_width(bl[1:-1])
                    elif bl.startswith('│') and bl.endswith('│'):
                        w = get_str_width(bl[1:-1].rstrip())
                    else:
                        w = get_str_width(bl)
                    if w > max_w: max_w = w
                
                for bl in box_lines:
                    if bl.startswith('┌') and bl.endswith('┐'):
                        out_lines.append('┌' + '─' * max_w + '┐')
                    elif bl.startswith('├') and bl.endswith('┤'):
                        inner = bl[1:-1]
                        # Trim trailing ─ from inner to strictly pad it
                        w = get_str_width(inner)
                        out_lines.append('├' + inner + '─' * (max_w - w) + '┤')
                    elif bl.startswith('└') and bl.endswith('┘'):
                        out_lines.append('└' + '─' * max_w + '┘')
                    elif bl.startswith('│') and bl.endswith('│'):
                        inner = bl[1:-1].rstrip()
                        out_lines.append('│' + pad_str(inner, max_w) + '│')
                    else:
                        # Not a typical box line, just append
                        out_lines.append(bl)
            if i < len(lines):
                out_lines.append(lines[i])
        else:
            out_lines.append(line)
        i += 1
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out_lines) + '\n')

for file in glob.glob("content/studynote/1_computer_architecture/**/*.md", recursive=True):
    fix_file(file)

print("ASCII fix completed.")
