"""
System Test Script
Verifies that all components are working correctly
"""

import os
import sys
import numpy as np

def print_status(message, status):
    """Print colored status message"""
    if status:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    return status

def test_dependencies():
    """Test if all dependencies are installed"""
    print("\n" + "="*60)
    print("Testing Dependencies")
    print("="*60)
    
    required_packages = [
        'pandas', 'numpy', 'sklearn', 'tensorflow',
        'streamlit', 'plotly', 'imblearn', 'xgboost'
    ]
    
    all_ok = True
    for package in required_packages:
        try:
            __import__(package)
            print_status(f"{package} installed", True)
        except ImportError:
            print_status(f"{package} NOT installed", False)
            all_ok = False
    
    return all_ok

def test_dataset():
    """Test if dataset exists"""
    print("\n" + "="*60)
    print("Testing Dataset")
    print("="*60)
    
    dataset_path = "Datasets/Datasets/cic-ids"
    
    if not os.path.exists(dataset_path):
        print_status(f"Dataset directory exists: {dataset_path}", False)
        return False
    
    print_status(f"Dataset directory exists: {dataset_path}", True)
    
    # Check for parquet files
    parquet_files = [f for f in os.listdir(dataset_path) if f.endswith('.parquet')]
    
    if len(parquet_files) == 0:
        print_status("Parquet files found", False)
        return False
    
    print_status(f"Found {len(parquet_files)} parquet files", True)
    
    # List files
    for f in parquet_files:
        file_path = os.path.join(dataset_path, f)
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        print(f"  - {f} ({size_mb:.2f} MB)")
    
    return True

def test_preprocessed_data():
    """Test if preprocessed data exists"""
    print("\n" + "="*60)
    print("Testing Preprocessed Data")
    print("="*60)
    
    required_files = [
        'data/processed/X_train.npy',
        'data/processed/X_test.npy',
        'data/processed/y_train.npy',
        'data/processed/y_test.npy'
    ]
    
    all_ok = True
    for file in required_files:
        exists = os.path.exists(file)
        print_status(f"{file} exists", exists)
        if not exists:
            all_ok = False
    
    if not all_ok:
        print("\n⚠️  Run preprocessing first: python src/data_preprocessing.py")
    
    return all_ok

def test_model():
    """Test if trained model exists"""
    print("\n" + "="*60)
    print("Testing Trained Model")
    print("="*60)
    
    required_files = [
        'models/cnn_lstm_final.h5',
        'models/scaler.pkl',
        'models/label_encoder.pkl',
        'models/feature_names.pkl'
    ]
    
    all_ok = True
    for file in required_files:
        exists = os.path.exists(file)
        if exists and file.endswith('.h5'):
            size_mb = os.path.getsize(file) / (1024 * 1024)
            print_status(f"{file} exists ({size_mb:.2f} MB)", True)
        else:
            print_status(f"{file} exists", exists)
        
        if not exists:
            all_ok = False
    
    if not all_ok:
        print("\n⚠️  Run training first: python src/cnn_lstm_model.py")
    
    return all_ok

def test_model_loading():
    """Test if model can be loaded"""
    print("\n" + "="*60)
    print("Testing Model Loading")
    print("="*60)
    
    try:
        import tensorflow as tf
        import pickle
        
        # Load model
        model = tf.keras.models.load_model('models/cnn_lstm_final.h5')
        print_status("Model loaded successfully", True)
        
        # Load preprocessors
        with open('models/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        print_status("Scaler loaded successfully", True)
        
        with open('models/label_encoder.pkl', 'rb') as f:
            label_encoder = pickle.load(f)
        print_status("Label encoder loaded successfully", True)
        
        with open('models/feature_names.pkl', 'rb') as f:
            feature_names = pickle.load(f)
        print_status(f"Feature names loaded ({len(feature_names)} features)", True)
        
        # Test prediction
        print("\nTesting prediction...")
        dummy_features = np.zeros((1, 10, len(feature_names)))
        prediction = model.predict(dummy_features, verbose=0)
        pred_class = np.argmax(prediction[0])
        attack_name = label_encoder.inverse_transform([pred_class])[0]
        
        print_status(f"Prediction test successful: {attack_name}", True)
        
        return True
    
    except Exception as e:
        print_status(f"Model loading failed: {e}", False)
        return False

def test_streamlit():
    """Test if Streamlit app can be imported"""
    print("\n" + "="*60)
    print("Testing Streamlit App")
    print("="*60)
    
    if not os.path.exists('app.py'):
        print_status("app.py exists", False)
        return False
    
    print_status("app.py exists", True)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print_status("Streamlit installed", True)
        print(f"  Version: {streamlit.__version__}")
        return True
    except ImportError:
        print_status("Streamlit NOT installed", False)
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("IDS SYSTEM TEST")
    print("="*60)
    
    results = {
        'Dependencies': test_dependencies(),
        'Dataset': test_dataset(),
        'Preprocessed Data': test_preprocessed_data(),
        'Trained Model': test_model(),
        'Model Loading': test_model_loading(),
        'Streamlit App': test_streamlit()
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results.items():
        print_status(test_name, result)
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nYour IDS system is ready to use!")
        print("\nTo launch the dashboard:")
        print("  streamlit run app.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("="*60)
        print("\nPlease fix the issues above before running the dashboard.")
        print("\nQuick fixes:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Preprocess data: python src/data_preprocessing.py")
        print("  3. Train model: python src/cnn_lstm_model.py")
        print("\nOr run the quick start script:")
        print("  python run_all.py")
    
    print("="*60 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
