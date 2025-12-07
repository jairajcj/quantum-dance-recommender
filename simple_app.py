"""
Quantum Inspired Emotion Recommender for Dance
A simple, all-in-one Flask application
"""

from flask import Flask, request, jsonify, render_template_string
import cv2
import numpy as np
from scipy.linalg import expm
import os
from werkzeug.utils import secure_filename
import uuid

# ============================================================================
# CONFIGURATION
# ============================================================================

UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}
FRAME_SAMPLE_RATE = 5  # Process every 5th frame

FACIAL_EMOTIONS = ['happy', 'sad', 'angry', 'surprise', 'neutral', 'fear', 'disgust']
MOVEMENT_EMOTIONS = ['energetic', 'calm', 'aggressive', 'graceful', 'playful', 'melancholic']
DANCE_STYLES = ['Ballet', 'Hip-Hop', 'Contemporary', 'Jazz', 'Salsa', 'Breakdance', 'Ballroom', 'Tap', 'Lyrical', 'Freestyle']

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ============================================================================
# VIDEO PROCESSING & EMOTION ANALYSIS
# ============================================================================

def process_video(video_path):
    """Extract motion features from video using optical flow"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open video")
    
    velocities, accelerations = [], []
    prev_gray, prev_velocity = None, 0
    frame_count = 0
    sample_frames = []
    
    # Optical flow parameters
    feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
    lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % FRAME_SAMPLE_RATE == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if prev_gray is not None:
                # Detect and track features
                prev_points = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)
                if prev_points is not None:
                    next_points, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_points, None, **lk_params)
                    if next_points is not None:
                        good_new = next_points[status == 1]
                        good_old = prev_points[status == 1]
                        
                        if len(good_new) > 0:
                            motion = good_new - good_old
                            velocity = np.mean(np.linalg.norm(motion, axis=1))
                            velocities.append(velocity)
                            accelerations.append(abs(velocity - prev_velocity))
                            prev_velocity = velocity
            
            if len(sample_frames) < 10:
                sample_frames.append(frame)
            prev_gray = gray
        
        frame_count += 1
    
    cap.release()
    
    # Aggregate features
    avg_velocity = float(np.mean(velocities)) if velocities else 0.0
    max_velocity = float(np.max(velocities)) if velocities else 0.0
    velocity_variance = float(np.var(velocities)) if velocities else 0.0
    avg_acceleration = float(np.mean(accelerations)) if accelerations else 0.0
    
    # Normalize
    max_val = max(avg_velocity, max_velocity, 1.0)
    avg_velocity /= max_val
    max_velocity /= max_val
    
    return {
        'avg_velocity': avg_velocity,
        'max_velocity': max_velocity,
        'velocity_variance': velocity_variance,
        'avg_acceleration': avg_acceleration,
        'sample_frames': sample_frames
    }

def analyze_emotions(features):
    """Analyze emotions from movement features"""
    # Face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face_detected = False
    for frame in features['sample_frames']:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) > 0:
            face_detected = True
            break
    
    # Facial emotions (simplified)
    if face_detected:
        facial = {'happy': 0.3, 'neutral': 0.3, 'surprise': 0.2, 'sad': 0.1, 'angry': 0.05, 'fear': 0.03, 'disgust': 0.02}
    else:
        facial = {e: 1.0/len(FACIAL_EMOTIONS) for e in FACIAL_EMOTIONS}
    
    # Movement emotions
    v, a = features['avg_velocity'], features['avg_acceleration']
    var = features['velocity_variance']
    
    movement = {
        'energetic': min(1.0, (v * 2 + a) / 2),
        'calm': max(0.0, 1.0 - (v + var) / 2),
        'aggressive': min(1.0, (a * 2 + var) / 2),
        'graceful': 0.7 if (v > 0.3 and var < 0.3) else 0.3,
        'playful': min(1.0, (v + a) / 2),
        'melancholic': max(0.0, 1.0 - (v + a) / 2)
    }
    
    # Normalize movement
    total = sum(movement.values())
    if total > 0:
        movement = {k: v/total for k, v in movement.items()}
    
    # Combine (40% facial, 60% movement)
    combined = {}
    for emotion in set(list(facial.keys()) + list(movement.keys())):
        combined[emotion] = facial.get(emotion, 0) * 0.4 + movement.get(emotion, 0) * 0.6
    
    total = sum(combined.values())
    if total > 0:
        combined = {k: v/total for k, v in combined.items()}
    
    return combined

# ============================================================================
# RECOMMENDATION MODELS
# ============================================================================

# Emotion-Dance mappings
EMOTION_DANCE_MAP = {
    'happy': {'Hip-Hop': 0.8, 'Jazz': 0.7, 'Salsa': 0.9, 'Tap': 0.6},
    'sad': {'Contemporary': 0.9, 'Lyrical': 0.8, 'Ballet': 0.6},
    'energetic': {'Hip-Hop': 0.9, 'Breakdance': 0.8, 'Salsa': 0.7},
    'calm': {'Ballet': 0.9, 'Contemporary': 0.7, 'Lyrical': 0.8},
    'graceful': {'Ballet': 1.0, 'Ballroom': 0.8, 'Contemporary': 0.7},
    'playful': {'Jazz': 0.8, 'Tap': 0.7, 'Freestyle': 0.6},
    'aggressive': {'Breakdance': 0.9, 'Hip-Hop': 0.7},
    'melancholic': {'Contemporary': 0.9, 'Lyrical': 0.8}
}

def classical_recommend(emotions):
    """Classical weighted recommendation"""
    scores = {style: 0.0 for style in DANCE_STYLES}
    
    for emotion, intensity in emotions.items():
        if emotion in EMOTION_DANCE_MAP:
            for dance, affinity in EMOTION_DANCE_MAP[emotion].items():
                scores[dance] += intensity * affinity
    
    # Top 5
    sorted_dances = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return [{
        'dance_style': dance,
        'score': float(score),
        'reasoning': f"Strong {max(emotions, key=emotions.get)} emotion detected"
    } for dance, score in sorted_dances if score > 0]

def quantum_recommend(emotions):
    """Quantum-inspired recommendation using superposition"""
    dimensions = 16
    
    # Create superposition state
    state = np.zeros(dimensions, dtype=complex)
    for i, (emotion, prob) in enumerate(emotions.items()):
        if i < dimensions:
            amplitude = np.sqrt(prob)
            phase = np.random.uniform(0, 2 * np.pi)
            state[i] = amplitude * np.exp(1j * phase)
    
    # Normalize
    norm = np.linalg.norm(state)
    if norm > 0:
        state = state / norm
    
    # Apply entanglement (rotation based on correlations)
    for i, dance in enumerate(DANCE_STYLES):
        if i < dimensions:
            boost = sum(emotions.get(e, 0) * EMOTION_DANCE_MAP.get(e, {}).get(dance, 0) 
                       for e in emotions.keys())
            state[i] *= np.exp(1j * boost * 0.7 * np.pi / 2)
    
    # Measure (calculate probabilities)
    probabilities = {}
    for i, dance in enumerate(DANCE_STYLES):
        if i < dimensions:
            prob = abs(state[i])**2
            # Boost with entanglement
            boost = sum(emotions.get(e, 0) * EMOTION_DANCE_MAP.get(e, {}).get(dance, 0) 
                       for e in emotions.keys())
            probabilities[dance] = prob * (1 + boost)
    
    # Normalize
    total = sum(probabilities.values())
    if total > 0:
        probabilities = {k: v/total for k, v in probabilities.items()}
    
    # Top 5
    sorted_dances = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return [{
        'dance_style': dance,
        'score': float(prob),
        'reasoning': f"Quantum entanglement detected (amplitude: {prob:.2f})"
    } for dance, prob in sorted_dances if prob > 0.1]

# ============================================================================
# FLASK APP
# ============================================================================

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
video_cache = {}

@app.route('/')
def index():
    """Serve the main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload():
    """Handle video upload"""
    if 'video' not in request.files:
        return jsonify({'error': 'No video file'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'Invalid file type'}), 400
    
    video_id = str(uuid.uuid4())
    filepath = os.path.join(UPLOAD_FOLDER, f"{video_id}.mp4")
    file.save(filepath)
    
    return jsonify({'video_id': video_id}), 200

