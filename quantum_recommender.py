import numpy as np
from scipy.linalg import expm
from config import Config
from utils import softmax, calculate_entropy

class QuantumRecommender:
    def __init__(self):
        self.dance_styles = Config.DANCE_STYLES
        self.dimensions = Config.QUANTUM_DIMENSIONS
        self.entanglement_strength = Config.ENTANGLEMENT_STRENGTH
        self.top_k = Config.TOP_K_RECOMMENDATIONS
        
        # Initialize quantum state space
        self.emotion_basis = self._create_emotion_basis()
        self.dance_basis = self._create_dance_basis()
        self.entanglement_matrix = self._create_entanglement_matrix()
    
    def _create_emotion_basis(self):
        """Create orthonormal basis vectors for emotions"""
        # Map emotions to quantum basis states
        basis = {}
        num_emotions = len(Config.FACIAL_EMOTIONS) + len(Config.MOVEMENT_EMOTIONS)
        
        all_emotions = Config.FACIAL_EMOTIONS + Config.MOVEMENT_EMOTIONS
        
        for i, emotion in enumerate(all_emotions):
            # Create basis vector (one-hot encoding in Hilbert space)
            vector = np.zeros(self.dimensions, dtype=complex)
            if i < self.dimensions:
                vector[i] = 1.0 + 0j
            basis[emotion] = vector
        
        return basis
    
    def _create_dance_basis(self):
        """Create orthonormal basis vectors for dance styles"""
        basis = {}
        
        for i, dance in enumerate(self.dance_styles):
            vector = np.zeros(self.dimensions, dtype=complex)
            if i < self.dimensions:
                vector[i] = 1.0 + 0j
            basis[dance] = vector
        
        return basis
    
    def _create_entanglement_matrix(self):
        """Create entanglement correlation matrix between emotions and dances"""
        # This matrix represents quantum correlations (entanglement)
        # Higher values mean stronger non-classical correlations
        
        correlations = {
            'happy': {'Hip-Hop': 0.9, 'Jazz': 0.8, 'Salsa': 0.95, 'Tap': 0.7},
            'sad': {'Contemporary': 0.95, 'Lyrical': 0.9, 'Ballet': 0.7},
            'angry': {'Breakdance': 0.9, 'Hip-Hop': 0.8, 'Freestyle': 0.7},
            'energetic': {'Hip-Hop': 0.95, 'Breakdance': 0.9, 'Salsa': 0.85},
            'calm': {'Ballet': 0.95, 'Contemporary': 0.8, 'Lyrical': 0.9},
            'graceful': {'Ballet': 1.0, 'Ballroom': 0.9, 'Contemporary': 0.8},
            'playful': {'Jazz': 0.9, 'Tap': 0.85, 'Freestyle': 0.7},
            'aggressive': {'Breakdance': 0.95, 'Hip-Hop': 0.8},
            'melancholic': {'Contemporary': 0.95, 'Lyrical': 0.9, 'Ballet': 0.7},
        }
        
        return correlations
    
    def recommend(self, emotions):
        """Generate quantum-inspired recommendations using superposition and entanglement"""
        # Step 1: Create superposition state from emotions
        quantum_state = self._create_superposition_state(emotions)
        
        # Step 2: Apply entanglement transformation
        entangled_state = self._apply_entanglement(quantum_state, emotions)
        
        # Step 3: Measure quantum state (collapse to recommendations)
        recommendations = self._quantum_measurement(entangled_state, emotions)
        
        return {
            'recommendations': recommendations,
            'method': 'quantum',
            'quantum_properties': {
                'superposition_entropy': float(calculate_entropy([abs(a)**2 for a in quantum_state])),
                'entanglement_strength': self.entanglement_strength,
                'coherence': float(np.abs(np.sum(quantum_state)))
            }
        }
    
    def _create_superposition_state(self, emotions):
        """Create quantum superposition from emotion probabilities"""
        # Initialize state vector
        state = np.zeros(self.dimensions, dtype=complex)
        
        # Create superposition: |ψ⟩ = Σ αᵢ|emotionᵢ⟩
        for emotion, probability in emotions.items():
            if emotion in self.emotion_basis:
                # Amplitude is square root of probability (Born rule)
                amplitude = np.sqrt(probability)
                
                # Add phase for quantum interference
                phase = np.random.uniform(0, 2 * np.pi)
                complex_amplitude = amplitude * np.exp(1j * phase)
                
                state += complex_amplitude * self.emotion_basis[emotion]
        
        # Normalize state
        norm = np.linalg.norm(state)
        if norm > 0:
            state = state / norm
        
        return state
    
    def _apply_entanglement(self, quantum_state, emotions):
        """Apply entanglement transformation based on emotion-dance correlations"""
        # Create entanglement operator (unitary transformation)
        entanglement_op = np.eye(self.dimensions, dtype=complex)
        
        # Modify operator based on emotion-dance correlations
        for i, dance in enumerate(self.dance_styles):
            if i >= self.dimensions:
                break
            
            for emotion, intensity in emotions.items():
                if emotion in self.entanglement_matrix:
                    if dance in self.entanglement_matrix[emotion]:
                        correlation = self.entanglement_matrix[emotion][dance]
                        
                        # Apply rotation based on correlation strength
                        angle = correlation * self.entanglement_strength * np.pi / 2
                        entanglement_op[i, i] *= np.exp(1j * angle * intensity)
        
        # Apply entanglement operator to state
        entangled_state = entanglement_op @ quantum_state
        
        return entangled_state
    
    def _quantum_measurement(self, quantum_state, emotions):
        """Perform quantum measurement to collapse state into recommendations"""
        # Calculate measurement probabilities for each dance style
        dance_probabilities = {}
        
        for i, dance in enumerate(self.dance_styles):
            if i < self.dimensions:
                # Probability = |⟨dance|ψ⟩|²
                projection = np.abs(np.dot(np.conj(self.dance_basis[dance]), quantum_state))**2
                
                # Boost probability based on entanglement correlations
                boost = 0.0
                for emotion, intensity in emotions.items():
                    if emotion in self.entanglement_matrix:
                        if dance in self.entanglement_matrix[emotion]:
                            boost += intensity * self.entanglement_matrix[emotion][dance]
                
                # Combine quantum probability with entanglement boost
                dance_probabilities[dance] = projection * (1 + boost)
        
        # Normalize probabilities
        total = sum(dance_probabilities.values())
        if total > 0:
            dance_probabilities = {k: v/total for k, v in dance_probabilities.items()}
        
        # Sort and select top K
        sorted_dances = sorted(dance_probabilities.items(), key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for dance, probability in sorted_dances[:self.top_k]:
            if probability > Config.SUPERPOSITION_THRESHOLD:
                recommendations.append({
                    'dance_style': dance,
                    'score': float(probability),
                    'confidence': float(probability),
                    'reasoning': self._generate_quantum_reasoning(dance, emotions, probability),
                    'quantum_amplitude': float(probability)  # Unique to quantum model
                })
        
        return recommendations
    
    def _generate_quantum_reasoning(self, dance_style, emotions, probability):
        """Generate reasoning for quantum recommendation"""
        # Find strongest entangled emotions
        entangled_emotions = []
        for emotion, intensity in emotions.items():
            if emotion in self.entanglement_matrix:
                if dance_style in self.entanglement_matrix[emotion]:
                    correlation = self.entanglement_matrix[emotion][dance_style]
                    entangled_emotions.append((emotion, intensity * correlation))
        
        entangled_emotions.sort(key=lambda x: x[1], reverse=True)
        
        if entangled_emotions:
            top_emotion = entangled_emotions[0][0]
            return f"Quantum entanglement detected between {top_emotion} and {dance_style} (amplitude: {probability:.2f})"
        else:
            return f"Emerged from quantum superposition (amplitude: {probability:.2f})"
