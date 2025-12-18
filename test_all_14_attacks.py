"""Test script to run predictions on all 14 attack types"""
import pandas as pd
import numpy as np
import pickle
import tensorflow as tf

print("=" * 70)
print("Testing All 14 Attack Types Detection")
print("=" * 70)

# Load the data
print("\n1. Loading data...")
df = pd.read_csv('all_14_attack_types.csv')
print(f"✅ Loaded {len(df)} samples with {len(df.columns)} features")

# Load model and preprocessors
print("\n2. Loading model and preprocessors...")
model = tf.keras.models.load_model('models/cnn_lstm_final.h5')
print("✅ Model loaded")

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
print("✅ Scaler loaded")

with open('models/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)
print("✅ Label encoder loaded")

with open('models/feature_names.pkl', 'rb') as f:
    feature_names = pickle.load(f)
print(f"✅ Feature names loaded ({len(feature_names)} features)")

# Show attack types the model can detect
print("\n3. Attack types the model can detect:")
for i, attack in enumerate(label_encoder.classes_, 1):
    print(f"   {i}. {attack}")

# Run predictions
print("\n4. Running predictions on all samples...")
predictions = []
confidences = []

for idx, row in df.iterrows():
    # Extract features
    features = []
    for feat in feature_names:
        if feat in df.columns:
            val = row[feat]
            if pd.isna(val) or np.isinf(val):
                val = 0.0
            features.append(float(val))
        else:
            features.append(0.0)
    
    # Create DataFrame and scale
    features_df = pd.DataFrame([features], columns=feature_names)
    features_scaled = scaler.transform(features_df)
    
    # Create sequence
    sequence = np.tile(features_scaled, (10, 1))
    sequence = sequence.reshape(1, 10, -1)
    
    # Predict
    prediction = model.predict(sequence, verbose=0)
    pred_class = np.argmax(prediction[0])
    confidence = float(prediction[0][pred_class])
    attack_name = label_encoder.inverse_transform([pred_class])[0]
    
    predictions.append(attack_name)
    confidences.append(confidence)
    
    print(f"   Sample {idx+1:2d}: {attack_name:30s} (Confidence: {confidence:.2%})")

# Add predictions to dataframe
df['Predicted_Attack'] = predictions
df['Confidence'] = confidences

# Show results
print("\n" + "=" * 70)
print("RESULTS SUMMARY")
print("=" * 70)

# Attack distribution
print("\n📊 Attack Type Distribution:")
attack_counts = df['Predicted_Attack'].value_counts()
for attack, count in attack_counts.items():
    percentage = (count / len(df)) * 100
    print(f"   {attack:30s}: {count:2d} samples ({percentage:5.1f}%)")

# Statistics
print(f"\n📈 Statistics:")
print(f"   Total samples analyzed: {len(df)}")
print(f"   Unique attack types detected: {len(attack_counts)}")
print(f"   Average confidence: {df['Confidence'].mean():.2%}")
print(f"   Min confidence: {df['Confidence'].min():.2%}")
print(f"   Max confidence: {df['Confidence'].max():.2%}")

# Risk levels
df['Risk_Level'] = df['Confidence'].apply(
    lambda x: 'High' if x > 0.9 else 'Medium' if x > 0.7 else 'Low'
)

print(f"\n⚠️ Risk Level Distribution:")
risk_counts = df['Risk_Level'].value_counts()
for risk, count in risk_counts.items():
    percentage = (count / len(df)) * 100
    print(f"   {risk:10s}: {count:2d} samples ({percentage:5.1f}%)")

# Save results
output_file = 'prediction_results.csv'
df.to_csv(output_file, index=False)
print(f"\n💾 Results saved to: {output_file}")

print("\n" + "=" * 70)
print("✅ SUCCESS! All 14 attack types tested!")
print("=" * 70)
