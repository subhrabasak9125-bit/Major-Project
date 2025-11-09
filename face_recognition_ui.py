import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime
import tkinter.messagebox

class FaceRecognitionUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Face Recognition Attendance System Software")
        self.root.geometry("1280x720")
        self.root.configure(bg='#0a0a2e')
        self.root.state('zoomed')  # Maximize window
        
        # Create header
        self.create_header()
        
        # Create main content area
        self.create_main_content()
        
        # Create footer
        self.create_footer()
        
        # Start time update
        self.update_time()
    
    def create_header(self):
        # Header frame with gradient-like effect
        header_frame = tk.Frame(self.root, bg='#16213e', height=100)
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        # Developer info
        dev_label = tk.Label(header_frame, text="Developed By: SMIT Students", 
                           fg='white', bg='#16213e', font=('Arial', 10))
        dev_label.pack(anchor='nw', padx=10, pady=5)
        
        # Logo and title area
        title_frame = tk.Frame(header_frame, bg='#16213e')
        title_frame.pack(expand=True, fill='both')
        
        # Facial recognition logo text
        logo_label = tk.Label(title_frame, text="🔍 FACIAL\nRECOGNITION\nSOFTWARE", 
                            fg='#00ffff', bg='#16213e', font=('Arial', 12, 'bold'))
        logo_label.pack(side='left', padx=20, pady=10)
        
        # Face images placeholder (represented as colored rectangles)
        faces_frame = tk.Frame(title_frame, bg='#16213e')
        faces_frame.pack(side='left', padx=50)
        
        for i, color in enumerate(['#ff6b6b', '#4ecdc4', '#45b7d1']):
            face_frame = tk.Frame(faces_frame, bg=color, width=60, height=60)
            face_frame.pack(side='left', padx=5)
            face_frame.pack_propagate(False)
            
            # Add face placeholder
            face_label = tk.Label(face_frame, text="👤", fg='white', bg=color, font=('Arial', 20))
            face_label.pack(expand=True)
        
        # Time display
        self.time_label = tk.Label(title_frame, text="", fg='#00ffff', bg='#16213e', 
                                 font=('Arial', 14, 'bold'))
        self.time_label.pack(side='right', padx=20)
    
    def create_main_content(self):
        # Main title
        title_label = tk.Label(self.root, text="FACE RECOGNITION ATTENDANCE SYSTEM SOFTWARE", 
                             fg='#ff4444', bg='#0a0a2e', font=('Arial', 28, 'bold'))
        title_label.pack(pady=20)
        
        # Main buttons grid
        main_frame = tk.Frame(self.root, bg='#0a0a2e')
        main_frame.pack(expand=True, fill='both', padx=50, pady=20)
        
        # Create 2x4 grid of buttons
        buttons_data = [
            ("STUDENT DETAILS", "👥", self.student_details, '#4a4a8a'),
            ("FACE RECOGNITION", "🔍", self.face_recognition, '#4a4a8a'),
            ("ATTENDANCE", "📊", self.attendance, '#4a4a8a'),
            ("HELP DESK", "❓", self.help_desk, '#4a4a8a'),
            ("TRAIN DATA", "🧠", self.train_data, '#4a4a8a'),
            ("PHOTOS", "📸", self.photos, '#4a4a8a'),
            ("DEVELOPER", "💻", self.developer, '#4a4a8a'),
            ("EXIT", "🚪", self.exit_app, '#8a4a4a')
        ]
        
        # Create grid layout
        for i in range(2):  # 2 rows
            for j in range(4):  # 4 columns
                index = i * 4 + j
                if index < len(buttons_data):
                    btn_text, icon, command, color = buttons_data[index]
                    
                    # Create button frame
                    btn_frame = tk.Frame(main_frame, bg=color, relief='raised', bd=2)
                    btn_frame.grid(row=i, column=j, padx=15, pady=15, sticky='nsew')
                    
                    # Configure grid weights for responsiveness
                    main_frame.grid_rowconfigure(i, weight=1)
                    main_frame.grid_columnconfigure(j, weight=1)
                    
                    # Icon
                    icon_label = tk.Label(btn_frame, text=icon, fg='white', bg=color, 
                                        font=('Arial', 40))
                    icon_label.pack(pady=(20, 10))
                    
                    # Button text
                    text_label = tk.Label(btn_frame, text=btn_text, fg='white', bg=color, 
                                        font=('Arial', 12, 'bold'), wraplength=150)
                    text_label.pack(pady=(0, 20))
                    
                    # Make frame clickable
                    for widget in [btn_frame, icon_label, text_label]:
                        widget.bind("<Button-1>", lambda e, cmd=command: cmd())
                        widget.bind("<Enter>", lambda e, frame=btn_frame: self.on_hover_enter(frame))
                        widget.bind("<Leave>", lambda e, frame=btn_frame, c=color: self.on_hover_leave(frame, c))
    
    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg='#16213e', height=50)
        footer_frame.pack(fill='x', side='bottom', padx=10, pady=(5, 10))
        footer_frame.pack_propagate(False)
        
        # Footer text
        footer_text = "Leadership is the ability to facilitate movement in the needed direction and have people feel good about it"
        footer_label = tk.Label(footer_frame, text=footer_text, fg='#ff6b6b', bg='#16213e', 
                              font=('Arial', 12, 'italic'))
        footer_label.pack(expand=True)
        
        # Settings button
        settings_btn = tk.Button(footer_frame, text="⚙️ Settings", fg='white', bg='#4a4a8a',
                               font=('Arial', 10), command=self.settings)
        settings_btn.pack(side='right', padx=10, pady=10)
    
    def on_hover_enter(self, frame):
        frame.configure(bg='#6a6aaa')
        for child in frame.winfo_children():
            child.configure(bg='#6a6aaa')
    
    def on_hover_leave(self, frame, original_color):
        frame.configure(bg=original_color)
        for child in frame.winfo_children():
            child.configure(bg=original_color)
    
    def update_time(self):
        current_time = datetime.now().strftime("%I:%M:%S %p")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    # Button command functions
    def student_details(self):
        """Open Student Management System"""
        try:
            from student_management import StudentManagementUI
            StudentManagementUI(self.root)
        except ImportError:
            tk.messagebox.showerror("Error", 
                "Student management module not found!\nPlease ensure student_management.py is in the same directory.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to open Student Management: {str(e)}")
    
    def face_recognition(self):
        """Open Face Recognition Module"""
        try:
            from face_recognition_module import FaceRecognitionModule
            FaceRecognitionModule(self.root)
        except ImportError:
            tk.messagebox.showerror("Error", 
                "Face recognition module not found!\nPlease ensure face_recognition_module.py is in the same directory.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to open Face Recognition: {str(e)}")
    
    def attendance(self):
        """View Attendance Records"""
        from attendance_viewer import AttendanceViewer
        try:
            AttendanceViewer(self.root)
        except ImportError:
            self.show_message("Attendance", 
                "Attendance viewer module is being developed.\n\nYou can find attendance records in the 'attendance' folder.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to open Attendance: {str(e)}")
    
    def help_desk(self):
        """Show Help Information"""
        help_text = """
        FACE RECOGNITION ATTENDANCE SYSTEM - HELP
        
        📋 WORKFLOW:
        1. Student Details → Add student information
        2. Photos → Capture 100+ photo samples
        3. Train Data → Train the AI model
        4. Face Recognition → Start attendance marking
        
        🎯 FEATURES:
        • Automatic face detection and recognition
        • Real-time attendance marking
        • CSV export functionality
        • Student management system
        
        📁 FILE LOCATIONS:
        • Student Data: student_data/students.csv
        • Photo Samples: data/ folder
        • Trained Model: trainer/trainer.yml
        • Attendance: attendance/ folder
        
        ⚙️ REQUIREMENTS:
        • Python 3.7+
        • OpenCV (cv2)
        • PIL (Pillow)
        • Working webcam
        
        💡 TIPS:
        • Capture photos in good lighting
        • Train with at least 100 samples per student
        • Adjust confidence threshold for better accuracy
        
        📧 SUPPORT:
        For technical support, contact SMIT Students
        """
        self.show_message("Help Desk", help_text)
    
    def train_data(self):
        """Open Train Data Module"""
        try:
            from train_data_module import TrainDataModule
            TrainDataModule(self.root)
        except ImportError:
            tk.messagebox.showerror("Error", 
                "Train data module not found!\nPlease ensure train_data_module.py is in the same directory.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to open Train Data: {str(e)}")
    
    def photos(self):
        """Open Photo Gallery/Capture"""
        photo_text = """
        PHOTO MANAGEMENT
        
        To capture photo samples:
        1. Go to 'Student Details'
        2. Enter student information
        3. Click 'ADD PHOTO SAMPLE'
        
        Or use the standalone photo capture:
        • Captures 100+ photos automatically
        • Detects faces in real-time
        • Saves to 'data' folder
        
        Note: Photo samples are required before training the model.
        """
        
        response = tk.messagebox.askyesnocancel("Photo Management", 
            photo_text + "\n\nDo you want to:\nYes = Open Photo Capture\nNo = View Data Folder\nCancel = Close")
        
        if response is True:  # Yes
            try:
                from photo_capture_module import PhotoCaptureModule
                # Open with sample student ID - user should use Student Details normally
                result = tk.messagebox.askquestion("Student Info", 
                    "This will open photo capture with test student.\n\nFor real students, use 'Student Details' → 'Add Photo Sample'\n\nContinue with test?")
                
                if result == 'yes':
                    PhotoCaptureModule(self.root, student_id=999, student_name="Test Student")
            except ImportError:
                tk.messagebox.showerror("Error", 
                    "Photo capture module not found!\nPlease ensure photo_capture_module.py is in the same directory.")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to open Photo Capture: {str(e)}")
        elif response is False:  # No
            import os
            data_path = os.path.abspath("data")
            if os.path.exists(data_path):
                os.startfile(data_path)  # Windows
            else:
                tk.messagebox.showinfo("Info", f"Data folder will be created at:\n{data_path}")
    
    def developer(self):
        """Show Developer Information"""
        dev_text = """
        🎓 FACE RECOGNITION ATTENDANCE SYSTEM
        
        👨‍💻 Developed By: SMIT Students
        
        📚 Project Details:
        • Academic Project
        • Face Recognition using OpenCV
        • LBPH Algorithm Implementation
        • Real-time Attendance Marking
        
        🛠️ Technologies Used:
        • Python 3.x
        • Tkinter (GUI)
        • OpenCV (Face Recognition)
        • PIL/Pillow (Image Processing)
        • CSV (Data Storage)
        
        📊 Features:
        ✓ Student Management System
        ✓ Photo Sample Collection
        ✓ AI Model Training
        ✓ Real-time Face Recognition
        ✓ Automatic Attendance Marking
        ✓ Data Export Functionality
        
        🎯 Version: 1.0.0
        📅 Year: 2024-2025
        
        © SMIT - All Rights Reserved
        """
        self.show_message("Developer Information", dev_text)
    
    def settings(self):
        """Open Settings Window"""
        settings_text = """
        ⚙️ SYSTEM SETTINGS
        
        Current Configuration:
        • Camera Index: 0 (Default)
        • Confidence Threshold: 50%
        • Max Photo Samples: 100
        • Recognition Algorithm: LBPH
        
        To modify settings:
        1. Face Recognition Module
           - Adjust confidence threshold
           - Change camera settings
        
        2. Photo Capture Module
           - Set sample count (50-200)
           - Camera selection
        
        3. Train Data Module
           - View training statistics
           - Model information
        
        Note: Advanced settings can be modified in the respective module source code.
        """
        self.show_message("Settings", settings_text)
    
    def exit_app(self):
        """Exit the application"""
        if tk.messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()
    
    def show_message(self, title, message):
        """Create a custom message dialog"""
        msg_window = tk.Toplevel(self.root)
        msg_window.title(title)
        msg_window.geometry("600x500")
        msg_window.configure(bg='#16213e')
        msg_window.grab_set()
        
        # Center the window
        msg_window.transient(self.root)
        
        # Title
        title_label = tk.Label(msg_window, text=title, fg='#00ffff', bg='#16213e', 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Message text with scrollbar
        text_frame = tk.Frame(msg_window, bg='#16213e')
        text_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        text_widget = tk.Text(text_frame, wrap='word', bg='#2c3e50', fg='white', 
                             font=('Arial', 11), relief='flat', padx=10, pady=10)
        text_widget.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
        scrollbar.pack(side='right', fill='y')
        text_widget.config(yscrollcommand=scrollbar.set)
        
        # Insert message
        text_widget.insert('1.0', message)
        text_widget.config(state='disabled')
        
        # OK button
        ok_btn = tk.Button(msg_window, text="OK", command=msg_window.destroy, 
                          bg='#4a4a8a', fg='white', font=('Arial', 12, 'bold'),
                          width=15, height=2)
        ok_btn.pack(pady=20)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FaceRecognitionUI()
    app.run()