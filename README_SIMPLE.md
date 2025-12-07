# Quantum Dance Emotion Recommender - Simple Version

**One file. Easy to understand. Fast to run.**

## Quick Start

### 1. Install Dependencies
```bash
pip install flask opencv-python numpy scipy werkzeug
```

### 2. Run the App
```bash
python simple_app.py
```

### 3. Open Browser
Go to: **http://localhost:5000**

## That's It!

Upload a dance video and get emotion-based recommendations using both:
- **Classical Model**: Traditional weighted scoring
- **Quantum Model**: Superposition & entanglement inspired

## How It Works

### Video Analysis
- Uses OpenCV optical flow to track movement
- Calculates velocity, acceleration, motion patterns
- Detects faces using Haar Cascade

### Emotion Detection
- **Movement-based**: energetic, calm, aggressive, graceful, playful, melancholic
- **Facial**: happy, sad, angry, surprise, neutral, fear, disgust
- Combines both for final emotion profile

### Recommendations
- **Classical**: Weighted emotion-dance mappings
- **Quantum**: Probability amplitudes with entanglement correlations

## File Structure

```
simple_app.py          ← Everything in ONE file!
requirements_simple.txt ← Just 5 packages
README_SIMPLE.md       ← This file
```

## Customization

Edit `simple_app.py` to:
- Add more dance styles (line 23)
- Adjust emotion-dance mappings (line 155)
- Change UI colors (line 260+)
- Modify quantum parameters (line 200+)

## Performance

- **Lightweight**: ~200MB install
- **Fast**: Processes videos in seconds
- **Efficient**: Frame sampling, in-memory caching
- **Simple**: No complex dependencies

Enjoy! 🎉
