"""Fix menu items in app.py"""

with open('app.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Fix menu items
replacements = [
    ('StartU Monitoring', 'Start Monitoring'),
    ('Real-Time rDetection', 'Real-Time Detection'),
    ('Moedel Performance', 'Model Performance'),
    ('Detectmion History', 'Detection History'),
    ('Sitart Monitoring', 'Start Monitoring'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Fixed all menu items!')
print('\nFixed:')
for old, new in replacements:
    print(f'  {old} → {new}')
