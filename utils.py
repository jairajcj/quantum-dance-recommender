import os
import uuid
import numpy as np
from config import Config

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def generate_video_id():
    """Generate unique ID for uploaded video"""
    return str(uuid.uuid4())

def normalize_features(features):
    """Normalize feature vector to unit length"""
    norm = np.linalg.norm(features)
    if norm == 0:
        return features
    return features / norm

def calculate_entropy(probabilities):
    """Calculate Shannon entropy of probability distribution"""
    probabilities = np.array(probabilities)
    probabilities = probabilities[probabilities > 0]  # Remove zeros
    return -np.sum(probabilities * np.log2(probabilities))

def softmax(x):
    """Compute softmax values for array x"""
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum()

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    dot_product = np.dot(vec1, vec2)
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    if norm_product == 0:
        return 0
    return dot_product / norm_product

def get_video_path(video_id):
    """Get full path for video file"""
    return os.path.join(Config.UPLOAD_FOLDER, f"{video_id}.mp4")

def format_emotion_data(emotions_dict):
    """Format emotion dictionary for JSON response"""
    return {
        'facial': {k: float(v) for k, v in emotions_dict.get('facial', {}).items()},
        'movement': {k: float(v) for k, v in emotions_dict.get('movement', {}).items()},
        'combined': {k: float(v) for k, v in emotions_dict.get('combined', {}).items()}
    }
