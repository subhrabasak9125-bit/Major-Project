# 🎓 Face Recognition Attendance System

A comprehensive face recognition-based attendance system developed by SMIT Students. This system uses OpenCV and machine learning to automatically mark attendance based on facial recognition.

## ✨ Features

- **Student Management System** - Complete CRUD operations for student data
- **Photo Sample Collection** - Automatic capture of 100+ training images
- **AI Model Training** - LBPH (Local Binary Patterns Histograms) algorithm
- **Real-time Face Recognition** - Live camera feed with instant detection
- **Automatic Attendance Marking** - No manual intervention required
- **Attendance Reports** - View, search, and export attendance data
- **Modern UI** - Professional dark-themed interface

## 📋 Requirements

### Software Requirements
- Python 3.7 or higher
- Webcam (built-in or external)
- Windows/Linux/macOS

### Python Libraries
```bash
pip install opencv-python opencv-contrib-python pillow numpy
```

## 📁 Project Structure

```
face-recognition-attendance/
│
├── face_recognition_ui.py          # Main application entry point
├── student_management.py           # Student CRUD operations
├── face_recognition_module.py      # Face recognition & attendance
├── train_data_module.py           # Model training
├── photo_capture_module.py        # Photo sample collection
├── attendance_viewer.py           # Attendance reports & export
│
├── data/                          # Photo samples storage
├── trainer/                       # Trained model storage
│   └── trainer.yml               # Trained LBPH model
├── student_data/                 # Student information
│   └── students.csv              # Student database
└── attendance/                   # Attendance records
    └── attendance_YYYY-MM-DD.csv # Daily attendance files
```

## 🚀 Installation

### Step 1: Clone or Download
Download all Python files to a single directory.

### Step 2: Install Dependencies
```bash
pip install opencv-python opencv-contrib-python pillow numpy
```

**Note:** Use `opencv-contrib-python` (not just `opencv-python`) to get the face recognition modules.

### Step 3: Verify Installation
```python
# Test script - save as test_install.py
import cv2
import PIL
import numpy as np

print("OpenCV version:", cv2.__version__)
print("PIL version:", PIL.__version__)
print("NumPy version:", np.__version__)

# Test face recognizer
try:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    print("✓ Face recognizer available!")
except:
    print("✗ Face recognizer NOT available - install opencv-contrib-python")
```

## 📖 User Guide

### Complete Workflow

#### 1️⃣ Add Student Information
1. Launch the application: `python face_recognition_ui.py`
2. Click **"STUDENT DETAILS"**
3. Fill in student information:
   - Student ID (must be unique number)
   - Student Name
   - Department, Course, Year, Semester
   - Class Division, Roll Number
   - Personal details (DOB, Email, Phone, Address)
4. Click **"SAVE"** button

#### 2️⃣ Capture Photo Samples
1. After saving student, click **"ADD PHOTO SAMPLE"**
   - OR from main menu: **"STUDENT DETAILS"** → Select student → **"ADD PHOTO SAMPLE"**
2. Position face in camera frame
3. System automatically captures 100 photos
4. Try different angles and expressions
5. Wait for completion message

**Tips for Better Photos:**
- Good, consistent lighting
- Face the camera directly
- Remove glasses if possible
- Neutral expressions work best
- Avoid extreme angles

#### 3️⃣ Train the Model
1. From main menu, click **"TRAIN DATA"**
2. Click **"SCAN IMAGES"** to detect available photos
3. Verify student count and image count
4. Click **"START TRAINING"**
5. Wait for training to complete (may take 1-5 minutes)
6. Success message confirms model is ready

**Training Tips:**
- Train all students before starting recognition
- Minimum 50 photos per student
- Recommended: 100-150 photos per student
- Retrain if adding new students

#### 4️⃣ Mark Attendance
1. From main menu, click **"FACE RECOGNITION"**
2. Click **"START CAMERA"**
3. Students face the camera
4. System automatically:
   - Detects faces
   - Recognizes students
   - Marks attendance
   - Displays confidence score
5. View recognized students in real-time table

**Recognition Settings:**
- Adjust **Confidence Threshold** slider (default 50%)
- Higher = more strict (fewer false positives)
- Lower = more lenient (may accept unknown faces)

#### 5️⃣ View Attendance Reports
1. From main menu, click **"ATTENDANCE"**
2. Select date from dropdown
3. Search by student name or ID
4. Export to CSV or TXT format

## 🎛️ Module Details

### Student Management Module
**File:** `student_management.py`

Features:
- Add new students
- Update existing records
- Delete student records
- Search functionality
- View all students
- Direct photo capture integration

### Photo Capture Module
**File:** `photo_capture_module.py`

Features:
- Automatic face detection
- Configurable sample count (50-200)
- Real-time preview
- Progress tracking
- Saves in correct format for training

### Training Module
**File:** `train_data_module.py`

Features:
- Image scanning and validation
- LBPH model training
- Progress visualization
- Training logs
- Model saving

### Face Recognition Module
**File:** `face_recognition_module.py`

Features:
- Real-time face detection
- Student recognition
- Automatic attendance marking
- Confidence scoring
- Session management
- CSV export

### Attendance Viewer Module
**File:** `attendance_viewer.py`

Features:
- Date-wise viewing
- Student search
- Export to CSV/TXT
- Statistics display
- Multi-date reports

## 🔧 Configuration

### Camera Settings
Edit in `photo_capture_module.py` and `face_recognition_module.py`:
```python
self.cap = cv2.VideoCapture(0)  # Change 0 to 1, 2, etc. for external cameras
```

### Confidence Threshold
Adjust in Face Recognition module UI or edit default:
```python
self.confidence_threshold = 50  # 0-100, higher = stricter
```

