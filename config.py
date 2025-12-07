import os

# Application Configuration
class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'quantum-dance-secret-key-2024'
    
    # Upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}
    
    # Video processing settings
    FRAME_SAMPLE_RATE = 5  # Process every 5th frame for efficiency
    MIN_DETECTION_CONFIDENCE = 0.5
    MIN_TRACKING_CONFIDENCE = 0.5
    
    # Emotion categories
    FACIAL_EMOTIONS = ['happy', 'sad', 'angry', 'surprise', 'neutral', 'fear', 'disgust']
    MOVEMENT_EMOTIONS = ['energetic', 'calm', 'aggressive', 'graceful', 'playful', 'melancholic']
    
    # Dance styles
    DANCE_STYLES = [
        'Ballet', 'Hip-Hop', 'Contemporary', 'Jazz', 'Salsa', 
        'Breakdance', 'Ballroom', 'Tap', 'Lyrical', 'Freestyle'
    ]
    
    # Quantum model parameters
    QUANTUM_DIMENSIONS = 16  # Hilbert space dimensions
    ENTANGLEMENT_STRENGTH = 0.7  # Correlation strength between emotion-dance pairs
    SUPERPOSITION_THRESHOLD = 0.1  # Minimum amplitude to consider
    
    # Classical model parameters
    SIMILARITY_THRESHOLD = 0.6
    TOP_K_RECOMMENDATIONS = 5

# Create upload directory if it doesn't exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
