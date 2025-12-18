"""
Database Module for IDS
Stores all detection history persistently
"""

import sqlite3
import json
import pandas as pd
from datetime import datetime
import os

class IDSDatabase:
    def __init__(self, db_path='data/ids_history.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Detections table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                attack_type TEXT NOT NULL,
                confidence REAL NOT NULL,
                source_ip TEXT,
                destination_ip TEXT,
                features TEXT,
                probabilities TEXT,
                risk_level TEXT,
                notes TEXT
            )
        ''')
        
        # Statistics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total_detections INTEGER DEFAULT 0,
                attack_count INTEGER DEFAULT 0,
                benign_count INTEGER DEFAULT 0,
                avg_confidence REAL DEFAULT 0.0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_detection(self, attack_type, confidence, features=None, probabilities=None, 
                     source_ip=None, destination_ip=None, notes=None):
        """Add a new detection record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        
        # Determine risk level
        if confidence > 0.9:
            risk_level = 'High'
        elif confidence > 0.7:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        # Convert features and probabilities to JSON
        features_json = json.dumps(features) if features else None
        probabilities_json = json.dumps(probabilities.tolist() if hasattr(probabilities, 'tolist') else probabilities) if probabilities is not None else None
        
        cursor.execute('''
            INSERT INTO detections 
            (timestamp, attack_type, confidence, source_ip, destination_ip, 
             features, probabilities, risk_level, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, attack_type, confidence, source_ip, destination_ip,
              features_json, probabilities_json, risk_level, notes))
        
        conn.commit()
        detection_id = cursor.lastrowid
        conn.close()
        
        # Update statistics
        self.update_statistics()
        
        return detection_id
    
    def get_all_detections(self, limit=None):
        """Get all detection records"""
        conn = sqlite3.connect(self.db_path)
        
        query = 'SELECT * FROM detections ORDER BY timestamp DESC'
        if limit:
            query += f' LIMIT {limit}'
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def get_detections_by_date(self, start_date, end_date):
        """Get detections within date range"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT * FROM detections 
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp DESC
        '''
        
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        
        return df
    
    def get_detections_by_attack_type(self, attack_type):
        """Get detections by attack type"""
        conn = sqlite3.connect(self.db_path)
        
        query = 'SELECT * FROM detections WHERE attack_type = ? ORDER BY timestamp DESC'
        df = pd.read_sql_query(query, conn, params=(attack_type,))
        conn.close()
        
        return df
    
    def get_statistics(self):
        """Get overall statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total detections
        cursor.execute('SELECT COUNT(*) FROM detections')
        total_detections = cursor.fetchone()[0]
        
        # Attack count
        cursor.execute("SELECT COUNT(*) FROM detections WHERE attack_type != 'Benign'")
        attack_count = cursor.fetchone()[0]
        
        # Benign count
        cursor.execute("SELECT COUNT(*) FROM detections WHERE attack_type = 'Benign'")
        benign_count = cursor.fetchone()[0]
        
        # Average confidence
        cursor.execute('SELECT AVG(confidence) FROM detections')
        avg_confidence = cursor.fetchone()[0] or 0.0
        
        # Attack distribution
        cursor.execute('''
            SELECT attack_type, COUNT(*) as count 
            FROM detections 
            GROUP BY attack_type 
            ORDER BY count DESC
        ''')
        attack_distribution = cursor.fetchall()
        
        # Recent detections
        cursor.execute('''
            SELECT timestamp, attack_type, confidence, risk_level
            FROM detections 
            ORDER BY timestamp DESC 
            LIMIT 10
        ''')
        recent_detections = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_detections': total_detections,
            'attack_count': attack_count,
            'benign_count': benign_count,
            'avg_confidence': avg_confidence,
            'attack_distribution': attack_distribution,
            'recent_detections': recent_detections
        }
    
    def update_statistics(self):
        """Update daily statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().date().isoformat()
        
        # Get today's stats
        cursor.execute('''
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN attack_type != 'Benign' THEN 1 ELSE 0 END) as attacks,
                   SUM(CASE WHEN attack_type = 'Benign' THEN 1 ELSE 0 END) as benign,
                   AVG(confidence) as avg_conf
            FROM detections
            WHERE DATE(timestamp) = ?
        ''', (today,))
        
        stats = cursor.fetchone()
        
        # Update or insert
        cursor.execute('''
            INSERT OR REPLACE INTO statistics 
            (date, total_detections, attack_count, benign_count, avg_confidence)
            VALUES (?, ?, ?, ?, ?)
        ''', (today, stats[0], stats[1] or 0, stats[2] or 0, stats[3] or 0.0))
        
        conn.commit()
        conn.close()
    
    def get_attack_timeline(self, hours=24):
        """Get attack timeline for last N hours"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                strftime('%Y-%m-%d %H:00:00', timestamp) as hour,
                attack_type,
                COUNT(*) as count
            FROM detections
            WHERE datetime(timestamp) >= datetime('now', '-' || ? || ' hours')
            GROUP BY hour, attack_type
            ORDER BY hour DESC
        '''
        
        df = pd.read_sql_query(query, conn, params=(hours,))
        conn.close()
        
        return df
    
    def clear_all_data(self):
        """Clear all detection data (use with caution!)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM detections')
        cursor.execute('DELETE FROM statistics')
        
        conn.commit()
        conn.close()
    
    def export_to_csv(self, filepath='data/detections_export.csv'):
        """Export all detections to CSV"""
        df = self.get_all_detections()
        df.to_csv(filepath, index=False)
        return filepath
    
    def get_detection_by_id(self, detection_id):
        """Get specific detection by ID"""
        conn = sqlite3.connect(self.db_path)
        
        query = 'SELECT * FROM detections WHERE id = ?'
        df = pd.read_sql_query(query, conn, params=(detection_id,))
        conn.close()
        
        if len(df) > 0:
            return df.iloc[0].to_dict()
        return None
