import cv2
import numpy as np
from collections import deque
import time

class LivenessDetector:
    """
    Liveness Detection Module for Face Recognition System
    
    This module detects if a face is real (live person) or fake (photo/video/mask)
    using multiple techniques:
    1. Eye blinking detection
    2. Head movement detection
    3. Texture analysis (detects flat surfaces like photos)
    4. Motion analysis (detects natural micro-movements)
    """
    
    def __init__(self):
        # Load cascade classifiers
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
        
        # Blink detection parameters
        self.blink_counter = 0
        self.total_blinks = 0
        self.eye_aspect_ratio_threshold = 0.25
        self.consecutive_frames = 2
        
        # Head movement detection
        self.face_positions = deque(maxlen=10)
        self.movement_threshold = 15
        
        # Texture analysis parameters
        self.texture_scores = deque(maxlen=5)
        self.texture_threshold = 20
        
        # Motion analysis
        self.prev_gray = None
        self.motion_scores = deque(maxlen=10)
        self.motion_threshold = 5
        
        # Overall liveness tracking
        self.liveness_checks = {
            'blink': False,
            'movement': False,
            'texture': False,
            'motion': False
        }
        
        # Time tracking
        self.start_time = time.time()
        self.check_duration = 3  # seconds to complete liveness check
        
    def reset(self):
        """Reset all detection parameters"""
        self.blink_counter = 0
        self.total_blinks = 0
        self.face_positions.clear()
        self.texture_scores.clear()
        self.motion_scores.clear()
        self.prev_gray = None
        self.liveness_checks = {
            'blink': False,
            'movement': False,
            'texture': False,
            'motion': False
        }
        self.start_time = time.time()
    
    def eye_aspect_ratio(self, eye_points):
        """Calculate eye aspect ratio for blink detection"""
        # Simplified EAR calculation
        height = abs(eye_points[1] - eye_points[3])
        width = abs(eye_points[0] - eye_points[2])
        
        if width == 0:
            return 0
        
        ear = height / width
        return ear
    
    def detect_blink(self, gray, face):
        """Detect eye blinking"""
        x, y, w, h = face
        roi_gray = gray[y:y+h, x:x+w]
        
        # Detect eyes in face region
        eyes = self.eye_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(20, 20)
        )
        
        if len(eyes) >= 2:
            # Calculate average eye openness
            total_ear = 0
            for (ex, ey, ew, eh) in eyes[:2]:
                eye_points = [ex, ey, ex + ew, ey + eh]
                ear = self.eye_aspect_ratio(eye_points)
                total_ear += ear
            
            avg_ear = total_ear / 2
            
            # Check if eyes are closed
            if avg_ear < self.eye_aspect_ratio_threshold:
                self.blink_counter += 1
            else:
                if self.blink_counter >= self.consecutive_frames:
                    self.total_blinks += 1
                    self.liveness_checks['blink'] = True
                self.blink_counter = 0
        
        return self.total_blinks
    
    def detect_head_movement(self, face):
        """Detect natural head movements"""
        x, y, w, h = face
        center_x = x + w // 2
        center_y = y + h // 2
        
        self.face_positions.append((center_x, center_y))
        
        if len(self.face_positions) >= 5:
            # Calculate movement variance
            positions = list(self.face_positions)
            x_coords = [p[0] for p in positions]
            y_coords = [p[1] for p in positions]
            
            x_variance = np.var(x_coords)
            y_variance = np.var(y_coords)
            
            # Check if there's natural movement
            if x_variance > self.movement_threshold or y_variance > self.movement_threshold:
                self.liveness_checks['movement'] = True
                return True
        
        return False
    
    def analyze_texture(self, gray, face):
        """Analyze texture to detect flat surfaces (photos)"""
        x, y, w, h = face
        roi = gray[y:y+h, x:x+w]
        
        # Calculate Laplacian variance (texture measure)
        # Real faces have more texture variation than printed photos
        laplacian = cv2.Laplacian(roi, cv2.CV_64F)
        variance = laplacian.var()
        
        self.texture_scores.append(variance)
        
        if len(self.texture_scores) >= 3:
            avg_texture = np.mean(self.texture_scores)
            # Real faces typically have higher texture variance
            if avg_texture > self.texture_threshold:
                self.liveness_checks['texture'] = True
                return True
        
        return False
    
    def analyze_motion(self, gray):
        """Analyze micro-movements and optical flow"""
        if self.prev_gray is not None:
            # Calculate frame difference
            diff = cv2.absdiff(self.prev_gray, gray)
            motion_score = np.mean(diff)
            
            self.motion_scores.append(motion_score)
            
            if len(self.motion_scores) >= 5:
                avg_motion = np.mean(self.motion_scores)
                # Real people have continuous micro-movements
                if avg_motion > self.motion_threshold:
                    self.liveness_checks['motion'] = True
        
        self.prev_gray = gray.copy()
    
    def check_liveness(self, frame, face):
        """
        Main liveness check function
        
        Args:
            frame: Current video frame (BGR)
            face: Detected face coordinates (x, y, w, h)
        
        Returns:
            tuple: (is_live: bool, confidence: float, status: str)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Perform all checks
        self.detect_blink(gray, face)
        self.detect_head_movement(face)
        self.analyze_texture(gray, face)
        self.analyze_motion(gray)
        
        # Calculate elapsed time
        elapsed_time = time.time() - self.start_time
        
        # Count passed checks
        passed_checks = sum(self.liveness_checks.values())
        total_checks = len(self.liveness_checks)
        
        # Calculate confidence score
        confidence = (passed_checks / total_checks) * 100
        
        # Determine liveness status
        if elapsed_time < self.check_duration:
            # Still checking
            status = f"Checking... {passed_checks}/{total_checks}"
            is_live = False
        else:
            # Check complete
            if passed_checks >= 3:  # At least 3 out of 4 checks must pass
                status = "LIVE ✓"
                is_live = True
            else:
                status = "SPOOF DETECTED ✗"
                is_live = False
        
        return is_live, confidence, status
    
    def draw_liveness_info(self, frame, face, status, confidence):
        """Draw liveness detection information on frame"""
        x, y, w, h = face
        
        # Draw status
        color = (0, 255, 0) if "LIVE" in status else (0, 0, 255) if "SPOOF" in status else (255, 165, 0)
        
        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        
        # Draw status text
        cv2.putText(frame, status, (x, y - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Draw confidence
        cv2.putText(frame, f"Confidence: {confidence:.0f}%", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Draw individual check status
        check_y = y + h + 20
        for check_name, passed in self.liveness_checks.items():
            check_color = (0, 255, 0) if passed else (128, 128, 128)
            check_text = f"{check_name.capitalize()}: {'✓' if passed else '○'}"
            cv2.putText(frame, check_text, (x, check_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, check_color, 1)
            check_y += 15
        
        return frame


class LivenessIntegration:
    """
    Integration wrapper for the existing face recognition system
    
    This class can be imported and used with minimal changes to existing code
    """
    
    def __init__(self):
        self.detector = LivenessDetector()
        self.liveness_enabled = True
        self.liveness_results = {}  # Store results per student ID
    
    def process_frame_with_liveness(self, frame, faces, recognizer=None, 
                                    student_id=None, confidence=None):
        """
        Process a frame with liveness detection
        
        Args:
            frame: Video frame
            faces: Detected faces [(x, y, w, h), ...]
            recognizer: Face recognizer object (optional)
            student_id: Recognized student ID (optional)
            confidence: Recognition confidence (optional)
        
        Returns:
            tuple: (processed_frame, liveness_passed, liveness_info)
        """
        if not self.liveness_enabled or len(faces) == 0:
            return frame, True, "Liveness check disabled"
        
        # Process the first face
        face = faces[0]
        
        # Run liveness check
        is_live, conf, status = self.detector.check_liveness(frame, face)
        
        # Draw liveness information
        processed_frame = self.detector.draw_liveness_info(
            frame.copy(), face, status, conf
        )
        
        # Store result if student is recognized
        if student_id is not None and is_live:
            self.liveness_results[student_id] = {
                'is_live': is_live,
                'confidence': conf,
                'status': status,
                'timestamp': time.time()
            }
        
        liveness_info = {
            'is_live': is_live,
            'confidence': conf,
            'status': status,
            'checks': self.detector.liveness_checks.copy()
        }
        
        return processed_frame, is_live, liveness_info
    
    def reset_detector(self):
        """Reset the liveness detector"""
        self.detector.reset()
    
    def enable_liveness(self, enabled=True):
        """Enable or disable liveness detection"""
        self.liveness_enabled = enabled
    
    def get_liveness_result(self, student_id):
        """Get stored liveness result for a student"""
        return self.liveness_results.get(student_id, None)
    
    def clear_results(self):
        """Clear all stored liveness results"""
        self.liveness_results.clear()


# Example usage with the existing face recognition module
"""
To integrate with face_recognition_module.py:

