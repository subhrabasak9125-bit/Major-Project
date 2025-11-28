import os
import csv
from datetime import datetime, timedelta
import glob

class RealTimeStatistics:
    """
    Enhanced Real-time Statistics with comprehensive data tracking
    """
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
    
    def get_total_students(self):
        """Count total students from students.csv"""
        students_file = os.path.join(self.base_dir, 'student_data', 'students.csv')
        
        if not os.path.exists(students_file):
            return 0
        
        try:
            with open(students_file, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header
                count = sum(1 for row in reader if any(cell.strip() for cell in row))
                return count
        except Exception as e:
            print(f"Error reading students: {e}")
            return 0
    
    def get_present_today(self):
        """Count unique students marked present today"""
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
        """Count total photo samples in data directory"""
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
        """Check if trained model exists and return training status"""
        model_file = os.path.join(self.base_dir, 'trainer', 'trainer.yml')
        
        try:
            if os.path.exists(model_file) and os.path.getsize(model_file) > 0:
                return 1  # Model is trained
            return 0  # Model not trained
        except Exception as e:
            print(f"Error checking model: {e}")
            return 0
    
    def get_training_progress(self):
        """Calculate training progress percentage"""
        data_folder = os.path.join(self.base_dir, 'data')
        model_file = os.path.join(self.base_dir, 'trainer', 'trainer.yml')
        
        if not os.path.exists(data_folder):
            return 0
        
        # Count total images
        total_images = len([f for f in os.listdir(data_folder) 
                           if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        
        if total_images == 0:
            return 0
        
        # If model exists, consider it 95% trained (simulating progress)
        if os.path.exists(model_file) and os.path.getsize(model_file) > 0:
            return 95  # Simulating 95% trained when model exists
        
        # Calculate progress based on image count (simplified)
        min_images_for_training = 50
        progress = min(80, (total_images / min_images_for_training) * 80)
        return int(progress)
    
    def get_total_attendance_records(self):
        """Count total attendance records across all files"""
        attendance_dir = os.path.join(self.base_dir, 'attendance')
        
        if not os.path.exists(attendance_dir):
            return 0
        
        total_records = 0
        try:
            for filename in os.listdir(attendance_dir):
                if filename.startswith("attendance_") and filename.endswith(".csv"):
                    filepath = os.path.join(attendance_dir, filename)
                    with open(filepath, 'r', encoding='utf-8', newline='') as f:
                        reader = csv.reader(f)
                        next(reader, None)  # Skip header
                        total_records += sum(1 for row in reader if any(cell.strip() for cell in row))
            return total_records
        except Exception as e:
            print(f"Error counting attendance records: {e}")
            return 0
    
    def get_recent_activity(self, limit=8):
        """Get recent attendance activity for real-time feed"""
        today_date = datetime.now().strftime("%Y-%m-%d")
        attendance_file = os.path.join(self.base_dir, 'attendance', f'attendance_{today_date}.csv')
        
        if not os.path.exists(attendance_file):
            return []
        
        try:
            activities = []
            with open(attendance_file, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    student_id = row.get('StudentID', '').strip()
                    name = row.get('Name', '').strip()
                    time = row.get('Time', '').strip()
                    status = row.get('Status', '').strip()
                    
                    if student_id and name and status == 'Present':
                        # Clean name for display
                        clean_name = name.encode('ascii', 'ignore').decode('ascii')
                        if not clean_name:
                            clean_name = f"Student_{student_id}"
                        
                        activities.append({
                            'id': student_id,
                            'name': clean_name,
                            'time': time,
                            'status': status
                        })
            
            # Return most recent activities (limit)
            return activities[-limit:]
        except Exception as e:
            print(f"Error reading recent activity: {e}")
            return []
        
    def get_last_7_days_attendance(self):
        """Returns list of last 7 days present count"""
        attendance_dir = os.path.join(self.base_dir, 'attendance')

        result = []
        for i in range(7):
            day = datetime.now() - timedelta(days=i)
            file = os.path.join(attendance_dir, f"attendance_{day.strftime('%Y-%m-%d')}.csv")

            if not os.path.exists(file):
                result.append(0)
                continue

            try:
                count = 0
                with open(file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                            if row.get("Status") == "Present":
                                count += 1
                result.append(count)
            except:
                result.append(0)

        return list(reversed(result))
    
    def get_department_distribution(self):
        """Returns dict: department -> count"""
        students_file = os.path.join(self.base_dir, 'student_data', 'students.csv')

        if not os.path.exists(students_file):
            return {}

        dept_count = {}

        with open(students_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dept = row.get("Department", "").strip()
                if dept:
                    dept_count[dept] = dept_count.get(dept, 0) + 1

        return dept_count

    def get_weekly_performance(self):
        """Returns present count per week for last 4 weeks"""
        attendance_dir = os.path.join(self.base_dir, "attendance")

        weekly = [0, 0, 0, 0]  # Week1, Week2, Week3, Week4

        for filename in glob.glob(os.path.join(attendance_dir, "attendance_*.csv")):
            date_str = filename.split("attendance_")[1].split(".csv")[0]
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                week_index = (datetime.now() - date).days // 7
                if 0 <= week_index < 4:
                    with open(filename, "r") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            if row.get("Status") == "Present":
                                weekly[3 - week_index] += 1
            except:
                pass

        return weekly
    
    
    def get_realtime_activity_counts(self):
        """Returns number of check-ins in last 10 minutes"""
        today = datetime.now().strftime("%Y-%m-%d")
        file = os.path.join(self.base_dir, "attendance", f"attendance_{today}.csv")

        activity = []

        if not os.path.exists(file):
            return activity

        now = datetime.now()

        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                t = row.get("Time", "")
                try:
                    timestamp = datetime.strptime(t, "%H:%M:%S")
                    total = datetime.combine(datetime.today(), timestamp.time())
                    if (now - total).seconds <= 600:  # last 10 min
                        activity.append(t)
                except:
                    pass

        return activity
   

    
    def get_student_names_map(self):
        """Create a mapping of student IDs to names"""
        students_file = os.path.join(self.base_dir, 'student_data', 'students.csv')
        
        if not os.path.exists(students_file):
            return {}
        
        try:
            name_map = {}
            with open(students_file, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    student_id = row.get('StudentID', '').strip()
                    name = row.get('Name', '').strip()
                    if student_id and name:
                        # Clean name
                        clean_name = name.encode('ascii', 'ignore').decode('ascii')
                        if clean_name:
                            name_map[student_id] = clean_name
            return name_map
        except Exception as e:
            print(f"Error reading student names: {e}")
            return {}
    
    def get_all_statistics(self):
        """Get all statistics at once for efficient updates"""
        return {
            'total_students': self.get_total_students(),
            'present_today': self.get_present_today(),
            'photos_collected': self.get_photos_collected(),
            'models_trained': self.get_models_trained(),
            'training_progress': self.get_training_progress(),
            'total_records': self.get_total_attendance_records(),
            'recent_activity': self.get_recent_activity(8),
            'last_update': datetime.now().strftime("%H:%M:%S")
        }


# Test function
if __name__ == "__main__":
    print("=" * 70)
    print("ENHANCED REAL-TIME STATISTICS MODULE")
    print("=" * 70)
    
    stats = RealTimeStatistics()
    all_stats = stats.get_all_statistics()
    
    print("\n📊 REAL-TIME STATISTICS:")
    print("-" * 70)
    print(f"📚 Total Students:     {all_stats['total_students']}")
    print(f"✅ Present Today:      {all_stats['present_today']}")
    print(f"📸 Photos Collected:   {all_stats['photos_collected']}")
    print(f"🧠 Models Trained:     {all_stats['models_trained']}")
    print(f"📊 Training Progress:  {all_stats['training_progress']}%")
    print(f"📈 Total Records:      {all_stats['total_records']}")
    print(f"🕒 Last Update:        {all_stats['last_update']}")
    
    print("\n🔄 RECENT ACTIVITY:")
    print("-" * 70)
    for activity in all_stats['recent_activity']:
        print(f"   {activity['name']} - {activity['time']} ✓")
    
    print("\n" + "=" * 70)