from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from config import Config
from utils import allowed_file, generate_video_id, get_video_path, format_emotion_data
from video_processor import VideoProcessor
from emotion_analyzer import EmotionAnalyzer
from classical_recommender import ClassicalRecommender
from quantum_recommender import QuantumRecommender
import json

app = Flask(__name__)
app.config.from_object(Config)

# Initialize processors (singleton pattern for efficiency)
video_processor = VideoProcessor()
emotion_analyzer = EmotionAnalyzer()
classical_recommender = ClassicalRecommender()
quantum_recommender = QuantumRecommender()

# In-memory cache for processed videos (RAM efficient - stores only results)
video_cache = {}

@app.route('/')
def index():
    """Serve main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    """Handle video upload"""
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Supported: mp4, avi, mov, mkv, webm'}), 400
    
    # Generate unique ID and save file
    video_id = generate_video_id()
    filename = secure_filename(f"{video_id}.mp4")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    return jsonify({
        'video_id': video_id,
        'message': 'Video uploaded successfully'
    }), 200

@app.route('/analyze/<video_id>', methods=['GET'])
def analyze_video(video_id):
    """Analyze video and return emotions + recommendations"""
    
    # Check cache first (efficiency optimization)
    if video_id in video_cache:
        return jsonify(video_cache[video_id]), 200
    
    video_path = get_video_path(video_id)
    
    if not os.path.exists(video_path):
        return jsonify({'error': 'Video not found'}), 404
    
    try:
        # Step 1: Extract video features
        features = video_processor.extract_features(video_path)
        
        # Step 2: Analyze emotions
        emotions = emotion_analyzer.analyze_emotions(features)
        
        # Step 3: Generate recommendations (both models)
        classical_recs = classical_recommender.recommend(emotions['combined'])
        quantum_recs = quantum_recommender.recommend(emotions['combined'])
        
        # Prepare response
        result = {
            'video_id': video_id,
            'emotions': format_emotion_data(emotions),
            'classical_recommendations': classical_recs,
            'quantum_recommendations': quantum_recs,
            'comparison': {
                'classical_diversity': classical_recs.get('diversity_score', 0),
                'quantum_coherence': quantum_recs.get('quantum_properties', {}).get('coherence', 0)
            }
        }
        
        # Cache result (memory efficient - only final results)
        video_cache[video_id] = result
        
        # Clean up video file to save storage
        # Uncomment if you want to delete after processing:
        # os.remove(video_path)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'cache_size': len(video_cache)}), 200

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Run app
    app.run(debug=True, host='0.0.0.0', port=5000)
