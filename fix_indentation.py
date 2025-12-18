"""Fix indentation in app.py for EDA sections"""

# Read the file
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with "if selected_section == 1:"
fixed_lines = []
in_section = False
section_indent = 0

for i, line in enumerate(lines):
    # Check if we're at a section start
    if 'if selected_section == 1:' in line or 'elif selected_section ==' in line:
        fixed_lines.append(line)
        in_section = True
        section_indent = len(line) - len(line.lstrip())
        continue
    
    # Check if we're at the next section or end of function
    if in_section and (line.strip().startswith('elif selected_section ==') or 
                       line.strip().startswith('def ') or
                       (line.strip() and not line[0].isspace() and i > 700)):
        in_section = False
    
    # If we're in a section, add extra indentation
    if in_section and line.strip():
        # Get current indentation
        current_indent = len(line) - len(line.lstrip())
        # Add 4 spaces if not already indented enough
        if current_indent <= section_indent:
            fixed_lines.append('    ' + line)
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("✅ Indentation fixed!")
