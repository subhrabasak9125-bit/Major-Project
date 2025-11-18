import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
from datetime import datetime
import json
import os

class EnhancedIDCardScanner:
    """
    Enhanced ID Card Scanner for SMIT Face Recognition System
    
    Features:
    - Multi-format ID card support
    - Advanced OCR with preprocessing
    - Batch verification support
    - Detailed verification reports
    - Manual override capability
    - Confidence scoring
    """
    
    def __init__(self):
        # SMIT-specific patterns (updated for new format)
        self.patterns = {
            'student_id_smit': r'(\d{2}\s*-\s*\d{2}\s*/\s*[A-Z]+\s*/\s*\d{3,4})',
            'student_id_numeric': r'ID\s*No[:\s]*(\d{3,5})',
            'name': r'([A-Z][A-Z\s]{3,35})',
            'registration': r'Registration[:\s]*([A-Z0-9\-/]+)',
            'dob': r'Date\s*of\s*Birth[:\s]*(\d{1,2}[./]\d{1,2}[./]\d{4})',
            'blood_group': r'Blood\s*Gr[:\s]*([ABO][+-])',
            'phone': r'Phone[:\s]*(\d{5}\s*\d{5}|\d{10})',
            'session': r'Session[:\s]*(\d{4}\s*-\s*\d{4})',
            'department': r'(DCSE|DCE|DME|DEE|DETC)',
            'stream': r'Stream[:\s]*([A-Za-z\s&]+)',
        }
        
        # Enhanced blue color detection for SMIT cards
        self.lower_blue = np.array([85, 40, 40])
        self.upper_blue = np.array([135, 255, 255])
        
        # Verification history
        self.verification_history = []
        self.batch_results = []
        
        # Manual overrides storage
        self.manual_overrides = self.load_manual_overrides()
    
    def load_manual_overrides(self):
        """Load manual verification overrides"""
        override_file = 'data/id_verification_overrides.json'
        if os.path.exists(override_file):
            try:
                with open(override_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def save_manual_override(self, student_id, override_data):
        """Save manual verification override"""
        self.manual_overrides[str(student_id)] = {
            'timestamp': datetime.now().isoformat(),
            'data': override_data,
            'reason': override_data.get('reason', 'Manual verification')
        }
        
        os.makedirs('data', exist_ok=True)
        with open('data/id_verification_overrides.json', 'w') as f:
            json.dump(self.manual_overrides, f, indent=2)
    
    def enhanced_preprocess(self, image):
        """Advanced preprocessing for better OCR"""
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Morphological operations to connect text
        kernel = np.ones((1, 1), np.uint8)
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Enhance contrast with CLAHE
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        return [enhanced, thresh, morph]
    
    def detect_id_card_advanced(self, frame):
        """Advanced ID card detection with multiple methods"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Multi-stage color detection
        mask = cv2.inRange(hsv, self.lower_blue, self.upper_blue)
        
        # Advanced morphological operations
        kernel_close = np.ones((7,7), np.uint8)
        kernel_open = np.ones((5,5), np.uint8)
        
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
        
        # Edge detection for card boundaries
        edges = cv2.Canny(mask, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None, None, 0
        
        # Find best candidate
        best_contour = None
        best_score = 0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            if area < 30000:  # Minimum area
                continue
            
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            
            # Score based on area and aspect ratio
            score = 0
            if 1.2 < aspect_ratio < 1.9:  # ID card aspect ratio
                score += 50
            
            if area > 50000:
                score += 30
            
            # Check rectangularity
            rect_area = w * h
            extent = area / float(rect_area)
            if extent > 0.7:
                score += 20
            
            if score > best_score:
                best_score = score
                best_contour = contour
        
        if best_contour is None:
            return None, None, 0
        
        x, y, w, h = cv2.boundingRect(best_contour)
        card_image = frame[y:y+h, x:x+w]
        
        return (x, y, w, h), card_image, best_score
    
    def extract_text_advanced(self, image):
        """Advanced OCR with multiple preprocessing attempts"""
        texts = []
        
        # Try multiple preprocessing methods
        preprocessed_images = self.enhanced_preprocess(image)
        
        for idx, proc_img in enumerate(preprocessed_images):
            try:
                # Try different PSM modes
                configs = [
                    '--psm 6',  # Uniform block of text
                    '--psm 4',  # Single column of text
                    '--psm 3',  # Fully automatic
                ]
                
                for config in configs:
                    text = pytesseract.image_to_string(proc_img, config=config)
                    if text.strip():
                        texts.append(text)
            except Exception as e:
                continue
        
        # Combine all texts and return most complete
        combined = '\n'.join(texts)
        return combined if combined else ""
    
    def parse_smit_id_card(self, text):
        """Enhanced parsing specifically for SMIT ID cards"""
        data = {
            'student_id': None,
            'registration_no': None,
            'name': None,
            'dob': None,
            'blood_group': None,
            'phone': None,
            'session': None,
            'department': None,
            'stream': None,
            'valid': False,
            'confidence': 0
        }
        
        confidence_score = 0
        
        # Extract student ID (SMIT format)
        match = re.search(self.patterns['student_id_smit'], text, re.IGNORECASE)
        if match:
            data['student_id'] = match.group(1).strip()
            confidence_score += 30
        else:
            # Try numeric ID format
            match = re.search(self.patterns['student_id_numeric'], text, re.IGNORECASE)
            if match:
                data['student_id'] = match.group(1).strip()
                confidence_score += 25
        
        # Extract registration number
        match = re.search(self.patterns['registration'], text, re.IGNORECASE)
        if match:
            data['registration_no'] = match.group(1).strip()
            confidence_score += 15
        
        # Extract name (improved logic)
        lines = text.split('\n')
        for i, line in enumerate(lines):
            # Look for uppercase names after ID
            if data['student_id'] and i > 0:
                potential_name = line.strip()
                if potential_name.isupper() and len(potential_name) > 3 and len(potential_name.split()) <= 4:
                    # Filter out common non-name text
                    if not any(word in potential_name for word in ['INSTITUTE', 'TECHNOLOGY', 'DIPLOMA', 'ENGINEERING']):
                        data['name'] = potential_name
                        confidence_score += 25
                        break
        
        # Extract department
        match = re.search(self.patterns['department'], text)
        if match:
            data['department'] = match.group(1)
            confidence_score += 10
        
        # Extract DOB
        match = re.search(self.patterns['dob'], text, re.IGNORECASE)
        if match:
            data['dob'] = match.group(1).strip()
            confidence_score += 10
        
        # Extract blood group
        match = re.search(self.patterns['blood_group'], text, re.IGNORECASE)
        if match:
            data['blood_group'] = match.group(1).strip()
            confidence_score += 5
        
        # Extract phone
        match = re.search(self.patterns['phone'], text, re.IGNORECASE)
        if match:
            data['phone'] = match.group(1).strip()
            confidence_score += 5
        
        # Extract session
        match = re.search(self.patterns['session'], text, re.IGNORECASE)
        if match:
            data['session'] = match.group(1).strip()
            confidence_score += 5
        
        # Extract stream
        match = re.search(self.patterns['stream'], text, re.IGNORECASE)
        if match:
            data['stream'] = match.group(1).strip()
            confidence_score += 5
        
        # Determine validity
        data['confidence'] = min(100, confidence_score)
        if data['student_id'] and data['name'] and confidence_score >= 50:
            data['valid'] = True
        
        return data
    
    def verify_with_database(self, scanned_data, expected_student_id, expected_name):
        """
        Enhanced verification with database cross-checking
        """
        # Check for manual override first
        if str(expected_student_id) in self.manual_overrides:
            override = self.manual_overrides[str(expected_student_id)]
            return True, 100, {
                'status': 'manual_override',
                'override_reason': override.get('reason'),
                'override_date': override.get('timestamp'),
                **scanned_data
            }
        
        if not scanned_data['valid']:
            return False, 0, {'error': 'Invalid ID card scan', **scanned_data}
        
        confidence = 0
        details = {}
        
        # Extract numeric ID from SMIT format
        scanned_id = scanned_data['student_id']
        if '/' in scanned_id:
            # Format: 23-24/DCSE/1011
            parts = scanned_id.split('/')
            if len(parts) >= 3:
                scanned_numeric = parts[-1].strip()
            else:
                scanned_numeric = ''.join(filter(str.isdigit, scanned_id))
        else:
            scanned_numeric = ''.join(filter(str.isdigit, scanned_id))
        
        expected_id_str = str(expected_student_id).strip()
        
        # ID verification with multiple checks
        id_match = False
        if scanned_numeric == expected_id_str:
            confidence += 40
            id_match = True
        elif scanned_numeric.endswith(expected_id_str) or expected_id_str in scanned_numeric:
            confidence += 30
            id_match = True
        elif expected_id_str.endswith(scanned_numeric):
            confidence += 25
            id_match = True
        
        details['id_match'] = id_match
        details['scanned_id'] = scanned_data['student_id']
        details['expected_id'] = expected_id_str
        
        if not id_match:
            details['error'] = f"ID mismatch: Expected {expected_id_str}, Got {scanned_numeric}"
            return False, confidence, details
        
        # Name verification with fuzzy matching
        scanned_name = scanned_data['name'].upper() if scanned_data['name'] else ""
        expected_name_upper = expected_name.upper()
        
        # Split names into words
        scanned_words = set(scanned_name.split())
        expected_words = set(expected_name_upper.split())
        
        # Calculate word overlap
        if expected_words:
            overlap = len(scanned_words & expected_words)
            name_confidence = (overlap / len(expected_words)) * 100
            
            if name_confidence >= 60:
                confidence += 40
                details['name_match'] = True
            elif name_confidence >= 40:
                confidence += 25
                details['name_match'] = 'partial'
            else:
                confidence += 10
                details['name_match'] = False
        
        # Bonus points for additional verified fields
        if scanned_data.get('department'):
            confidence += 5
        if scanned_data.get('registration_no'):
            confidence += 5
        if scanned_data.get('dob'):
            confidence += 5
        if scanned_data.get('session'):
            confidence += 5
        
        details['scanned_name'] = scanned_data['name']
        details['expected_name'] = expected_name
        details['registration_no'] = scanned_data.get('registration_no', 'N/A')
        details['dob'] = scanned_data.get('dob', 'N/A')
        details['blood_group'] = scanned_data.get('blood_group', 'N/A')
        details['department'] = scanned_data.get('department', 'N/A')
        details['session'] = scanned_data.get('session', 'N/A')
        details['scan_confidence'] = scanned_data['confidence']
        
        # Overall match determination
        match = confidence >= 70
        
        # Log verification attempt
        self.log_verification(expected_student_id, scanned_data, match, confidence, details)
        
        return match, confidence, details
    
    def log_verification(self, student_id, scanned_data, success, confidence, details):
        """Log verification attempts for audit trail"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'student_id': student_id,
            'success': success,
            'confidence': confidence,
            'scanned_data': scanned_data,
            'details': details
        }
        
        self.verification_history.append(log_entry)
        
        # Save to file
        os.makedirs('logs', exist_ok=True)
        log_file = f'logs/id_verification_{datetime.now().strftime("%Y%m%d")}.json'
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            logs.append(log_entry)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        except:
            pass
    
    def batch_verify(self, batch_data):
        """
        Batch verification for multiple students
        batch_data: list of tuples (frame, expected_id, expected_name)
        """
        results = []
        
        for idx, (frame, expected_id, expected_name) in enumerate(batch_data):
            card_rect, card_img, detect_score = self.detect_id_card_advanced(frame)
            
            if card_rect and card_img is not None:
                text = self.extract_text_advanced(card_img)
                scanned_data = self.parse_smit_id_card(text)
                match, confidence, details = self.verify_with_database(
                    scanned_data, expected_id, expected_name
                )
                
                results.append({
                    'index': idx,
                    'student_id': expected_id,
                    'match': match,
                    'confidence': confidence,
                    'details': details,
                    'detection_score': detect_score
                })
            else:
                results.append({
                    'index': idx,
                    'student_id': expected_id,
                    'match': False,
                    'confidence': 0,
                    'error': 'ID card not detected',
                    'detection_score': 0
                })
        
        self.batch_results = results
        return results
    
    def generate_verification_report(self, output_path='reports'):
        """Generate detailed verification report"""
        os.makedirs(output_path, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'{output_path}/verification_report_{timestamp}.txt'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("ID CARD VERIFICATION REPORT\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Verifications: {len(self.verification_history)}\n\n")
            
            # Summary statistics
            successful = sum(1 for v in self.verification_history if v['success'])
            failed = len(self.verification_history) - successful
            
            if self.verification_history:
                avg_confidence = sum(v['confidence'] for v in self.verification_history) / len(self.verification_history)
            else:
                avg_confidence = 0
            
            f.write("SUMMARY\n")
            f.write("-" * 80 + "\n")
            f.write(f"Successful Verifications: {successful}\n")
            f.write(f"Failed Verifications: {failed}\n")
            f.write(f"Success Rate: {(successful/len(self.verification_history)*100) if self.verification_history else 0:.1f}%\n")
            f.write(f"Average Confidence: {avg_confidence:.1f}%\n\n")
            
            # Detailed entries
            f.write("DETAILED LOG\n")
            f.write("-" * 80 + "\n")
            
            for entry in self.verification_history[-50:]:  # Last 50 entries
                f.write(f"\nTimestamp: {entry['timestamp']}\n")
                f.write(f"Student ID: {entry['student_id']}\n")
                f.write(f"Status: {'✓ VERIFIED' if entry['success'] else '✗ FAILED'}\n")
                f.write(f"Confidence: {entry['confidence']}%\n")
                f.write(f"Scanned Name: {entry['scanned_data'].get('name', 'N/A')}\n")
                f.write(f"Scanned ID: {entry['scanned_data'].get('student_id', 'N/A')}\n")
                
                if 'error' in entry['details']:
                    f.write(f"Error: {entry['details']['error']}\n")
                
                f.write("-" * 40 + "\n")
        
        return report_file
    
    def draw_enhanced_detection(self, frame, card_rect, data, status, confidence):
        """Enhanced visualization with more information"""
        if card_rect:
            x, y, w, h = card_rect
            
            # Status-based colors
            if status == 'verified':
                color = (0, 255, 0)
                status_text = "✓ VERIFIED"
            elif status == 'failed':
                color = (0, 0, 255)
                status_text = "✗ FAILED"
            elif status == 'manual_override':
                color = (255, 165, 0)
                status_text = "⚠ MANUAL OVERRIDE"
            else:
                color = (255, 165, 0)
                status_text = "⋯ SCANNING"
            
            # Draw thick border
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 4)
            
            # Draw corner markers
            corner_size = 20
            cv2.line(frame, (x, y), (x+corner_size, y), color, 6)
            cv2.line(frame, (x, y), (x, y+corner_size), color, 6)
            cv2.line(frame, (x+w, y), (x+w-corner_size, y), color, 6)
            cv2.line(frame, (x+w, y), (x+w, y+corner_size), color, 6)
            cv2.line(frame, (x, y+h), (x+corner_size, y+h), color, 6)
            cv2.line(frame, (x, y+h), (x, y+h-corner_size), color, 6)
            cv2.line(frame, (x+w, y+h), (x+w-corner_size, y+h), color, 6)
            cv2.line(frame, (x+w, y+h), (x+w, y+h-corner_size), color, 6)
            
            # Status banner
            banner_height = 40
            overlay = frame.copy()
            cv2.rectangle(overlay, (x, y-banner_height), (x+w, y), color, -1)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
            
            cv2.putText(frame, status_text, (x+10, y-12),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            
            # Information display
            if data and data.get('valid'):
                info_y = y + h + 30
                font_scale = 0.6
                thickness = 2
                
                # Display extracted information
                info_items = [
                    f"ID: {data.get('student_id', 'N/A')}",
                    f"Name: {data.get('name', 'N/A')}",
                    f"Confidence: {confidence}%"
                ]
                
                if data.get('department'):
                    info_items.append(f"Dept: {data['department']}")
                
                for idx, info in enumerate(info_items):
                    cv2.putText(frame, info, (x, info_y + idx*25),
                               cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)
        
        return frame


# Installation check function
def check_installation():
    """Check if all required components are installed"""
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"✓ Tesseract OCR {version} installed")
        return True
    except Exception as e:
        print(f"✗ Tesseract OCR not found: {e}")
        print("\nInstallation Instructions:")
        print("1. Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Install to default location")
        print("3. pip install pytesseract")
        return False


if __name__ == "__main__":
    print("Enhanced ID Card Scanner Module - SMIT")
    print("=" * 50)
    check_installation()
    print("\nFeatures:")
    print("✓ Advanced SMIT ID card detection")
    print("✓ Multi-format support")
    print("✓ Batch verification")
    print("✓ Manual override capability")
    print("✓ Detailed verification reports")
    print("✓ Audit trail logging")