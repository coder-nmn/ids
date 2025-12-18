"""
Test Prediction Pipeline
"""

import tensorflow as tf
import pickle
import numpy as np
import pandas as pd

print("Loading model and preprocessors...")

# Load model
model = tf.keras.models.load_model('models/cnn_lstm_final.h5')

# Load preprocessors
with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('models/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

with open('models/feature_names.pkl', 'rb') as f:
    feature_names = pickle.load(f)

print(f"✅ Loaded successfully")
print(f"   Model: {model.output_shape[-1]} classes")
print(f"   Scaler: {scaler.n_features_in_} features")
print(f"   Label encoder: {len(label_encoder.classes_)} classes")
print(f"   Feature names: {len(feature_names)} features")

# Test prediction with dummy data
print("\nTesting prediction with dummy data...")

# Create dummy features
dummy_features = [0.0] * len(feature_names)

# Convert to DataFrame
features_df = pd.DataFrame([dummy_features], columns=feature_names)

# Scale
features_scaled = scaler.transform(features_df)

# Create sequence
sequence_length = 10
sequence = np.tile(features_scaled, (sequence_length, 1))
sequence = sequence.reshape(1, sequence_length, -1)

print(f"Sequence shape: {sequence.shape}")

# Predict
prediction = model.predict(sequence, verbose=0)
pred_class = np.argmax(prediction[0])
confidence = float(prediction[0][pred_class])
attack_name = label_encoder.inverse_transform([pred_class])[0]

print(f"\n✅ Prediction successful!")
print(f"   Predicted class: {pred_class}")
print(f"   Attack type: {attack_name}")
print(f"   Confidence: {confidence:.2%}")
print(f"   Probabilities shape: {prediction[0].shape}")

print("\nTop 5 predictions:")
top_5_idx = np.argsort(prediction[0])[-5:][::-1]
for idx in top_5_idx:
    attack = label_encoder.inverse_transform([idx])[0]
    prob = prediction[0][idx]
    print(f"   {attack}: {prob:.2%}")

print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\nYou can now run the dashboard:")
print("  streamlit run app.py")
