import numpy as np
import cv2
from config import Config

class EmotionAnalyzer:
    def __init__(self):
        self.facial_emotions = Config.FACIAL_EMOTIONS
        self.movement_emotions = Config.MOVEMENT_EMOTIONS
        # Load Haar Cascade for face detection (lightweight)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def analyze_emotions(self, video_features):
        """Analyze emotions from video features"""
        # Analyze facial presence (simplified)
        facial_emotions = self._analyze_facial_presence(video_features.get('sample_frames', []))
        
        # Analyze movement-based emotions
        movement_emotions = self._analyze_movement_emotions(video_features)
        
        # Combine both analyses
        combined_emotions = self._combine_emotions(facial_emotions, movement_emotions)
        
        return {
            'facial': facial_emotions,
            'movement': movement_emotions,
            'combined': combined_emotions
        }
    
    def _analyze_facial_presence(self, frames):
        """Detect facial presence and infer basic emotions"""
        if not frames:
            return {emotion: 1.0/len(self.facial_emotions) for emotion in self.facial_emotions}
        
        face_detected = False
        for frame in frames:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            if len(faces) > 0:
                face_detected = True
                break
        
        # Simple emotion distribution based on face presence
        if face_detected:
            emotions = {
                'happy': 0.3,
                'neutral': 0.3,
                'surprise': 0.2,
                'sad': 0.1,
                'angry': 0.05,
                'fear': 0.03,
                'disgust': 0.02
            }
        else:
            # Equal distribution if no face
            emotions = {emotion: 1.0/len(self.facial_emotions) for emotion in self.facial_emotions}
        
        return emotions
    
    def _analyze_movement_emotions(self, features):
        """Infer emotions from movement characteristics"""
        emotions = {}
        
        # Extract movement features
        avg_velocity = features.get('avg_velocity', 0)
        max_velocity = features.get('max_velocity', 0)
        velocity_variance = features.get('velocity_variance', 0)
        avg_acceleration = features.get('avg_acceleration', 0)
        pose_diversity = features.get('pose_diversity', 0)
        
        # Energetic: high velocity and acceleration
        emotions['energetic'] = min(1.0, (avg_velocity * 2 + avg_acceleration) / 2)
        
        # Calm: low velocity and variance
        emotions['calm'] = max(0.0, 1.0 - (avg_velocity + velocity_variance) / 2)
        
        # Aggressive: high acceleration and velocity variance
        emotions['aggressive'] = min(1.0, (avg_acceleration * 2 + velocity_variance) / 2)
        
        # Graceful: moderate velocity with low variance
        if avg_velocity > 0.3 and velocity_variance < 0.3:
            emotions['graceful'] = 0.7
        else:
            emotions['graceful'] = 0.3
        
        # Playful: high pose diversity and moderate velocity
        emotions['playful'] = min(1.0, (pose_diversity * 3 + avg_velocity) / 2)
        
        # Melancholic: low velocity and low diversity
        emotions['melancholic'] = max(0.0, 1.0 - (avg_velocity + pose_diversity) / 2)
        
        # Normalize to sum to 1
        total = sum(emotions.values())
        if total > 0:
            emotions = {k: v/total for k, v in emotions.items()}
        
        return emotions
    
    def _combine_emotions(self, facial, movement):
        """Combine facial and movement emotions with weighted average"""
        combined = {}
        
        # Weight: 40% facial, 60% movement (movement is more reliable in our simplified version)
        facial_weight = 0.4
        movement_weight = 0.6
        
        # Map emotions to combined space
        all_emotions = set(list(facial.keys()) + list(movement.keys()))
        
        for emotion in all_emotions:
            facial_score = facial.get(emotion, 0) * facial_weight
            movement_score = movement.get(emotion, 0) * movement_weight
            combined[emotion] = facial_score + movement_score
        
        # Normalize
        total = sum(combined.values())
        if total > 0:
            combined = {k: v/total for k, v in combined.items()}
        
        return combined

