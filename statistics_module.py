
import os
import csv
from datetime import datetime

class RealTimeStatistics:
    """
    Handles all statistics calculations by reading from actual files
    """
    
    def __init__(self):
        """Initialize with base directory path"""
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
    
    def get_total_students(self):
        """
        Count total students from students.csv
        Returns: int - number of registered students
        """
        students_file = os.path.join(self.base_dir, 'student_data', 'students.csv')
        
        if not os.path.exists(students_file):
            return 0
        
        try:
            with open(students_file, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header
                # Count non-empty rows
                count = sum(1 for row in reader if any(cell.strip() for cell in row))
                return count
        except Exception as e:
            print(f"Error reading students: {e}")
            return 0
    
    def get_present_today(self):
        """
        Count unique students marked present today
        Returns: int - number of students present today
        """
        today_date = datetime.now().strftime("%Y-%m-%d")
        attendance_file = os.path.join(self.base_dir, 'attendance', f'attendance_{today_date}.csv')
        
        if not os.path.exists(attendance_file):
            return 0
        
        try:
            attended_ids = set()
            with open(attendance_file, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    student_id = row.get('StudentID', '').strip()
                    status = row.get('Status', '').strip()
                    if student_id and status == 'Present':
                        attended_ids.add(student_id)
            
            return len(attended_ids)
        except Exception as e:
            print(f"Error reading attendance: {e}")
            return 0
    
    def get_photos_collected(self):
        """
        Count total photo samples in data directory
        Returns: int - number of photo files
        """
        data_folder = os.path.join(self.base_dir, 'data')
        
        if not os.path.exists(data_folder):
            return 0
        
        try:
            photo_count = 0
            for filename in os.listdir(data_folder):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    photo_count += 1
            return photo_count
        except Exception as e:
            print(f"Error counting photos: {e}")
            return 0
    
    def get_models_trained(self):
        """
        Check if trained model exists and is valid
        Returns: int - 1 if model exists, 0 otherwise
        """
        model_file = os.path.join(self.base_dir, 'trainer', 'trainer.yml')
        
        try:
            if os.path.exists(model_file) and os.path.getsize(model_file) > 0:
                return 1
            return 0
        except Exception as e:
            print(f"Error checking model: {e}")
            return 0
    
    def get_all_statistics(self):
        """
        Get all statistics at once
        Returns: dict with all statistics
        """
        return {
            'total_students': self.get_total_students(),
            'present_today': self.get_present_today(),
            'photos_collected': self.get_photos_collected(),
            'models_trained': self.get_models_trained()
        }
    
    def get_photos_per_student(self):
        """
        Get photo count per student
        Returns: dict with student_id as key and photo count as value
        """
        data_folder = os.path.join(self.base_dir, 'data')
        
        if not os.path.exists(data_folder):
            return {}
        
        student_photos = {}
        
        try:
            for filename in os.listdir(data_folder):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    # Extract student ID from filename (format: User.ID.Number.jpg)
                    parts = filename.split('.')
                    if len(parts) >= 2:
                        student_id = parts[1]
                        student_photos[student_id] = student_photos.get(student_id, 0) + 1
            
            return student_photos
        except Exception as e:
            print(f"Error getting photo stats: {e}")
            return {}
    
    def validate_system_files(self):
        """
        Check if all required directories and files exist
        Returns: dict with validation results
        """
        validation = {
            'student_data_folder': os.path.exists(os.path.join(self.base_dir, 'student_data')),
            'students_csv': os.path.exists(os.path.join(self.base_dir, 'student_data', 'students.csv')),
            'data_folder': os.path.exists(os.path.join(self.base_dir, 'data')),
            'trainer_folder': os.path.exists(os.path.join(self.base_dir, 'trainer')),
            'trainer_model': os.path.exists(os.path.join(self.base_dir, 'trainer', 'trainer.yml')),
            'attendance_folder': os.path.exists(os.path.join(self.base_dir, 'attendance'))
        }
        
        return validation


# Test function
if __name__ == "__main__":
    print("=" * 70)
    print("SMIT FACE RECOGNITION SYSTEM - REAL-TIME STATISTICS TEST")
    print("=" * 70)
    
    stats = RealTimeStatistics()
    all_stats = stats.get_all_statistics()
    
    print("\n📊 CURRENT STATISTICS:")
    print("-" * 70)
    print(f"📚 Total Students:     {all_stats['total_students']}")
    print(f"✅ Present Today:      {all_stats['present_today']}")
    print(f"📸 Photos Collected:   {all_stats['photos_collected']}")
    print(f"🧠 Models Trained:     {all_stats['models_trained']}")
    
    # Photo details
    photos_per_student = stats.get_photos_per_student()
    if photos_per_student:
        print("\n📸 PHOTOS PER STUDENT:")
        print("-" * 70)
        for student_id, count in sorted(photos_per_student.items()):
            print(f"   Student {student_id}: {count} photos")
    
    # System validation
    print("\n🔍 SYSTEM VALIDATION:")
    print("-" * 70)
    validation = stats.validate_system_files()
    for item, exists in validation.items():
        status = "✅" if exists else "❌"
        print(f"   {status} {item.replace('_', ' ').title()}")
    

    print("\n" + "=" * 70)
