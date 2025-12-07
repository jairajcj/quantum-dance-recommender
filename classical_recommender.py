import numpy as np
from config import Config
from utils import cosine_similarity

class ClassicalRecommender:
    def __init__(self):
        self.dance_styles = Config.DANCE_STYLES
        self.top_k = Config.TOP_K_RECOMMENDATIONS
        
        # Predefined emotion-dance mappings (knowledge base)
        self.emotion_dance_matrix = self._build_emotion_dance_matrix()
    
    def _build_emotion_dance_matrix(self):
        """Build emotion-to-dance style mapping matrix"""
        # This is a simplified knowledge base
        # Rows: emotions, Columns: dance styles
        mappings = {
            'happy': {'Hip-Hop': 0.8, 'Jazz': 0.7, 'Salsa': 0.9, 'Tap': 0.6},
            'sad': {'Contemporary': 0.9, 'Lyrical': 0.8, 'Ballet': 0.6},
            'angry': {'Breakdance': 0.8, 'Hip-Hop': 0.7, 'Freestyle': 0.6},
            'energetic': {'Hip-Hop': 0.9, 'Breakdance': 0.8, 'Salsa': 0.7, 'Tap': 0.6},
            'calm': {'Ballet': 0.9, 'Contemporary': 0.7, 'Lyrical': 0.8},
            'graceful': {'Ballet': 1.0, 'Ballroom': 0.8, 'Contemporary': 0.7},
            'playful': {'Jazz': 0.8, 'Tap': 0.7, 'Freestyle': 0.6},
            'aggressive': {'Breakdance': 0.9, 'Hip-Hop': 0.7},
            'melancholic': {'Contemporary': 0.9, 'Lyrical': 0.8, 'Ballet': 0.6},
            'surprise': {'Freestyle': 0.7, 'Jazz': 0.6},
            'neutral': {'Freestyle': 0.5, 'Contemporary': 0.5},
            'fear': {'Contemporary': 0.6, 'Freestyle': 0.5},
            'disgust': {'Freestyle': 0.5}
        }
        
        return mappings
    
    def recommend(self, emotions):
        """Generate classical recommendations based on weighted emotion vectors"""
        # Calculate scores for each dance style
        dance_scores = {style: 0.0 for style in self.dance_styles}
        
        for emotion, intensity in emotions.items():
            if emotion in self.emotion_dance_matrix:
                for dance, affinity in self.emotion_dance_matrix[emotion].items():
                    if dance in dance_scores:
                        dance_scores[dance] += intensity * affinity
        
        # Sort by score
        sorted_dances = sorted(dance_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get top K recommendations
        recommendations = []
        for dance, score in sorted_dances[:self.top_k]:
            if score > 0:
                recommendations.append({
                    'dance_style': dance,
                    'score': float(score),
                    'confidence': min(1.0, float(score)),
                    'reasoning': self._generate_reasoning(dance, emotions)
                })
        
        return {
            'recommendations': recommendations,
            'method': 'classical',
            'diversity_score': self._calculate_diversity(recommendations)
        }
    
    def _generate_reasoning(self, dance_style, emotions):
        """Generate human-readable reasoning for recommendation"""
        # Find top contributing emotions
        contributions = []
        for emotion, intensity in emotions.items():
            if emotion in self.emotion_dance_matrix:
                if dance_style in self.emotion_dance_matrix[emotion]:
                    affinity = self.emotion_dance_matrix[emotion][dance_style]
                    contributions.append((emotion, intensity * affinity))
        
        contributions.sort(key=lambda x: x[1], reverse=True)
        
        if contributions:
            top_emotion = contributions[0][0]
            return f"Strong {top_emotion} emotion detected, which aligns well with {dance_style}"
        else:
            return f"General compatibility with {dance_style}"
    
    def _calculate_diversity(self, recommendations):
        """Calculate diversity score of recommendations"""
        if len(recommendations) < 2:
            return 0.0
        
        # Simple diversity: variance in scores
        scores = [r['score'] for r in recommendations]
        return float(np.std(scores))
