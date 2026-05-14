# 🧠 AI-Fraud-Detection-System 🚀

---

## 🔥 Project Overview

This project is a **real-time AI-powered fraud detection system** that combines:

- 🧠 Machine Learning (Isolation Forest)
- 🎥 Computer Vision (OpenCV)
- ✋ Gesture Recognition (MediaPipe)
- 📊 Live Risk Visualization Dashboard
- ⚡ Real-time transaction simulation engine

It simulates financial transactions and detects fraudulent activity in real time using AI + webcam interaction.

---

## ⚙️ How It Works

💳 Transactions are read from dataset (`creditcard.csv`)  
🧠 AI model analyzes each transaction for anomalies  
📊 Each transaction gets a **risk score (0–100%)**  
🎥 Webcam tracks hand movements in real time  
✋ Gestures control system behavior  

The system provides a **live cyber-security style dashboard** with dynamic updates.

---

## ✋ Gesture Controls

| Gesture | Action |
|--------|--------|
| 👉 Swipe Right | Next transaction |
| 👈 Swipe Left | Previous transaction |
| ✊ Fist + Finger Close | 🚨 Trigger Fraud Alert |

---

## 🧠 AI Model Details

- Algorithm: Isolation Forest
- Type: Unsupervised Anomaly Detection
- Features Used:
  - Time
  - Amount
- Preprocessing: StandardScaler
- Output: Fraud probability → converted into risk score (0–100%)

---

## 📊 Risk Levels

🟢 SAFE → Normal transaction behavior  
🟠 SUSPICIOUS → Slight anomaly detected  
🔴 HIGH RISK → Strong fraud indication  

---

## ⚡ Key Features

✔ Real-time fraud detection engine  
✔ AI-based anomaly scoring system  
✔ Gesture-controlled interface (hands-free control)  
✔ Live transaction feed UI  
✔ Dynamic risk graph visualization  
✔ Fraud alert system with sound 🔊  
✔ Cyber-security inspired dashboard design  
✔ Smooth cinematic UI experience  

---

## 🛠️ Tech Stack

- 🐍 Python
- 🎥 OpenCV
- ✋ MediaPipe
- 🧠 Scikit-learn
- 📊 Pandas
- 🔢 NumPy
- 🔊 Playsound
- 🧵 Threading

---

## 📁 Project Structure
AI-Fraud-Detection-System/
│
├── main.py # Main application (AI + CV system)
├── creditcard.csv # Transaction dataset
├── alert.mp3 # Fraud alert sound
├── requirements.txt # Python dependencies
└── README.md # Project documentation

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
python main.py

## ⚠️ Notes

- Ensure good lighting for webcam detection
- Make sure `alert.mp3` exists in project folder
- Dataset `creditcard.csv` must be present
- Run on a system with decent performance for smooth real-time processing
