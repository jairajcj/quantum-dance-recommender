# Quantum Dance Emotion Recommender

AI-powered emotion analysis for dance videos using classical and quantum-inspired recommendation models.

**🌐 Live Demo**: [https://jairajcj.github.io/quantum-dance-recommender/](https://jairajcj.github.io/quantum-dance-recommender/)  
**📦 GitHub**: [https://github.com/jairajcj/quantum-dance-recommender](https://github.com/jairajcj/quantum-dance-recommender)

---

## 🚀 Quick Start Guide

### Prerequisites

Before you begin, make sure you have:
- **Python 3.7 or higher** installed ([Download Python](https://www.python.org/downloads/))
- **pip** (Python package manager - comes with Python)
- A terminal/command prompt

### Step 1: Check Python Installation

Open your terminal and verify Python is installed:

```bash
python --version
```

You should see something like `Python 3.x.x`. If not, install Python first.

### Step 2: Clone or Download the Repository

**Option A: Clone with Git**
```bash
git clone https://github.com/jairajcj/quantum-dance-recommender.git
cd quantum-dance-recommender
```

**Option B: Download ZIP**
1. Download the ZIP from GitHub
2. Extract it to a folder
3. Open terminal in that folder

### Step 3: Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

This installs:
- `Flask` - Web framework
- `opencv-python` - Video processing
- `numpy` - Numerical computing
- `scipy` - Scientific computing
- `werkzeug` - File handling

### Step 4: Run the Application

Start the Flask server:

```bash
python app.py
```

You should see:
```
Starting Quantum Dance Emotion Recommender...
Open http://localhost:5000 in your browser
 * Running on http://127.0.0.1:5000
```

### Step 5: Open in Browser

Open your web browser and go to:

**http://localhost:5000**

### Step 6: Upload and Analyze!

1. Click the upload area
2. Select a dance video (MP4, AVI, MOV, MKV, WEBM)
3. Wait for processing (a few seconds)
4. View emotion analysis and dance recommendations!

### Step 7: Stop the Server

When you're done, press `Ctrl+C` in the terminal to stop the server.

---

## 📋 Troubleshooting

### "Python not found"
- Install Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

### "pip not found"
```bash
python -m ensurepip --upgrade
```

### "Module not found" errors
```bash
pip install -r requirements.txt --upgrade
```

### Port 5000 already in use
Change the port in `app.py` (last line):
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use port 5001 instead
```

---

## 🎯 How It Works

### Video Analysis
- Uses **OpenCV optical flow** to track movement
- Calculates velocity, acceleration, and motion patterns
- Detects faces using Haar Cascade classifier

### Emotion Detection
- **Movement-based emotions**: energetic, calm, aggressive, graceful, playful, melancholic
- **Facial emotions**: happy, sad, angry, surprise, neutral, fear, disgust
- Combines both for comprehensive emotion profile

### Recommendation Models

**Classical Model**
- Traditional weighted scoring
- Direct emotion-to-dance mappings
- Fast and interpretable

**Quantum-Inspired Model**
- Uses quantum computing concepts
- Superposition of emotion states
- Entanglement correlations
- Probability amplitude calculations

---

## 📁 Project Structure

```
quantum-dance-recommender/
├── app.py              # Main Flask application (all-in-one)
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── index.html         # GitHub Pages demo (static)
├── .gitignore         # Git ignore rules
└── uploads/           # Temporary video storage (auto-created)
```

---

## 🎨 Features

- ✅ Real-time video processing
- ✅ Emotion detection (facial + movement)
- ✅ Classical AI recommendations
- ✅ Quantum-inspired recommendations
- ✅ Beautiful quantum-themed UI
- ✅ Supports multiple video formats
- ✅ Fast processing with frame sampling
- ✅ In-memory caching for performance

---

## 🛠️ Customization

Edit `app.py` to customize:

- **Add dance styles** (line 25): Add to `DANCE_STYLES` list
- **Emotion mappings** (line 151): Modify `EMOTION_DANCE_MAP`
- **UI colors** (line 311+): Change CSS gradient colors
- **Quantum parameters** (line 182+): Adjust dimensions, phases
- **Frame sampling** (line 21): Change `FRAME_SAMPLE_RATE`

---

## 📊 Performance

- **Lightweight**: ~200MB total install size
- **Fast**: Processes videos in seconds
- **Efficient**: Frame sampling (every 5th frame)
- **Smart**: In-memory caching for repeated analyses

---

## 🌐 Deployment

### Local Development
```bash
python app.py
```

### GitHub Pages (Static Demo Only)
The static demo is already live at:
[https://jairajcj.github.io/quantum-dance-recommender/](https://jairajcj.github.io/quantum-dance-recommender/)

### Production Deployment
For full functionality, deploy to a Python hosting service:
- **Render** ([render.com](https://render.com))
- **Railway** ([railway.app](https://railway.app))
- **PythonAnywhere** ([pythonanywhere.com](https://www.pythonanywhere.com))
- **Heroku** ([heroku.com](https://www.heroku.com))

---

## 📝 License

This project is open source and available for educational and research purposes.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## 📧 Contact

**GitHub**: [@jairajcj](https://github.com/jairajcj)  
**Repository**: [quantum-dance-recommender](https://github.com/jairajcj/quantum-dance-recommender)

---

Enjoy analyzing dance videos! 🎉💃🕺

