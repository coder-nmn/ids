# 🚀 Quick Start - Daily Upload & Tracking

## What You Want
Upload 1 CSV file per day for 7 days and see:
- ✅ What attack types happened each day
- ✅ How accurate the model was each day
- ✅ Weekly trends and patterns
- ✅ Complete detailed analytics

## 3 Simple Steps

### 1️⃣ Generate 7 Days of Data (One-time)
```bash
python generate_daily_data.py
```
**Output**: Creates `daily_data/` folder with 7 CSV files (one per day)

### 2️⃣ Start the App
```bash
streamlit run app.py
```

### 3️⃣ Upload & Track
1. Select **"📅 Daily Upload & Tracking"** from sidebar
2. Choose **"Day 1 - Monday"**
3. Upload `daily_data/day_1_*.csv`
4. Click **"🔍 Analyze This Day"**
5. See results! ✅

**Repeat for Day 2, Day 3... Day 7**

## What You'll See

### After Each Day Upload:
```
📊 Day 1 Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Records:     500
Attacks Detected:  150 (30%)
Benign Traffic:    350 (70%)
Accuracy:          95.2%

🎯 Attack Types Today:
  - PortScan: 45
  - DDoS: 30
  - Web Attack: 25
  - Bot: 20
  - Others: 30
```

### After All 7 Days:
```
📈 WEEKLY SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Days Tracked:      7
Total Records:     3,500
Attacks Detected:  1,400 (40%)
Average Accuracy:  96.5%

📊 Trends:
  - Wednesday: Highest attacks (45%)
  - Saturday: Lowest attacks (18%)
  - Most common: DDoS attacks
  - Accuracy improved over week
```

## Visual Analytics You Get

### 1. Daily Attack Distribution (Pie Chart)
Shows what % of each attack type occurred that day

### 2. Weekly Attack Trend (Line Chart)
Shows attacks vs benign traffic over 7 days

### 3. Daily Accuracy (Bar Chart)
Shows model accuracy for each day

### 4. Attack Rate Trend (Line Chart)
Shows attack percentage over the week

### 5. Overall Attack Types (Pie + Bar Charts)
Shows total distribution across all 7 days

## Example Daily Pattern

```
Day 1 (Monday):    Normal traffic, 30% attacks
Day 2 (Tuesday):   Port scanning, 36% attacks
Day 3 (Wednesday): DDoS attack, 45% attacks ⚠️
Day 4 (Thursday):  Normal traffic, 28% attacks
Day 5 (Friday):    Web attacks, 42% attacks
Day 6 (Saturday):  Low activity, 18% attacks
Day 7 (Sunday):    Bot activity, 50% attacks ⚠️
```

## Download Options

After analysis, you can download:
- ✅ Individual day results (CSV)
- ✅ Weekly summary (CSV)
- ✅ Complete analysis with predictions

## Clear & Restart

Click **"🗑️ Clear All Data"** to start fresh with new data

## That's It! 🎉

You now have:
- ✅ 7 days of network traffic data
- ✅ Daily attack analysis
- ✅ Accuracy tracking
- ✅ Weekly trends
- ✅ Complete detailed reports

---

## Need More Details?
Read the full guide: `DAILY_TRACKING_GUIDE.md`

## Questions?
- Check the app's sidebar for other modes
- Try "📊 EDA" for deeper analysis
- Use "🔴 Real-Time Detection" for live monitoring
