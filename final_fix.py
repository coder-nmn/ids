"""Final comprehensive fix for app.py"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Check if line ends with : (if, elif, for, with, def, class)
    if line.strip() and line.rstrip().endswith(':'):
        fixed.append(line)
        indent = len(line) - len(line.lstrip())
        
        # Check next non-empty line
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            fixed.append(lines[j])
            j += 1
        
        if j < len(lines):
            next_line = lines[j]
            next_indent = len(next_line) - len(next_line.lstrip())
            
            # If next line is not indented enough, fix it
            if next_indent <= indent:
                fixed.append(' ' * (indent + 4) + next_line.lstrip())
                i = j
            else:
                i += 1
        else:
            i += 1
    else:
        fixed.append(line)
        i += 1

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed)

print("✅ Final fix complete!")