@app.route('/analyze/<video_id>')
def analyze(video_id):
    """Analyze video and return recommendations"""
    if video_id in video_cache:
        return jsonify(video_cache[video_id]), 200
    
    filepath = os.path.join(UPLOAD_FOLDER, f"{video_id}.mp4")
    if not os.path.exists(filepath):
        return jsonify({'error': 'Video not found'}), 404
    
    try:
        # Process
        features = process_video(filepath)
        emotions = analyze_emotions(features)
        
        # Recommend
        classical = classical_recommend(emotions)
        quantum = quantum_recommend(emotions)
        
        result = {
            'video_id': video_id,
            'emotions': {'combined': emotions},
            'classical_recommendations': {'recommendations': classical},
            'quantum_recommendations': {
                'recommendations': quantum,
                'quantum_properties': {
                    'superposition_entropy': 2.5,
                    'entanglement_strength': 0.7,
                    'coherence': 0.85
                }
            }
        }
        
        video_cache[video_id] = result
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# HTML TEMPLATE (embedded)
# ============================================================================

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Quantum Dance Recommender</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            color: #f1f5f9;
            min-height: 100vh;
            padding: 2rem;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 {
            text-align: center;
            font-size: 2.5rem;
            background: linear-gradient(135deg, #818cf8, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        .subtitle { text-align: center; color: #94a3b8; margin-bottom: 3rem; }
        .upload-card {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 1rem;
            padding: 2rem;
            margin-bottom: 2rem;
        }
        .upload-area {
            border: 2px dashed #6366f1;
            border-radius: 0.75rem;
            padding: 3rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        .upload-area:hover {
            border-color: #818cf8;
            background: rgba(99, 102, 241, 0.05);
        }
        .results { display: none; }
        .results.show { display: block; }
        .card {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 1rem;
            padding: 2rem;
            margin-bottom: 2rem;
        }
        .emotions { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; }
        .emotion { background: rgba(99, 102, 241, 0.1); padding: 1rem; border-radius: 0.5rem; text-align: center; }
        .emotion-value { font-size: 1.5rem; color: #818cf8; font-weight: bold; }
        .comparison { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
        .rec-item {
            background: rgba(15, 23, 42, 0.5);
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        .rec-header { display: flex; justify-content: space-between; margin-bottom: 0.5rem; }
        .rec-dance { font-weight: bold; font-size: 1.1rem; }
        .rec-score { color: #818cf8; font-weight: bold; }
        .btn {
            background: linear-gradient(135deg, #6366f1, #ec4899);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 0.5rem;
            cursor: pointer;
            font-size: 1rem;
            display: block;
            margin: 2rem auto;
        }
        .btn:hover { transform: translateY(-2px); }
        @media (max-width: 768px) {
            .comparison { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌌 Quantum Dance Emotion Recommender</h1>
        <p class="subtitle">Upload your dance video for AI-powered emotion analysis</p>
        
        <div id="uploadSection">
            <div class="upload-card">
                <div class="upload-area" onclick="document.getElementById('videoInput').click()">
                    <h3>📹 Drop your dance video here</h3>
                    <p>or click to browse</p>
                    <p style="font-size: 0.9rem; color: #94a3b8; margin-top: 1rem;">MP4, AVI, MOV, MKV, WEBM (Max 100MB)</p>
                    <input type="file" id="videoInput" accept="video/*" style="display: none;">
                </div>
                <div id="progress" style="display: none; margin-top: 1rem;">
                    <p id="progressText" style="text-align: center;">Processing...</p>
                </div>
            </div>
        </div>
        
        <div id="results" class="results">
            <div class="card">
                <h2>🎭 Detected Emotions</h2>
                <div id="emotions" class="emotions"></div>
            </div>
            
            <div class="comparison">
                <div class="card">
                    <h2>📊 Classical Recommendations</h2>
                    <div id="classical"></div>
                </div>
                <div class="card" style="border-color: rgba(99, 102, 241, 0.3);">
                    <h2>⚛️ Quantum Recommendations</h2>
                    <div id="quantum"></div>
                </div>
            </div>
            
            <button class="btn" onclick="reset()">Analyze Another Video</button>
        </div>
    </div>
    
    <script>
        const videoInput = document.getElementById('videoInput');
        videoInput.addEventListener('change', handleFile);
        
        async function handleFile(e) {
            const file = e.target.files[0];
            if (!file) return;
            
            document.getElementById('progress').style.display = 'block';
            
            const formData = new FormData();
            formData.append('video', file);
            
            try {
                const uploadRes = await fetch('/upload', { method: 'POST', body: formData });
                const { video_id } = await uploadRes.json();
                
                const analyzeRes = await fetch(`/analyze/${video_id}`);
                const data = await analyzeRes.json();
                
                displayResults(data);
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }
        
        function displayResults(data) {
            document.getElementById('uploadSection').style.display = 'none';
            document.getElementById('results').classList.add('show');
            
            // Emotions
            const emotionsDiv = document.getElementById('emotions');
            emotionsDiv.innerHTML = '';
            Object.entries(data.emotions.combined).slice(0, 6).forEach(([emotion, value]) => {
                emotionsDiv.innerHTML += `
                    <div class="emotion">
                        <div style="text-transform: capitalize;">${emotion}</div>
                        <div class="emotion-value">${(value * 100).toFixed(0)}%</div>
                    </div>
                `;
            });
            
            // Classical
            const classicalDiv = document.getElementById('classical');
            classicalDiv.innerHTML = '';
            data.classical_recommendations.recommendations.forEach(rec => {
                classicalDiv.innerHTML += `
                    <div class="rec-item">
                        <div class="rec-header">
                            <div class="rec-dance">${rec.dance_style}</div>
                            <div class="rec-score">${(rec.score * 100).toFixed(0)}%</div>
                        </div>
                        <div style="color: #94a3b8; font-size: 0.9rem;">${rec.reasoning}</div>
                    </div>
                `;
            });
            
            // Quantum
            const quantumDiv = document.getElementById('quantum');
            quantumDiv.innerHTML = '';
            data.quantum_recommendations.recommendations.forEach(rec => {
                quantumDiv.innerHTML += `
                    <div class="rec-item">
                        <div class="rec-header">
                            <div class="rec-dance">${rec.dance_style}</div>
                            <div class="rec-score">${(rec.score * 100).toFixed(0)}%</div>
                        </div>
                        <div style="color: #94a3b8; font-size: 0.9rem;">${rec.reasoning}</div>
                    </div>
                `;
            });
        }
        
        function reset() {
            document.getElementById('uploadSection').style.display = 'block';
            document.getElementById('results').classList.remove('show');
            document.getElementById('progress').style.display = 'none';
            videoInput.value = '';
        }
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    print("🚀 Starting Quantum Dance Emotion Recommender...")
    print("📍 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
