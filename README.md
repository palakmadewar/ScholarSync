# ScholarSync personal agent

**ScholarSync** is an intelligent app that helps learners track, analyze, and improve their study habits using **AI and Machine Learning**.  
It predicts your expected productivity, shows trends, and gives insights to make your study sessions more effective.

---

## Why This Project?

Many students struggle to organize their study time, track progress, and understand what helps them study better.  
This app provides a **personalized study assistant** to:

- Log study sessions easily  
- Track productivity trends  
- Estimate how productive a session will be  
- Get insights to improve learning efficiency

---

## How It Works

1. **Log Study Sessions:**  
   Enter your study details like subject, duration, mood, distractions, caffeine, and study technique.  

2. **Analyze Productivity:**  
   The app uses a **Random Forest ML model** to predict your productivity based on past sessions.  

3. **View Insights:**  
   See charts and KPIs:  
   - Time spent per subject  
   - Productivity trends  
   - Best study techniques  

4. **Make Smarter Plans:**  
   Understand what works best for you and optimize future sessions.

---

## Features

- Log study sessions with mood, distractions, caffeine, and technique  
- Predict productivity in real-time  
- Visualize study time and performance trends  
- Local SQLite database ensures privacy  
- Clean, interactive Streamlit dashboard  

---

## Hackathon Integration (Haulout Hackathon 2025)

This project aligns with the Haulout Hackathon theme:

1. **Data Management (Walrus):**  
   Study session data can be securely stored on **Walrus decentralized storage**, ensuring tamper-proof and reliable access.  

2. **Data Verification (Seal):**  
   Each session can be cryptographically verified using **Seal**, confirming authenticity.  

3. **Marketplace / Monetisation (Nautilus):**  
   Aggregated insights or anonymized study analytics can be shared or monetized via **Nautilus**, creating opportunities for verified educational data.  

> **Note:** The core AI Study Tracker code is unchanged; this section shows alignment with hackathon themes.

---

## Quickstart

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-study-tracker.git
cd ai-study-tracker

# Create virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate sample data
python src/generate_sample.py --days 28 --sessions_per_day 2 --out data/sessions.csv

# Import data to SQLite
python src/ingest.py --csv data/sessions.csv --db data/study.db --schema sql/schema.sql

# Train the ML model
python src/train_model.py --db data/study.db --out models/pipeline.joblib

# Launch the dashboard
streamlit run app/streamlit_app.py

