import cv2
import numpy as np
from config import Config

class VideoProcessor:
    def __init__(self):
        # Use OpenCV's optical flow for motion detection (lightweight)
        self.feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
        self.lk_params = dict(winSize=(15, 15), maxLevel=2, 
                             criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        
    def extract_features(self, video_path):
        """Extract movement features from video using optical flow"""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError("Could not open video file")
        
        features = {
            'velocities': [],
            'accelerations': [],
            'motion_magnitudes': [],
            'frames': []
        }
        
        frame_count = 0
        prev_gray = None
        prev_points = None
        prev_velocity = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Sample frames for efficiency
            if frame_count % Config.FRAME_SAMPLE_RATE == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                if prev_gray is not None:
                    # Detect feature points if needed
                    if prev_points is None or len(prev_points) < 10:
                        prev_points = cv2.goodFeaturesToTrack(prev_gray, mask=None, **self.feature_params)
                    
                    if prev_points is not None:
                        # Calculate optical flow
                        next_points, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_points, None, **self.lk_params)
                        
                        if next_points is not None:
                            # Select good points
                            good_new = next_points[status == 1]
                            good_old = prev_points[status == 1]
                            
                            # Calculate motion
                            if len(good_new) > 0:
                                motion = good_new - good_old
                                velocity = np.mean(np.linalg.norm(motion, axis=1))
                                features['velocities'].append(velocity)
                                
                                # Calculate acceleration
                                acceleration = abs(velocity - prev_velocity)
                                features['accelerations'].append(acceleration)
                                prev_velocity = velocity
                                
                                # Motion magnitude
                                features['motion_magnitudes'].append(np.sum(np.linalg.norm(motion, axis=1)))
                                
                                prev_points = good_new.reshape(-1, 1, 2)
                
                # Store sample frames
                if len(features['frames']) < 10:
                    features['frames'].append(frame)
                
                prev_gray = gray
            
            frame_count += 1
        
        cap.release()
        
        return self._aggregate_features(features)
    
    def _aggregate_features(self, features):
        """Aggregate temporal features into summary statistics"""
        aggregated = {}
        
        # Movement statistics
        if features['velocities']:
            velocities = np.array(features['velocities'])
            aggregated['avg_velocity'] = float(np.mean(velocities))
            aggregated['max_velocity'] = float(np.max(velocities))
            aggregated['velocity_variance'] = float(np.var(velocities))
        else:
            aggregated['avg_velocity'] = 0.0
            aggregated['max_velocity'] = 0.0
            aggregated['velocity_variance'] = 0.0
        
        if features['accelerations']:
            accelerations = np.array(features['accelerations'])
            aggregated['avg_acceleration'] = float(np.mean(accelerations))
            aggregated['acceleration_variance'] = float(np.var(accelerations))
        else:
            aggregated['avg_acceleration'] = 0.0
            aggregated['acceleration_variance'] = 0.0
        
        if features['motion_magnitudes']:
            aggregated['pose_diversity'] = float(np.std(features['motion_magnitudes']))
        else:
            aggregated['pose_diversity'] = 0.0
        
        # Normalize values for consistency
        max_val = max(aggregated['avg_velocity'], aggregated['max_velocity'], 1.0)
        aggregated['avg_velocity'] /= max_val
        aggregated['max_velocity'] /= max_val
        
        # Store sample frames for emotion detection
        aggregated['sample_frames'] = features['frames']
        
        return aggregated

