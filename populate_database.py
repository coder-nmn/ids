"""
Populate Database with Sample Detections
Run this to add sample data to the dashboard
"""

from database import IDSDatabase
import numpy as np
from datetime import datetime, timedelta

print("Populating database with sample detections...")

db = IDSDatabase()

# Sample attack types
attack_types = ['Benign', 'DDoS', 'PortScan', 'Bot', 'DoS Hulk']

# Add 20 sample detections
for i in range(20):
    attack = np.random.choice(attack_types, p=[0.7, 0.1, 0.1, 0.05, 0.05])
    confidence = 0.96 + (np.random.random() * 0.04)  # 96-100%
    
    # Random features
    features = [np.random.random() * 100 for _ in range(40)]
    probabilities = np.random.random(14)
    probabilities = probabilities / probabilities.sum()  # Normalize
    
    db.add_detection(
        attack_type=attack,
        confidence=confidence,
        features=features,
        probabilities=probabilities,
        source_ip=f"192.168.1.{100+i}",
        destination_ip="192.168.1.1",
        notes=f"Sample detection {i+1}"
    )
    
    print(f"Added detection {i+1}: {attack} ({confidence:.2%})")

print("\n✅ Database populated!")
print(f"\nTotal detections: {db.get_statistics()['total_detections']}")
print("\nRefresh your dashboard to see the data!")
