"""Fix EDA section indentation"""

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Split by sections
sections = content.split('elif selected_section ==')

# First part (before any elif)
parts = [sections[0]]

# Fix each section (2-8)
for i, section in enumerate(sections[1:], start=2):
    # Split into header and body
    lines = section.split('\n')
    
    # First line is the condition (e.g., " 2:")
    header = f"elif selected_section == {lines[0]}"
    
    # Rest needs indentation
    body_lines = []
    for line in lines[1:]:
        if line.strip() and not line.startswith('    # ============'):
            # Add 4 spaces if not a section marker
            if line and not line[0].isspace():
                body_lines.append('    ' + line)
            elif line.startswith('    ') and not line.startswith('        '):
                # Already has 4 spaces, needs 4 more
                body_lines.append('    ' + line)
            else:
                body_lines.append(line)
        else:
            body_lines.append(line)
    
    parts.append(header + '\n' + '\n'.join(body_lines))

# Join back
fixed_content = ''.join(parts)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✅ Fixed indentation!")
