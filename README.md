# ScholarSync personal agent

**ScholarSync** is an intelligent app that helps learners track, analyze, and improve their study habits using **AI and Machine Learning**.
It predicts your expected productivity, shows trends, and gives insights to make your study sessions more effective.

---

## Why This Project?

Many students struggle to organize their study time, track progress, and understand what helps them study better.
This app provides a **personalized study assistant** to:

* Log study sessions easily
* Track productivity trends
* Estimate how productive a session will be
* Get insights to improve learning efficiency

---

## How It Works

1. **Log Study Sessions:**
   Enter your study details like subject, duration, mood, distractions, caffeine, and study technique.

2. **Analyze Productivity:**
   The app uses a **Random Forest ML model** to predict your productivity based on past sessions.

3. **View Insights:**
   See charts and KPIs:

   * Time spent per subject
   * Productivity trends
   * Best study techniques

4. **Make Smarter Plans:**
   Understand what works best for you and optimize future sessions.

---

## Features

* Log study sessions with mood, distractions, caffeine, and technique
* Predict productivity in real-time
* Visualize study time and performance trends
* Local SQLite database ensures privacy
* Clean, interactive Streamlit dashboard

---

## 🌐 Decentralized AI + On-Chain Data (AI x Data Hackathon)

### 🚀 New Vision

Students contribute study data to train a **global decentralized productivity model**. Their updates are **secured on-chain**, enabling:

* Privacy-preserving learning
* Transparency in contribution
* Token rewards for improving the AI

> **“Democratizing AI Training — Powered by Students, Secured by Blockchain.”**

### 🔍 Why Blockchain?

* Ensures **authentic and verifiable** contributions (on-chain storage of model update proofs)
* Removes central control over data and model
* Enables **token incentives** for contributors

### 🧠 Decentralized AI Workflow

1. User logs a study session
2. Model trains locally on their device (Federated Learning)
3. Model update (weights/gradients) stored on-chain
4. Updated global model shared back to all users
5. Contributors **earn tokens** for improving model performance

### 🏗️ Architecture Overview

* Local device: study data + local model training
* Smart Contract: record updates + token rewards
* IPFS / Decentralized storage: hashed data & model checkpoints
* Streamlit dApp: UI for logging + wallet interaction

### 🔗 Web3 Features

* Wallet login using MetaMask
* Token balance display
* Secure on-chain contribution history

---

## Quickstart

```bash
# Clone the repository
git clone https://github.com/yourusername/ScholarSync.git
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
```
