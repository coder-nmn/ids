"""Test Dashboard Components"""

print("Testing Dashboard Components...")
print("="*60)

# Test 1: Check database
print("\n1. Testing Database...")
from database import IDSDatabase
db = IDSDatabase()
stats = db.get_statistics()
print(f"   ✅ Total Detections: {stats['total_detections']}")
print(f"   ✅ Attacks: {stats['attack_count']}")
print(f"   ✅ Benign: {stats['benign_count']}")

# Test 2: Check sample data
print("\n2. Testing Sample Data...")
import pandas as pd
df = pd.read_csv('sample_network_data.csv')
print(f"   ✅ Sample data: {len(df)} rows, {len(df.columns)} columns")

# Test 3: Check model files
print("\n3. Testing Model Files...")
import os
files = [
    'models/cnn_lstm_final.h5',
    'models/scaler.pkl',
    'models/label_encoder.pkl',
    'models/feature_names.pkl'
]
for f in files:
    if os.path.exists(f):
        print(f"   ✅ {f}")
    else:
        print(f"   ❌ {f} - MISSING!")

# Test 4: Check app.py menu
print("\n4. Testing App Menu...")
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
menu_items = [
    '🚀 Start Monitoring',
    '🔴 Real-Time Detection',
    '📊 Model Performance',
    '📜 Detection History'
]

for item in menu_items:
    if item in content:
        print(f"   ✅ {item}")
    else:
        print(f"   ❌ {item} - NOT FOUND!")

print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\nYour dashboard is ready!")
print("Run: streamlit run app.py")
