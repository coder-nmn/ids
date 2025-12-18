"""Extract Web Attack samples"""
import pandas as pd
import pickle

# Load feature names
with open('models/feature_names.pkl', 'rb') as f:
    model_features = pickle.load(f)

# Try different encodings
encodings = ['latin-1', 'iso-8859-1', 'cp1252']

for encoding in encodings:
    try:
        print(f"Trying encoding: {encoding}")
        df = pd.read_csv('Datasets/Datasets/3rd/Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv', 
                        encoding=encoding)
        print(f"✅ Success! Loaded {len(df)} records")
        
        # Get label column
        label_col = 'Label' if 'Label' in df.columns else ' Label'
        
        # Show unique labels
        print(f"\nAttack types found:")
        labels = df[label_col].unique()
        for label in labels:
            count = len(df[df[label_col] == label])
            print(f"   {label}: {count} samples")
        
        # Extract samples for each web attack type
        web_samples = []
        for label in labels:
            if label != 'BENIGN':
                attack_df = df[df[label_col] == label]
                n_samples = min(3, len(attack_df))
                samples = attack_df.sample(n=n_samples, random_state=42)
                
                # Extract 40 features
                extracted = pd.DataFrame()
                for feat in model_features:
                    if feat in samples.columns:
                        extracted[feat] = samples[feat].values
                    elif ' ' + feat in samples.columns:
                        extracted[feat] = samples[' ' + feat].values
                    else:
                        extracted[feat] = 0.0
                
                extracted['Label'] = label
                web_samples.append(extracted)
                print(f"   ✅ Extracted {len(extracted)} samples for {label}")
        
        # Save
        if web_samples:
            web_df = pd.concat(web_samples, ignore_index=True)
            web_df.to_csv('web_attack_samples.csv', index=False)
            print(f"\n💾 Saved {len(web_df)} web attack samples to web_attack_samples.csv")
        
        break
        
    except Exception as e:
        print(f"❌ Failed with {encoding}: {e}")

print("\n✅ Done!")
