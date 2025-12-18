"""Comprehensive indentation fix for EDA sections"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []
in_section = False
section_indent = 0

for i, line in enumerate(lines):
    # Check if we're starting a section
    if ('if selected_section == 1:' in line or 'elif selected_section ==' in line) and i > 700:
        fixed_lines.append(line)
        in_section = True
        section_indent = len(line) - len(line.lstrip())
        continue
    
    # Check if we're ending a section (next elif or function def)
    if in_section and i > 700:
        if (line.strip().startswith('elif selected_section ==') or 
            line.strip().startswith('def show_database_eda')):
            in_section = False
            fixed_lines.append(line)
            continue
    
    # If in section, ensure proper indentation
    if in_section and line.strip():
        current_indent = len(line) - len(line.lstrip())
        # Content should be indented 4 more spaces than the if/elif
        if current_indent <= section_indent:
            fixed_lines.append(' ' * (section_indent + 4) + line.lstrip())
        else:
            # Already has some indentation, adjust it
            extra_indent = current_indent - section_indent
            fixed_lines.append(' ' * (section_indent + 4 + extra_indent - 4) + line.lstrip())
    else:
        fixed_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("✅ All indentation fixed!")
