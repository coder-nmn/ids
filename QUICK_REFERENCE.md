# 🚀 Quick Reference Card

## Start Dashboard
```bash
streamlit run app.py
```
Opens at: `http://localhost:8501`

---

## Dashboard Tabs

| Tab | Purpose | Key Features |
|-----|---------|--------------|
| 🏠 Dashboard | Overview | Stats, charts, recent detections |
| 📁 File Upload | Batch analysis | Upload CSV, get predictions |
| 🔴 Real-Time | Live detection | Manual input or JSON API |
| 📊 Performance | Model info | Metrics, architecture, training |
| 📜 History | **All detections** | **Filter, export, view details** |
| 🔧 API Docs | Integration | Hardware guide, examples |

---

## Key Features

### ✅ What Works
- Real-time detection (<50ms)
- Batch file processing
- **Persistent database storage**
- **Complete detection history**
- Export to CSV
- 14 attack types
- 87.74% accuracy

### 💾 Data Persistence
- **Every prediction is saved**
- **Data survives restarts**
- **Access history anytime**
- **Export anytime**

---

## Quick Commands

```bash
# Start dashboard
streamlit run app.py

# Test everything
python test_all_features.py

# Quick test
python test_prediction.py

# Check status
python check_status.py

# Verify model
python verify_model.py
```

---

## Database

**Location**: `data/ids_history.db`

**What's Saved**:
- Timestamp
- Attack type
- Confidence
- All 40 features
- Probabilities
- IPs
- Risk level
- Notes

---

## Attack Types (14)

1. Benign
2. Bot
3. DDoS
4. DoS (4 variants)
5. FTP-Patator
6. Infiltration
7. PortScan
8. SSH-Patator
9. Web Attacks (3 types)

---

## Model Stats

- **Accuracy**: 87.74%
- **Features**: 40
- **Classes**: 14
- **Speed**: <50ms

---

## Files

| File | Purpose |
|------|---------|
| `app.py` | Dashboard |
| `database.py` | Database module |
| `data/ids_history.db` | Detection database |
| `models/*.pkl` | Preprocessors |
| `models/*.h5` | Trained model |

---

## Export Data

1. Go to "Detection History" tab
2. Click "Export All to CSV" or "Export Filtered"
3. Download the file

---

## View History

1. Go to "Detection History" tab
2. See all past detections
3. Filter by attack type or risk level
4. View detailed individual records
5. See probability distributions

---

## Hardware Integration

Send JSON POST to dashboard:
```json
{
    "features": [0.0, 0.0, ...],  // 40 values
    "source_ip": "192.168.1.100",
    "destination_ip": "192.168.1.1"
}
```

See API Documentation tab for details.

---

## Troubleshooting

**Dashboard won't start?**
```bash
python check_status.py
```

**Need to reset database?**
```bash
del data\ids_history.db
```

**Model issues?**
```bash
python verify_model.py
```

---

## Status: ✅ FULLY OPERATIONAL

All features tested and working!

**Last Updated**: December 7, 2025
