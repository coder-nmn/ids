"""Fix emoji encoding in app.py"""

with open('app.py', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

# Fix line 158 (menu items)
for i, line in enumerate(lines):
    if '"� Start Monitoring"' in line:
        lines[i] = line.replace('"� Start Monitoring"', '"🚀 Start Monitoring"')
        lines[i] = lines[i].replace('"� Real-Time Detection"', '"🔴 Real-Time Detection"')
        lines[i] = lines[i].replace('"� Model Performance"', '"📊 Model Performance"')
        lines[i] = lines[i].replace('"� Detection History"', '"📜 Detection History"')
        print(f'Fixed line {i+1}: Menu items')
    
    if 'mode == "� Start Monitoring"' in line:
        lines[i] = line.replace('"� Start Monitoring"', '"🚀 Start Monitoring"')
        print(f'Fixed line {i+1}: Mode check for Start Monitoring')

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('\n✅ All emojis fixed!')
