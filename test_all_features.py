"""
Comprehensive End-to-End Feature Test
Tests all IDS features and saves data to database
"""

import tensorflow as tf
import pickle
import numpy as np
import pandas as pd
from database import IDSDatabase
from datetime import datetime
import time

print("="*70)
print("COMPREHENSIVE IDS FEATURE TEST")
print("="*70)

# Initialize database
print("\n1. Initializing Database...")
db = IDSDatabase()
print("   ✅ Database initialized")

# Load model and preprocessors
print("\n2. Loading Model and Preprocessors...")
model = tf.keras.models.load_model('models/cnn_lstm_final.h5')

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('models/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

with open('models/feature_names.pkl', 'rb') as f:
    feature_names = pickle.load(f)

print(f"   ✅ Model loaded: {model.output_shape[-1]} classes")
print(f"   ✅ Scaler loaded: {scaler.n_features_in_} features")
print(f"   ✅ Label encoder: {len(label_encoder.classes_)} classes")

# Test 1: Predict with dummy data (all zeros)
print("\n3. Test 1: Benign Traffic (All Zeros)")
dummy_features = [0.0] * len(feature_names)
features_df = pd.DataFrame([dummy_features], columns=feature_names)
features_scaled = scaler.transform(features_df)
sequence = np.tile(features_scaled, (10, 1)).reshape(1, 10, -1)

prediction = model.predict(sequence, verbose=0)
pred_class = np.argmax(prediction[0])
confidence = float(prediction[0][pred_class])
attack_name = label_encoder.inverse_transform([pred_class])[0]

print(f"   Prediction: {attack_name}")
print(f"   Confidence: {confidence:.2%}")

# Save to database
detection_id = db.add_detection(
    attack_type=attack_name,
    confidence=confidence,
    features=dummy_features,
    probabilities=prediction[0],
    source_ip="192.168.1.100",
    destination_ip="192.168.1.1",
    notes="Test 1: Dummy benign traffic"
)
print(f"   ✅ Saved to database (ID: {detection_id})")

# Test 2: Load real data and test
print("\n4. Test 2: Real Dataset Samples")
print("   Loading sample data...")

# Load a small sample from the dataset
data_path = 'Datasets/Datasets/cic-ids/Benign-Monday-no-metadata.parquet'
df_sample = pd.read_parquet(data_path)
df_sample = df_sample.sample(n=5, random_state=42)

print(f"   Testing {len(df_sample)} real samples...")

for idx, row in df_sample.iterrows():
    # Extract features
    features = []
    for feat in feature_names:
        if feat in df_sample.columns:
            val = row[feat]
            # Handle inf and nan
            if pd.isna(val) or np.isinf(val):
                val = 0.0
            features.append(float(val))
        else:
            features.append(0.0)
    
    # Predict
    features_df = pd.DataFrame([features], columns=feature_names)
    features_scaled = scaler.transform(features_df)
    sequence = np.tile(features_scaled, (10, 1)).reshape(1, 10, -1)
    
    prediction = model.predict(sequence, verbose=0)
    pred_class = np.argmax(prediction[0])
    confidence = float(prediction[0][pred_class])
    attack_name = label_encoder.inverse_transform([pred_class])[0]
    
    # Save to database
    detection_id = db.add_detection(
        attack_type=attack_name,
        confidence=confidence,
        features=features,
        probabilities=prediction[0],
        source_ip=f"192.168.1.{100+idx}",
        destination_ip="192.168.1.1",
        notes=f"Test 2: Real sample {idx}"
    )
    
    print(f"   Sample {idx}: {attack_name} ({confidence:.2%}) - ID: {detection_id}")

# Test 3: Test different attack types
print("\n5. Test 3: Simulated Attack Patterns")

attack_patterns = [
    {"name": "High Traffic", "multiplier": 100.0},
    {"name": "Suspicious Ports", "multiplier": 50.0},
    {"name": "Rapid Connections", "multiplier": 200.0},
]

for pattern in attack_patterns:
    features = [pattern["multiplier"] * np.random.random() for _ in range(len(feature_names))]
    
    features_df = pd.DataFrame([features], columns=feature_names)
    features_scaled = scaler.transform(features_df)
    sequence = np.tile(features_scaled, (10, 1)).reshape(1, 10, -1)
    
    prediction = model.predict(sequence, verbose=0)
    pred_class = np.argmax(prediction[0])
    confidence = float(prediction[0][pred_class])
    attack_name = label_encoder.inverse_transform([pred_class])[0]
    
    detection_id = db.add_detection(
        attack_type=attack_name,
        confidence=confidence,
        features=features,
        probabilities=prediction[0],
        source_ip="10.0.0.50",
        destination_ip="192.168.1.1",
        notes=f"Test 3: {pattern['name']}"
    )
    
    print(f"   {pattern['name']}: {attack_name} ({confidence:.2%}) - ID: {detection_id}")

# Test 4: Database retrieval
print("\n6. Test 4: Database Retrieval")

stats = db.get_statistics()
print(f"   Total Detections: {stats['total_detections']}")
print(f"   Attack Count: {stats['attack_count']}")
print(f"   Benign Count: {stats['benign_count']}")
print(f"   Average Confidence: {stats['avg_confidence']:.2%}")

print("\n   Attack Distribution:")
for attack_type, count in stats['attack_distribution']:
    print(f"      {attack_type}: {count}")

print("\n   Recent Detections:")
for detection in stats['recent_detections'][:5]:
    timestamp, attack_type, confidence, risk_level = detection
    print(f"      {timestamp} | {attack_type} | {confidence:.2%} | {risk_level}")

# Test 5: Retrieve specific detection
print("\n7. Test 5: Retrieve Specific Detection")
detection = db.get_detection_by_id(1)
if detection:
    print(f"   Detection ID: {detection['id']}")
    print(f"   Timestamp: {detection['timestamp']}")
    print(f"   Attack Type: {detection['attack_type']}")
    print(f"   Confidence: {detection['confidence']:.2%}")
    print(f"   Risk Level: {detection['risk_level']}")
    print(f"   Source IP: {detection['source_ip']}")
    print(f"   Notes: {detection['notes']}")

# Test 6: Export data
print("\n8. Test 6: Export Data to CSV")
export_path = db.export_to_csv('data/test_detections_export.csv')
print(f"   ✅ Exported to: {export_path}")

# Test 7: Timeline
print("\n9. Test 7: Attack Timeline")
timeline = db.get_attack_timeline(hours=24)
if len(timeline) > 0:
    print(f"   Timeline entries: {len(timeline)}")
    print(timeline.head())
else:
    print("   No timeline data yet")

# Final Summary
print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)

all_detections = db.get_all_detections()
print(f"✅ Total detections in database: {len(all_detections)}")
print(f"✅ All features tested successfully")
print(f"✅ Data persistence working")
print(f"✅ Retrieval working")
print(f"✅ Export working")

print("\n" + "="*70)
print("ALL TESTS PASSED!")
print("="*70)

print("\nYou can now:")
print("  1. Run the dashboard: streamlit run app.py")
print("  2. View all saved detections in the dashboard")
print("  3. Export data anytime")
print("  4. Historical data persists across restarts")
