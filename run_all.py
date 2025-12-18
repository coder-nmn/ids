"""
Quick Start Script
Runs the complete IDS pipeline: preprocessing → training → dashboard
"""

import os
import sys
import subprocess
import time

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(command, description):
    """Run a command and handle errors"""
    print_header(description)
    print(f"Running: {command}\n")
    
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with error: {e}")
        return False

def check_dataset():
    """Check if dataset exists"""
    dataset_path = "Datasets/Datasets/cic-ids"
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at {dataset_path}")
        print("Please ensure CIC-IDS dataset is in the correct location.")
        return False
    
    # Check for parquet files
    parquet_files = [f for f in os.listdir(dataset_path) if f.endswith('.parquet')]
    if len(parquet_files) == 0:
        print(f"❌ No parquet files found in {dataset_path}")
        return False
    
    print(f"✅ Found {len(parquet_files)} parquet files in dataset")
    return True

def main():
    print_header("IDS System - Quick Start")
    
    print("""
    This script will:
    1. Check dataset availability
    2. Preprocess data (CIC-IDS)
    3. Train CNN-LSTM model
    4. Launch Streamlit dashboard
    
    Estimated time: 2-6 hours (depending on hardware)
    """)
    
    response = input("Do you want to continue? (y/n): ")
    if response.lower() != 'y':
        print("Aborted.")
        return
    
    # Step 1: Check dataset
    print_header("Step 1: Checking Dataset")
    if not check_dataset():
        print("\n❌ Dataset check failed. Please fix the issues and try again.")
        return
    
    # Step 2: Preprocess data
    if not os.path.exists('data/processed/X_train.npy'):
        if not run_command("python src/data_preprocessing.py", "Step 2: Data Preprocessing"):
            return
    else:
        print_header("Step 2: Data Preprocessing")
        print("✅ Preprocessed data already exists. Skipping...")
    
    # Step 3: Train model
    if not os.path.exists('models/cnn_lstm_final.h5'):
        if not run_command("python src/cnn_lstm_model.py", "Step 3: Model Training"):
            return
    else:
        print_header("Step 3: Model Training")
        print("✅ Trained model already exists. Skipping...")
    
    # Step 4: Launch dashboard
    print_header("Step 4: Launching Streamlit Dashboard")
    print("Dashboard will open at http://localhost:8501")
    print("Press Ctrl+C to stop the dashboard\n")
    
    time.sleep(2)
    
    try:
        subprocess.run("streamlit run app.py", shell=True)
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard stopped.")
    
    print_header("Setup Complete!")
    print("""
    Your IDS system is ready!
    
    To run the dashboard again:
        streamlit run app.py
    
    To retrain the model:
        python src/cnn_lstm_model.py
    
    To reprocess data:
        python src/data_preprocessing.py
    """)

if __name__ == "__main__":
    main()