1. Import this module at the top of face_recognition_module.py:
   from liveness_detection import LivenessIntegration

2. In FaceRecognitionModule.__init__, add:
   self.liveness = LivenessIntegration()

3. In process_video method, modify the face processing loop:
   
   # Before recognition
   frame, liveness_passed, liveness_info = self.liveness.process_frame_with_liveness(
       frame, faces, self.recognizer, id_, confidence
   )
   
   # Only mark attendance if liveness check passes
   if liveness_passed and confidence < 100 - self.confidence_threshold:
       if id_ not in self.recognized_students:
           self.mark_attendance(id_, name, confidence_text)
           self.recognized_students.add(id_)

4. Add liveness reset in reset_session:
   self.liveness.reset_detector()
   self.liveness.clear_results()
"""


# Standalone testing
if __name__ == "__main__":
    import tkinter as tk
    from tkinter import messagebox
    
    print("Liveness Detection Module")
    print("=" * 50)
    print("\nThis module provides anti-spoofing capabilities for the")
    print("Face Recognition Attendance System.")
    print("\nFeatures:")
    print("  ✓ Eye blink detection")
    print("  ✓ Head movement tracking")
    print("  ✓ Texture analysis (photo detection)")
    print("  ✓ Motion analysis (video detection)")
    print("\nIntegration Instructions:")
    print("  See code comments for integration with face_recognition_module.py")
    print("=" * 50)
    
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(
        "Liveness Detection Module",
        "Liveness Detection Module Loaded Successfully!\n\n"
        "Features:\n"
        "• Eye blink detection\n"
        "• Head movement tracking\n"
        "• Texture analysis\n"
        "• Motion analysis\n\n"
        "Ready to integrate with Face Recognition System."
    )