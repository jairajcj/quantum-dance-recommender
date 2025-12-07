# Quantum Inspired Emotion Recommender for Dance Experiences

A web-based application that analyzes dance videos and provides emotion-driven recommendations using both classical and quantum-inspired AI models.

## Features

- **Video Upload**: Drag-and-drop or browse to upload dance videos
- **Emotion Detection**: Combines facial expression analysis (DeepFace) with movement-based emotion inference
- **Dual Recommendation System**:
  - **Classical Model**: Weighted emotion-dance mappings
  - **Quantum Model**: Superposition and entanglement metaphors for nuanced recommendations
- **Interactive Comparison**: Side-by-side view of both recommendation approaches
- **Modern UI**: Quantum-themed interface with smooth animations

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone or navigate to project directory**:
```bash
cd "C:\Users\Lenovo\Documents\New folder (2)"
```

2. **Create virtual environment** (recommended):
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

1. **Start the server**:
```bash
python app.py
```

2. **Open browser** and navigate to:
```
http://localhost:5000
```

3. **Upload a dance video** and view the results!

## Project Structure

```
├── app.py                      # Flask application
├── config.py                   # Configuration settings
├── utils.py                    # Utility functions
├── video_processor.py          # Video analysis (MediaPipe)
├── emotion_analyzer.py         # Emotion detection (DeepFace + movement)
├── classical_recommender.py    # Classical baseline model
├── quantum_recommender.py      # Quantum-inspired model
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Main web page
├── static/
│   ├── styles.css             # Styling
│   └── app.js                 # Frontend logic
└── uploads/                   # Uploaded videos (auto-created)
```

## How It Works

### 1. Video Processing
- Extracts frames at intervals for efficiency
- Uses MediaPipe for pose estimation (33 body landmarks)
- Calculates movement features: velocity, acceleration, pose diversity

### 2. Emotion Analysis
- **Facial**: DeepFace detects 7 emotions (happy, sad, angry, surprise, neutral, fear, disgust)
- **Movement**: Infers 6 emotions from motion (energetic, calm, aggressive, graceful, playful, melancholic)
- **Combined**: Weighted fusion (60% facial, 40% movement)

### 3. Classical Recommendations
- Uses predefined emotion-dance affinity matrix
- Weighted scoring based on detected emotions
- Returns top 5 dance styles with confidence scores

### 4. Quantum-Inspired Recommendations
- **Superposition**: Emotions exist in multiple states with probability amplitudes
- **Entanglement**: Non-classical correlations between emotions and dance styles
- **Measurement**: Probabilistic collapse to specific recommendations
- Provides unique insights through quantum properties (entropy, coherence)

## Performance Optimizations

- **Frame Sampling**: Processes every 5th frame (configurable)
- **In-Memory Caching**: Stores analysis results to avoid reprocessing
- **Singleton Pattern**: Reuses model instances across requests
- **Lazy Loading**: Models loaded only when needed

## API Endpoints

- `GET /` - Main web interface
- `POST /upload` - Upload video file
- `GET /analyze/<video_id>` - Analyze video and get recommendations
- `GET /health` - Health check

## Configuration

Edit `config.py` to customize:
- Frame sample rate
- Emotion categories
- Dance styles
- Quantum model parameters
- Upload limits

## Research Use

This system is designed for academic research comparing classical and quantum-inspired recommendation approaches. Key metrics:

- **Diversity**: Variance in recommendation scores
- **Entropy**: Information content of emotion distributions
- **Coherence**: Quantum state coherence measure

## License

MIT License - Feel free to use for research and education

## Acknowledgments

- MediaPipe for pose estimation
- DeepFace for facial emotion recognition
- Quantum computing concepts for inspiration
