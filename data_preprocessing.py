"""
Data Preprocessing Module
Loads and preprocesses CIC-IDS dataset for IDS training
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import pickle
import os

class DataPreprocessor:
    def __init__(self, data_path='Datasets/Datasets/cic-ids'):
        self.data_path = data_path
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_names = None
        
    def load_cic_ids_data(self, sample_per_file=None):
        """Load all CIC-IDS parquet files with optional sampling"""
        print("Loading CIC-IDS dataset...")
        
        files = [
            'Benign-Monday-no-metadata.parquet',
            'Botnet-Friday-no-metadata.parquet',
            'Bruteforce-Tuesday-no-metadata.parquet',
            'DDoS-Friday-no-metadata.parquet',
            'DoS-Wednesday-no-metadata.parquet',
            'Infiltration-Thursday-no-metadata.parquet',
            'Portscan-Friday-no-metadata.parquet',
            'WebAttacks-Thursday-no-metadata.parquet'
        ]
        
        dfs = []
        for f in files:
            file_path = os.path.join(self.data_path, f)
            if os.path.exists(file_path):
                df = pd.read_parquet(file_path)
                
                # Sample if needed to reduce memory
                if sample_per_file and len(df) > sample_per_file:
                    df = df.sample(n=sample_per_file, random_state=42)
                    print(f"Loaded {f}: {len(df)} records (sampled)")
                else:
                    print(f"Loaded {f}: {len(df)} records")
                
                dfs.append(df)
            else:
                print(f"Warning: {f} not found")
        
        print("\nCombining datasets...")
        data = pd.concat(dfs, ignore_index=True)
        print(f"Total records: {len(data):,}")
        print(f"Total features: {len(data.columns)}")
        print(f"Attack types: {data['Label'].nunique()}")
        
        return data
    
    def clean_data(self, df):
        """Clean and prepare data (memory-efficient)"""
        print("\nCleaning data...")
        
        # Handle missing values column by column to save memory
        print("Handling missing values...")
        for col in df.columns:
            if df[col].dtype in [np.float32, np.float64]:
                # Replace inf with nan
                df[col] = df[col].replace([np.inf, -np.inf], np.nan)
                # Fill nan with 0
                df[col] = df[col].fillna(0)
        
        # Remove constant columns
        print("Removing constant columns...")
        cols_to_drop = []
        for col in df.columns:
            if df[col].nunique() == 1:
                cols_to_drop.append(col)
        
        if len(cols_to_drop) > 0:
            print(f"Dropping {len(cols_to_drop)} constant columns")
            df = df.drop(columns=cols_to_drop)
        
        # Skip duplicate removal to save memory
        print("Skipping duplicate removal to save memory...")
        print(f"After cleaning: {len(df)} records, {len(df.columns)} features")
        
        return df
    
    def select_features(self, df, n_features=40):
        """Select top N most important features"""
        print(f"\nSelecting top {n_features} features...")
        
        # Separate features and labels
        X = df.drop('Label', axis=1)
        y = df['Label']
        
        # Remove non-numeric columns
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        X = X[numeric_cols]
        
        print(f"Total numeric features: {len(numeric_cols)}")
        
        # Feature selection using Random Forest
        from sklearn.ensemble import RandomForestClassifier
        
        # Sample for faster computation and less memory
        sample_size = min(30000, len(X))
        print(f"Using sample of {sample_size} records for feature selection...")
        
        X_sample = X.sample(n=sample_size, random_state=42)
        y_sample = y.loc[X_sample.index]
        
        # Encode labels for RF
        le_temp = LabelEncoder()
        y_sample_encoded = le_temp.fit_transform(y_sample)
        
        print("Training Random Forest for feature importance...")
        rf = RandomForestClassifier(
            n_estimators=50, 
            max_depth=10,  # Limit depth to save memory
            random_state=42, 
            n_jobs=-1,
            verbose=0
        )
        rf.fit(X_sample, y_sample_encoded)
        
        # Get feature importance
        importances = pd.DataFrame({
            'feature': X.columns,
            'importance': rf.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Select top features
        top_features = importances.head(n_features)['feature'].tolist()
        self.feature_names = top_features
        
        print(f"Selected top {len(top_features)} features")
        print(f"Top 5 features: {top_features[:5]}")
        
        # Free memory
        del X_sample, y_sample, y_sample_encoded, rf
        
        return X[top_features], y

    
    def preprocess_data(self, X, y, apply_smote=True, max_samples=800000):
        """Preprocess features and labels (max_samples increased for better accuracy)"""
        print("\nPreprocessing data...")
        
        # Limit dataset size to prevent memory issues
        if len(X) > max_samples:
            print(f"Dataset too large ({len(X)} records). Sampling {max_samples} records...")
            sample_indices = np.random.choice(len(X), max_samples, replace=False)
            X = X.iloc[sample_indices]
            y = y.iloc[sample_indices]
            print(f"Using {len(X)} samples")
        
        # Encode labels
        print("Encoding labels...")
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Scale features
        print("Scaling features...")
        X_scaled = self.scaler.fit_transform(X)
        
        # Train-test split
        print("Splitting train/test...")
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        print(f"Train set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        
        # Apply SMOTE for balancing (only if train set is not too large)
        if apply_smote and len(X_train) < 300000:
            print("\nApplying SMOTE for class balancing...")
            try:
                smote = SMOTE(random_state=42, k_neighbors=5, n_jobs=-1)
                X_train, y_train = smote.fit_resample(X_train, y_train)
                print(f"After SMOTE: {len(X_train)} samples")
            except Exception as e:
                print(f"SMOTE failed: {e}")
                print("Continuing without SMOTE...")
        else:
            print("Skipping SMOTE (dataset large enough)")
        
        return X_train, X_test, y_train, y_test
    
    def create_sequences(self, X, y, sequence_length=10, max_sequences=200000):
        """Create sequences for LSTM"""
        print(f"\nCreating sequences (length={sequence_length})...")
        
        # Limit number of sequences to prevent memory issues
        max_possible = len(X) - sequence_length
        if max_possible > max_sequences:
            print(f"Too many possible sequences ({max_possible}). Limiting to {max_sequences}...")
            # Sample indices
            indices = np.random.choice(max_possible, max_sequences, replace=False)
            indices = np.sort(indices)
        else:
            indices = range(max_possible)
        
        sequences = []
        labels = []
        
        print("Creating sequences...")
        for i in indices:
            seq = X[i:i+sequence_length]
            label = y[i+sequence_length]
            sequences.append(seq)
            labels.append(label)
            
            # Progress indicator
            if len(sequences) % 50000 == 0:
                print(f"  Created {len(sequences)} sequences...")
        
        X_seq = np.array(sequences, dtype=np.float32)  # Use float32 to save memory
        y_seq = np.array(labels, dtype=np.int32)
        
        print(f"Created {len(X_seq)} sequences")
        print(f"Sequence shape: {X_seq.shape}")
        
        return X_seq, y_seq
    
    def save_preprocessors(self, output_dir='models'):
        """Save scaler and label encoder"""
        os.makedirs(output_dir, exist_ok=True)
        
        with open(f'{output_dir}/scaler.pkl', 'wb') as f:
            pickle.dump(self.scaler, f)
        
        with open(f'{output_dir}/label_encoder.pkl', 'wb') as f:
            pickle.dump(self.label_encoder, f)
        
        with open(f'{output_dir}/feature_names.pkl', 'wb') as f:
            pickle.dump(self.feature_names, f)
        
        print(f"\nSaved preprocessors to {output_dir}/")
    
    def get_attack_names(self):
        """Get list of attack names"""
        return self.label_encoder.classes_.tolist()


def main():
    """Main preprocessing pipeline"""
    import gc
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor()
    
    # Load data with sampling to reduce memory usage
    # Sample 60K records per file = ~480K total records
    df = preprocessor.load_cic_ids_data(sample_per_file=100000)  # Increased for better accuracy
    
    # Clean data
    df = preprocessor.clean_data(df)
    
    # Free memory
    gc.collect()
    
    # Select features
    X, y = preprocessor.select_features(df, n_features=40)
    
    # Free memory
    del df
    gc.collect()
    
    # Preprocess (with sampling if needed)
    X_train, X_test, y_train, y_test = preprocessor.preprocess_data(
        X, y, apply_smote=True, max_samples=800000  # Increased for better accuracy
    )
    
    # Free memory
    del X, y
    gc.collect()
    
    # Create sequences for LSTM
    X_train_seq, y_train_seq = preprocessor.create_sequences(
        X_train, y_train, sequence_length=10, max_sequences=300000  # Increased for better accuracy
    )
    X_test_seq, y_test_seq = preprocessor.create_sequences(
        X_test, y_test, sequence_length=10, max_sequences=100000  # Increased for better accuracy
    )
    
    # Free memory
    del X_train, X_test, y_train, y_test
    gc.collect()
    
    # Save preprocessed data
    print("\nSaving preprocessed data...")
    os.makedirs('data/processed', exist_ok=True)
    
    np.save('data/processed/X_train.npy', X_train_seq)
    np.save('data/processed/X_test.npy', X_test_seq)
    np.save('data/processed/y_train.npy', y_train_seq)
    np.save('data/processed/y_test.npy', y_test_seq)
    
    # Save preprocessors
    preprocessor.save_preprocessors()
    
    # Print summary
    print("\n" + "="*60)
    print("PREPROCESSING COMPLETE")
    print("="*60)
    print(f"Training sequences: {X_train_seq.shape}")
    print(f"Testing sequences: {X_test_seq.shape}")
    print(f"Number of classes: {len(preprocessor.get_attack_names())}")
    print(f"Attack types: {preprocessor.get_attack_names()}")
    print("="*60)
    print("\nNext step: Train the model")
    print("  python src/cnn_lstm_model.py")


if __name__ == "__main__":
    main()
