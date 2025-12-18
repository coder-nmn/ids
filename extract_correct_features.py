"""Extract real attack samples with correct 40 features"""
import pandas as pd
import pickle

print("=" * 70)
print("Extracting Real Samples with Correct Features")
print("=" * 70)

# Load feature names the model expects
with open('models/feature_names.pkl', 'rb') as f:
    model_features = pickle.load(f)

print(f"\nModel expects {len(model_features)} features")

# Load the real attack samples
print("\nLoading real attack samples...")
df = pd.read_csv('real_attack_samples.csv')
print(f"✅ Loaded {len(df)} samples with {len(df.columns)} features")

# Check if there's a Label column
if 'Label' in df.columns:
    print(f"\n📊 Attack types in data:")
    label_counts = df['Label'].value_counts()
    for label, count in label_counts.items():
        print(f"   {label}: {count} samples")

# Check which features match
print(f"\n🔍 Checking feature availability...")
available_features = []
missing_features = []

for feat in model_features:
    if feat in df.columns:
        available_features.append(feat)
    else:
        missing_features.append(feat)

print(f"✅ Available: {len(available_features)}/{len(model_features)}")
print(f"❌ Missing: {len(missing_features)}/{len(model_features)}")

if missing_features:
    print(f"\nMissing features:")
    for feat in missing_features[:10]:  # Show first 10
        print(f"   - {feat}")
    if len(missing_features) > 10:
        print(f"   ... and {len(missing_features) - 10} more")

# Try to extract available features
if len(available_features) >= 30:  # If we have at least 30 features
    print(f"\n✅ Extracting {len(available_features)} available features...")
    
    # Create dataframe with available features, fill missing with 0
    extracted_df = pd.DataFrame()
    for feat in model_features:
        if feat in df.columns:
            extracted_df[feat] = df[feat]
        else:
            extracted_df[feat] = 0.0  # Fill missing features with 0
    
    # Add label if available
    if 'Label' in df.columns:
        extracted_df['Label'] = df['Label']
    
    # Save
    output_file = 'real_samples_40_features.csv'
    extracted_df.to_csv(output_file, index=False)
    print(f"💾 Saved to: {output_file}")
    print(f"   Samples: {len(extracted_df)}")
    print(f"   Features: {len(extracted_df.columns) - (1 if 'Label' in extracted_df.columns else 0)}")
else:
    print(f"\n❌ Not enough matching features ({len(available_features)}/40)")
    print("The dataset structure might be different from what the model expects.")

print("\n" + "=" * 70)
