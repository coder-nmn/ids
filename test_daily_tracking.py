"""
Test Daily Tracking Feature
Quick verification that everything works
"""

import pandas as pd
import os
from daily_tracking import DailyTracker

def test_data_files():
    """Test that all daily CSV files exist and are valid"""
    print("🔍 Testing Daily Data Files...")
    print("=" * 60)
    
    for day in range(1, 8):
        files = [f for f in os.listdir('daily_data') if f.startswith(f'day_{day}_')]
        
        if not files:
            print(f"❌ Day {day}: No file found")
            continue
        
        filepath = os.path.join('daily_data', files[0])
        
        try:
            df = pd.read_csv(filepath)
            attack_counts = df['Label'].value_counts()
            benign = attack_counts.get('BENIGN', 0)
            attacks = len(df) - benign
            
            print(f"✅ Day {day}: {len(df)} records, {attacks} attacks ({attacks/len(df)*100:.1f}%)")
            print(f"   Top 3 attacks: {', '.join(attack_counts.index[1:4].tolist())}")
        
        except Exception as e:
            print(f"❌ Day {day}: Error - {e}")
    
    print("=" * 60)

def test_tracker():
    """Test the DailyTracker class"""
    print("\n🔍 Testing DailyTracker...")
    print("=" * 60)
    
    # Create test tracker
    tracker = DailyTracker(storage_file='test_tracking.json')
    
    # Clear any existing data
    tracker.clear_all()
    print("✅ Tracker initialized")
    
    # Add test day
    test_stats = {
        'total_records': 500,
        'total_attacks': 150,
        'total_benign': 350,
        'attack_rate': 30.0,
        'accuracy': 95.5,
        'avg_confidence': 95.5,
        'attack_distribution': {'DDoS': 50, 'PortScan': 40, 'Bot': 30, 'BENIGN': 350},
        'top_attack': 'DDoS'
    }
    
    tracker.add_day('Day 1 - Monday', '2024-12-02', test_stats)
    print("✅ Test day added")
    
    # Get summary
    summary = tracker.get_summary()
    if summary:
        print(f"✅ Summary retrieved:")
        print(f"   Total days: {summary['total_days']}")
        print(f"   Total records: {summary['total_records']}")
        print(f"   Total attacks: {summary['total_attacks']}")
        print(f"   Avg accuracy: {summary['avg_accuracy']:.1f}%")
    
    # Clean up
    tracker.clear_all()
    if os.path.exists('test_tracking.json'):
        os.remove('test_tracking.json')
    print("✅ Cleanup complete")
    
    print("=" * 60)

def test_app_integration():
    """Test that app.py has the new mode"""
    print("\n🔍 Testing App Integration...")
    print("=" * 60)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '📅 Daily Upload & Tracking' in content:
            print("✅ Daily Upload mode found in app.py")
        else:
            print("❌ Daily Upload mode NOT found in app.py")
        
        if 'from daily_tracking import show_daily_upload_tracking' in content:
            print("✅ Import statement found")
        else:
            print("❌ Import statement NOT found")
        
        if 'show_daily_upload_tracking(model, scaler, label_encoder, feature_names)' in content:
            print("✅ Function call found")
        else:
            print("❌ Function call NOT found")
    
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
    
    print("=" * 60)

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 DAILY TRACKING FEATURE TEST")
    print("=" * 60 + "\n")
    
    # Test 1: Data files
    test_data_files()
    
    # Test 2: Tracker class
    test_tracker()
    
    # Test 3: App integration
    test_app_integration()
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETE!")
    print("=" * 60)
    print("\n💡 Next Steps:")
    print("   1. Run: streamlit run app.py")
    print("   2. Select: 📅 Daily Upload & Tracking")
    print("   3. Upload files from daily_data/ folder")
    print("   4. Enjoy your daily tracking! 🎉\n")

if __name__ == "__main__":
    main()