### Photo Sample Count
Adjust in Photo Capture module UI or edit default:
```python
self.max_photos = 100  # 50-200 recommended
```

## 📊 Data Management

### Student Data Format
**File:** `student_data/students.csv`
```csv
StudentID,Name,Department,Course,Year,Semester,Division,RollNo,Gender,DOB,Email,Phone,Address,Teacher
1,John Doe,Computer,TE,2020-2021,Semester-1,A,101,Male,01/01/2000,john@email.com,1234567890,Address,Teacher Name
```

### Attendance Format
**File:** `attendance/attendance_YYYY-MM-DD.csv`
```csv
StudentID,Name,Time,Confidence,Date
1,John Doe,14:30:15,85%,2024-01-15
```

### Photo Naming Format
**Directory:** `data/`
```
User.1.1.jpg
User.1.2.jpg
...
User.1.100.jpg
```
Format: `User.{StudentID}.{PhotoNumber}.jpg`

## ❓ Troubleshooting

### Camera Issues

**Problem:** Camera not opening
```python
# Solution 1: Try different camera index
self.cap = cv2.VideoCapture(1)  # or 2, 3, etc.

# Solution 2: Check camera permissions
# Windows: Settings → Privacy → Camera
# Linux: Check /dev/video* permissions
```

**Problem:** Camera already in use
- Close other applications using camera
- Restart the application

### Recognition Issues

**Problem:** Low recognition accuracy
- **Solution 1:** Capture more training samples (150-200)
- **Solution 2:** Improve lighting conditions
- **Solution 3:** Retrain model
- **Solution 4:** Lower confidence threshold

**Problem:** "Unknown" faces
- Ensure model is trained
- Check confidence threshold (try lowering)
- Verify training data exists for student

**Problem:** False positives
- Increase confidence threshold
- Capture more diverse training samples
- Ensure good lighting during training

### Training Issues

**Problem:** "No faces detected"
- Check if photos are in `data/` folder
- Verify photo naming format
- Ensure photos contain visible faces

**Problem:** Training fails
- Install `opencv-contrib-python` (not just opencv-python)
```bash
pip uninstall opencv-python
pip install opencv-contrib-python
```

**Problem:** Model file not found
- Check `trainer/trainer.yml` exists
- Retrain model if file is missing

### File/Import Issues

**Problem:** Module not found
- Ensure all .py files are in same directory
- Check file names match exactly
- Verify Python is running from correct directory

**Problem:** CSV errors
- Check CSV file encoding (should be UTF-8)
- Verify CSV structure matches expected format
- Delete corrupted CSV and let system recreate

## 🔐 Security & Privacy

### Data Protection
- All data stored locally
- No cloud/internet connection required
- Student photos never transmitted
- Attendance records encrypted (optional - implement if needed)

### Recommendations
- Regularly backup `student_data/` and `attendance/` folders
- Restrict file access to authorized users
- Review and approve attendance records
- Consider manual verification for critical systems

## 🎯 Performance Optimization

### Speed Improvements
```python
# Reduce frame processing rate
self.window.after(50, self.process_capture)  # Increase to 100 for slower PCs

# Lower image resolution
img = img.resize((320, 240))  # Instead of (640, 480)
```

### Accuracy Improvements
1. **Better Training Data:**
   - Capture 150-200 samples per student
   - Include variety of expressions
   - Multiple lighting conditions
   - Different angles (±30 degrees)

2. **Environmental Control:**
   - Consistent lighting
   - Plain background
   - Camera at eye level
   - 2-3 feet from camera

## 📞 Support

### Common Questions

**Q: How many students can the system handle?**
A: No hard limit. Tested with 100+ students successfully.

**Q: Does it work with glasses?**
A: Yes, but accuracy may vary. Train with glasses on.

**Q: Can it recognize multiple faces simultaneously?**
A: Yes, the system can detect and recognize multiple students at once.

**Q: How long does training take?**
A: 1-5 minutes depending on number of students and photos.

**Q: Can I use this for commercial purposes?**
A: This is an academic project. Review licenses of used libraries.

### Contact
- **Developers:** SMIT Students
- **Project Type:** Academic
- **Year:** 2024-2025

## 📝 License

This project is developed for academic purposes. Please check individual library licenses:
- OpenCV: Apache 2.0 License
- Python: PSF License
- PIL/Pillow: PIL Software License

## 🎓 Credits

**Developed By:** SMIT Students

**Technologies Used:**
- Python 3.x
- OpenCV (Computer Vision)
- Tkinter (GUI)
- PIL/Pillow (Image Processing)
- LBPH Algorithm (Face Recognition)

**Special Thanks:**
- OpenCV Community
- Python Community
- SMIT Faculty

## 🔄 Version History

### Version 1.0.0 (Current)
- Initial release
- Student management system
- Photo capture module
- Model training
- Face recognition
- Attendance marking
- Report generation

### Future Enhancements (Planned)
- Database integration (SQLite/MySQL)
- Email notifications
- SMS integration
- Facial mask detection
- Temperature screening integration
- Mobile app version
- Cloud backup
- Multi-language support

## 📚 Additional Resources

### Learning Materials
- [OpenCV Documentation](https://docs.opencv.org/)
- [Face Recognition Algorithms](https://github.com/topics/face-recognition)
- [LBPH Algorithm Explanation](https://towardsdatascience.com/face-recognition-how-lbph-works-90ec258c3d6b)

### Similar Projects
- Search GitHub for "face recognition attendance"
- OpenCV official face recognition samples
- Academic papers on biometric attendance systems

---

**Happy Coding! 🚀**

For issues or questions, please refer to the troubleshooting section or contact SMIT Students.
