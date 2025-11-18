# import tkinter as tk
# from tkinter import ttk
# import time
# from datetime import datetime
# import tkinter.messagebox

# class FaceRecognitionUI:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("Face Recognition Attendance System Software")
#         self.root.geometry("1280x720")
#         self.root.configure(bg='#0a0a2e')
#         self.root.state('zoomed')  # Maximize window
        
#         # Create header
#         self.create_header()
        
#         # Create main content area
#         self.create_main_content()
        
#         # Create footer
#         self.create_footer()
        
#         # Start time update
#         self.update_time()
    
#     def create_header(self):
#         # Header frame with gradient-like effect
#         header_frame = tk.Frame(self.root, bg='#16213e', height=100)
#         header_frame.pack(fill='x', padx=10, pady=(10, 5))
#         header_frame.pack_propagate(False)
        
#         # Developer info
#         dev_label = tk.Label(header_frame, text="Developed By: SMIT Students", 
#                            fg='white', bg='#16213e', font=('Arial', 10))
#         dev_label.pack(anchor='nw', padx=10, pady=5)
        
#         # Logo and title area
#         title_frame = tk.Frame(header_frame, bg='#16213e')
#         title_frame.pack(expand=True, fill='both')
        
#         # Facial recognition logo text
#         logo_label = tk.Label(title_frame, text="🔍 FACIAL\nRECOGNITION\nSOFTWARE", 
#                             fg='#00ffff', bg='#16213e', font=('Arial', 12, 'bold'))
#         logo_label.pack(side='left', padx=20, pady=10)
        
#         # Face images placeholder (represented as colored rectangles)
#         faces_frame = tk.Frame(title_frame, bg='#16213e')
#         faces_frame.pack(side='left', padx=50)
        
#         for i, color in enumerate(['#ff6b6b', '#4ecdc4', '#45b7d1']):
#             face_frame = tk.Frame(faces_frame, bg=color, width=60, height=60)
#             face_frame.pack(side='left', padx=5)
#             face_frame.pack_propagate(False)
            
#             # Add face placeholder
#             face_label = tk.Label(face_frame, text="👤", fg='white', bg=color, font=('Arial', 20))
#             face_label.pack(expand=True)
        
#         # Time display
#         self.time_label = tk.Label(title_frame, text="", fg='#00ffff', bg='#16213e', 
#                                  font=('Arial', 14, 'bold'))
#         self.time_label.pack(side='right', padx=20)
    
#     def create_main_content(self):
#         # Main title
#         title_label = tk.Label(self.root, text="FACE RECOGNITION ATTENDANCE SYSTEM SOFTWARE", 
#                              fg='#ff4444', bg='#0a0a2e', font=('Arial', 28, 'bold'))
#         title_label.pack(pady=20)
        
#         # Main buttons grid
#         main_frame = tk.Frame(self.root, bg='#0a0a2e')
#         main_frame.pack(expand=True, fill='both', padx=50, pady=20)
        
#         # Create 2x4 grid of buttons
#         buttons_data = [
#             ("STUDENT DETAILS", "👥", self.student_details, '#4a4a8a'),
#             ("FACE RECOGNITION", "🔍", self.face_recognition, '#4a4a8a'),
#             ("ATTENDANCE", "📊", self.attendance, '#4a4a8a'),
#             ("HELP DESK", "❓", self.help_desk, '#4a4a8a'),
#             ("TRAIN DATA", "🧠", self.train_data, '#4a4a8a'),
#             ("PHOTOS", "📸", self.photos, '#4a4a8a'),
#             ("DEVELOPER", "💻", self.developer, '#4a4a8a'),
#             ("EXIT", "🚪", self.exit_app, '#8a4a4a')
#         ]
        
#         # Create grid layout
#         for i in range(2):  # 2 rows
#             for j in range(4):  # 4 columns
#                 index = i * 4 + j
#                 if index < len(buttons_data):
#                     btn_text, icon, command, color = buttons_data[index]
                    
#                     # Create button frame
#                     btn_frame = tk.Frame(main_frame, bg=color, relief='raised', bd=2)
#                     btn_frame.grid(row=i, column=j, padx=15, pady=15, sticky='nsew')
                    
#                     # Configure grid weights for responsiveness
#                     main_frame.grid_rowconfigure(i, weight=1)
#                     main_frame.grid_columnconfigure(j, weight=1)
                    
#                     # Icon
#                     icon_label = tk.Label(btn_frame, text=icon, fg='white', bg=color, 
#                                         font=('Arial', 40))
#                     icon_label.pack(pady=(20, 10))
                    
#                     # Button text
#                     text_label = tk.Label(btn_frame, text=btn_text, fg='white', bg=color, 
#                                         font=('Arial', 12, 'bold'), wraplength=150)
#                     text_label.pack(pady=(0, 20))
                    
#                     # Make frame clickable
#                     for widget in [btn_frame, icon_label, text_label]:
#                         widget.bind("<Button-1>", lambda e, cmd=command: cmd())
#                         widget.bind("<Enter>", lambda e, frame=btn_frame: self.on_hover_enter(frame))
#                         widget.bind("<Leave>", lambda e, frame=btn_frame, c=color: self.on_hover_leave(frame, c))
    
#     def create_footer(self):
#         footer_frame = tk.Frame(self.root, bg='#16213e', height=50)
#         footer_frame.pack(fill='x', side='bottom', padx=10, pady=(5, 10))
#         footer_frame.pack_propagate(False)
        
#         # Footer text
#         footer_text = "Leadership is the ability to facilitate movement in the needed direction and have people feel good about it"
#         footer_label = tk.Label(footer_frame, text=footer_text, fg='#ff6b6b', bg='#16213e', 
#                               font=('Arial', 12, 'italic'))
#         footer_label.pack(expand=True)
        
#         # Settings button
#         settings_btn = tk.Button(footer_frame, text="⚙️ Settings", fg='white', bg='#4a4a8a',
#                                font=('Arial', 10), command=self.settings)
#         settings_btn.pack(side='right', padx=10, pady=10)
    
#     def on_hover_enter(self, frame):
#         frame.configure(bg='#6a6aaa')
#         for child in frame.winfo_children():
#             child.configure(bg='#6a6aaa')
    
#     def on_hover_leave(self, frame, original_color):
#         frame.configure(bg=original_color)
#         for child in frame.winfo_children():
#             child.configure(bg=original_color)
    
#     def update_time(self):
#         current_time = datetime.now().strftime("%I:%M:%S %p")
#         self.time_label.config(text=current_time)
#         self.root.after(1000, self.update_time)
    
#     # Button command functions
#     def student_details(self):
#         """Open Student Management System"""
#         try:
#             from student_management import StudentManagementUI
#             StudentManagementUI(self.root)
#         except ImportError:
#             tk.messagebox.showerror("Error", 
#                 "Student management module not found!\nPlease ensure student_management.py is in the same directory.")
#         except Exception as e:
#             tk.messagebox.showerror("Error", f"Failed to open Student Management: {str(e)}")
    
#     def face_recognition(self):
#         """Open Face Recognition Module"""
#         try:
#             from face_recognition_module import FaceRecognitionModule
#             FaceRecognitionModule(self.root)
#         except ImportError:
#             tk.messagebox.showerror("Error", 
#                 "Face recognition module not found!\nPlease ensure face_recognition_module.py is in the same directory.")
#         except Exception as e:
#             tk.messagebox.showerror("Error", f"Failed to open Face Recognition: {str(e)}")
    
#     def attendance(self):
#         """View Attendance Records"""
#         from attendance_viewer import AttendanceViewer
#         try:
#             AttendanceViewer(self.root)
#         except ImportError:
#             self.show_message("Attendance", 
#                 "Attendance viewer module is being developed.\n\nYou can find attendance records in the 'attendance' folder.")
#         except Exception as e:
#             tk.messagebox.showerror("Error", f"Failed to open Attendance: {str(e)}")
    
#     def help_desk(self):
#         """Show Help Information"""
#         help_text = """
#         FACE RECOGNITION ATTENDANCE SYSTEM - HELP
        
#         📋 WORKFLOW:
#         1. Student Details → Add student information
#         2. Photos → Capture 100+ photo samples
#         3. Train Data → Train the AI model
#         4. Face Recognition → Start attendance marking
        
#         🎯 FEATURES:
#         • Automatic face detection and recognition
#         • Real-time attendance marking
#         • CSV export functionality
#         • Student management system
        
#         📁 FILE LOCATIONS:
#         • Student Data: student_data/students.csv
#         • Photo Samples: data/ folder
#         • Trained Model: trainer/trainer.yml
#         • Attendance: attendance/ folder
        
#         ⚙️ REQUIREMENTS:
#         • Python 3.7+
#         • OpenCV (cv2)
#         • PIL (Pillow)
#         • Working webcam
        
#         💡 TIPS:
#         • Capture photos in good lighting
#         • Train with at least 100 samples per student
#         • Adjust confidence threshold for better accuracy
        
#         📧 SUPPORT:
#         For technical support, contact SMIT Students
#         """
#         self.show_message("Help Desk", help_text)
    
#     def train_data(self):
#         """Open Train Data Module"""
#         try:
#             from train_data_module import TrainDataModule
#             TrainDataModule(self.root)
#         except ImportError:
#             tk.messagebox.showerror("Error", 
#                 "Train data module not found!\nPlease ensure train_data_module.py is in the same directory.")
#         except Exception as e:
#             tk.messagebox.showerror("Error", f"Failed to open Train Data: {str(e)}")
    
#     def photos(self):
#         """Open Photo Gallery/Capture"""
#         photo_text = """
#         PHOTO MANAGEMENT
        
#         To capture photo samples:
#         1. Go to 'Student Details'
#         2. Enter student information
#         3. Click 'ADD PHOTO SAMPLE'
        
#         Or use the standalone photo capture:
#         • Captures 100+ photos automatically
#         • Detects faces in real-time
#         • Saves to 'data' folder
        
#         Note: Photo samples are required before training the model.
#         """
        
#         response = tk.messagebox.askyesnocancel("Photo Management", 
#             photo_text + "\n\nDo you want to:\nYes = Open Photo Capture\nNo = View Data Folder\nCancel = Close")
        
#         if response is True:  # Yes
#             try:
#                 from photo_capture_module import PhotoCaptureModule
#                 # Open with sample student ID - user should use Student Details normally
#                 result = tk.messagebox.askquestion("Student Info", 
#                     "This will open photo capture with test student.\n\nFor real students, use 'Student Details' → 'Add Photo Sample'\n\nContinue with test?")
                
#                 if result == 'yes':
#                     PhotoCaptureModule(self.root, student_id=999, student_name="Test Student")
#             except ImportError:
#                 tk.messagebox.showerror("Error", 
#                     "Photo capture module not found!\nPlease ensure photo_capture_module.py is in the same directory.")
#             except Exception as e:
#                 tk.messagebox.showerror("Error", f"Failed to open Photo Capture: {str(e)}")
#         elif response is False:  # No
#             import os
#             data_path = os.path.abspath("data")
#             if os.path.exists(data_path):
#                 os.startfile(data_path)  # Windows
#             else:
#                 tk.messagebox.showinfo("Info", f"Data folder will be created at:\n{data_path}")
    
#     def developer(self):
#         """Show Developer Information"""
#         dev_text = """
#         🎓 FACE RECOGNITION ATTENDANCE SYSTEM
        
#         👨‍💻 Developed By: SMIT Students
        
#         📚 Project Details:
#         • Academic Project
#         • Face Recognition using OpenCV
#         • LBPH Algorithm Implementation
#         • Real-time Attendance Marking
        
#         🛠️ Technologies Used:
#         • Python 3.x
#         • Tkinter (GUI)
#         • OpenCV (Face Recognition)
#         • PIL/Pillow (Image Processing)
#         • CSV (Data Storage)
        
#         📊 Features:
#         ✓ Student Management System
#         ✓ Photo Sample Collection
#         ✓ AI Model Training
#         ✓ Real-time Face Recognition
#         ✓ Automatic Attendance Marking
#         ✓ Data Export Functionality
        
#         🎯 Version: 1.0.0
#         📅 Year: 2024-2025
        
#         © SMIT - All Rights Reserved
#         """
#         self.show_message("Developer Information", dev_text)
    
#     def settings(self):
#         """Open Settings Window"""
#         settings_text = """
#         ⚙️ SYSTEM SETTINGS
        
#         Current Configuration:
#         • Camera Index: 0 (Default)
#         • Confidence Threshold: 50%
#         • Max Photo Samples: 100
#         • Recognition Algorithm: LBPH
        
#         To modify settings:
#         1. Face Recognition Module
#            - Adjust confidence threshold
#            - Change camera settings
        
#         2. Photo Capture Module
#            - Set sample count (50-200)
#            - Camera selection
        
#         3. Train Data Module
#            - View training statistics
#            - Model information
        
#         Note: Advanced settings can be modified in the respective module source code.
#         """
#         self.show_message("Settings", settings_text)
    
#     def exit_app(self):
#         """Exit the application"""
#         if tk.messagebox.askyesno("Exit", "Are you sure you want to exit?"):
#             self.root.quit()
    
#     def show_message(self, title, message):
#         """Create a custom message dialog"""
#         msg_window = tk.Toplevel(self.root)
#         msg_window.title(title)
#         msg_window.geometry("600x500")
#         msg_window.configure(bg='#16213e')
#         msg_window.grab_set()
        
#         # Center the window
#         msg_window.transient(self.root)
        
#         # Title
#         title_label = tk.Label(msg_window, text=title, fg='#00ffff', bg='#16213e', 
#                               font=('Arial', 16, 'bold'))
#         title_label.pack(pady=20)
        
#         # Message text with scrollbar
#         text_frame = tk.Frame(msg_window, bg='#16213e')
#         text_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
#         text_widget = tk.Text(text_frame, wrap='word', bg='#2c3e50', fg='white', 
#                              font=('Arial', 11), relief='flat', padx=10, pady=10)
#         text_widget.pack(side='left', fill='both', expand=True)
        
#         scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
#         scrollbar.pack(side='right', fill='y')
#         text_widget.config(yscrollcommand=scrollbar.set)
        
#         # Insert message
#         text_widget.insert('1.0', message)
#         text_widget.config(state='disabled')
        
#         # OK button
#         ok_btn = tk.Button(msg_window, text="OK", command=msg_window.destroy, 
#                           bg='#4a4a8a', fg='white', font=('Arial', 12, 'bold'),
#                           width=15, height=2)
#         ok_btn.pack(pady=20)
    
#     def run(self):
#         self.root.mainloop()

# if __name__ == "__main__":
#     app = FaceRecognitionUI()
#     app.run()
"""
face_recognition_ui.py - COMPLETE REWRITE
Professional Face Recognition Attendance System UI with Real-Time Statistics
SMIT Face Recognition System - 2025
"""

import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

try:
    import customtkinter as ctk
except ImportError:
    raise ImportError("customtkinter is required. Install with: pip install customtkinter")

from PIL import Image, ImageTk
import cv2

# Import statistics module
from statistics_module import RealTimeStatistics

# Optional pygame for sound
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

# Configuration
VIDEO_PATH = "WhatsApp Video 2025-11-17 at 23.41.36_2c9c66ab.mp4"  # Optional
MUSIC_PATH = None  # Optional background music path

class FaceRecognitionUI:
    def __init__(self, root=None):
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = root or ctk.CTk()
        self.root.title("SMIT Face Recognition Attendance System")
        self.root.geometry("1280x780")
        
        try:
            self.root.state("zoomed")
        except:
            pass

        # Initialize statistics module
        self.stats_module = RealTimeStatistics()

        # Optional video capture for background
        self.cap = None
        self.video_enabled = False
        if os.path.exists(VIDEO_PATH):
            try:
                self.cap = cv2.VideoCapture(VIDEO_PATH)
                self.video_enabled = True
            except:
                pass

        # Optional music
        self.music_playing = False
        self.muted = False
        if PYGAME_AVAILABLE and MUSIC_PATH and os.path.exists(MUSIC_PATH):
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(MUSIC_PATH)
                pygame.mixer.music.set_volume(0.25)
            except:
                pass

        self.running = True
        
        # Build UI
        self.build_ui()
        
        # Start updates
        if self.video_enabled:
            self.update_video()
        self.update_clock()
        
        # Start statistics auto-update
        self.root.after(2000, self.schedule_stats_update)
        
        # Start music if available
        if PYGAME_AVAILABLE and MUSIC_PATH and os.path.exists(MUSIC_PATH):
            try:
                pygame.mixer.music.play(-1)
                self.music_playing = True
            except:
                pass

    def build_ui(self):
        """Build the main UI structure"""
        
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#0a0a2e")
        self.main_frame.pack(fill="both", expand=True)
        
        # If video is enabled, create canvas for background
        if self.video_enabled:
            self.video_canvas = tk.Canvas(self.main_frame, bg="#0a0a2e", 
                                         highlightthickness=0)
            self.video_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Content frame (on top of video if enabled)
        self.content_frame = ctk.CTkFrame(self.main_frame, 
                                         fg_color=("gray10", "gray10"))
        self.content_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        
        # Build sections
        self.build_header()
        self.build_stats_cards()
        self.build_function_grid()
        self.build_footer()
        
    def build_header(self):
        """Build header with title and controls"""
        header = ctk.CTkFrame(self.content_frame, fg_color=("gray15", "gray15"), 
                             height=80)
        header.pack(fill="x", padx=10, pady=10)
        header.pack_propagate(False)
        
        # Title
        title = ctk.CTkLabel(header, 
                            text="🎓 SMIT FACE RECOGNITION ATTENDANCE SYSTEM",
                            font=ctk.CTkFont(size=22, weight="bold"),
                            text_color="#00d9ff")
        title.pack(side="left", padx=20, pady=10)
        
        # Subtitle
        subtitle = ctk.CTkLabel(header, 
                               text="Smart Attendance • Powered by AI",
                               font=ctk.CTkFont(size=11),
                               text_color="gray70")
        subtitle.place(relx=0.02, rely=0.6)
        
        # Clock
        self.clock_label = ctk.CTkLabel(header, text="", 
                                       font=ctk.CTkFont(size=13, weight="bold"),
                                       text_color="#00d9ff")
        self.clock_label.place(relx=0.68, rely=0.25)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(header, text="🔄", width=70,
                                    command=self.refresh_statistics_manual,
                                    fg_color="#2ecc71",
                                    hover_color="#27ae60")
        refresh_btn.place(relx=0.88, rely=0.3)
        
        # Music controls (if available)
        if PYGAME_AVAILABLE and MUSIC_PATH:
            self.music_btn = ctk.CTkButton(header, text="🎵", width=70,
                                          command=self.toggle_music)
            self.music_btn.place(relx=0.94, rely=0.3)

    def build_stats_cards(self):
        """Build statistics cards with REAL data"""
        stats_container = ctk.CTkFrame(self.content_frame, 
                                      fg_color=("gray12", "gray12"))
        stats_container.pack(fill="x", padx=10, pady=(0, 10))
        
        # Configure grid
        for i in range(4):
            stats_container.columnconfigure(i, weight=1, uniform="stat")
        
        # Get REAL statistics
        real_stats = self.get_real_statistics()
        
        # Stats data with real values
        stats = [
            ("📚 Total Students", real_stats['total_students'], "#3498db"),
            ("✅ Present Today", real_stats['present_today'], "#2ecc71"),
            ("📸 Photos Collected", real_stats['photos_collected'], "#9b59b6"),
            ("🧠 Models Trained", real_stats['models_trained'], "#f39c12")
        ]
        
        # Store label references for updates
        self.stat_labels = []
        self.stat_values = {}
        
        for i, (label, value, color) in enumerate(stats):
            card = ctk.CTkFrame(stats_container, fg_color=("gray14", "gray14"),
                               corner_radius=10)
            card.grid(row=0, column=i, padx=8, pady=12, sticky="nsew")
            
            # Icon/Title
            title_label = ctk.CTkLabel(card, text=label,
                                      font=ctk.CTkFont(size=12, weight="bold"),
                                      text_color="gray80")
            title_label.pack(pady=(15, 5))
            
            # Value
            value_label = ctk.CTkLabel(card, text=str(value),
                                      font=ctk.CTkFont(size=28, weight="bold"),
                                      text_color=color)
            value_label.pack(pady=(0, 15))
            
            # Store reference for updates
            self.stat_labels.append(value_label)
            self.stat_values[label] = value

    def build_function_grid(self):
        """Build main function buttons grid"""
        grid_container = ctk.CTkFrame(self.content_frame, 
                                     fg_color=("gray12", "gray12"))
        grid_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Configure grid - 4 columns x 2 rows
        for i in range(4):
            grid_container.columnconfigure(i, weight=1, uniform="btn")
        for i in range(2):
            grid_container.rowconfigure(i, weight=1, uniform="btn")
        
        # Button data
        buttons = [
            ("STUDENT DETAILS", "👥", self.student_details, "#3498db"),
            ("FACE RECOGNITION", "🔍", self.face_recognition, "#2ecc71"),
            ("ATTENDANCE", "📊", self.attendance, "#9b59b6"),
            ("HELP DESK", "❓", self.help_desk, "#e67e22"),
            ("TRAIN DATA", "🧠", self.train_data, "#e74c3c"),
            ("PHOTOS", "📸", self.photos, "#1abc9c"),
            ("DEVELOPER", "💻", self.developer, "#34495e"),
            ("EXIT", "🚪", self.exit_app, "#c0392b")
        ]
        
        for idx, (text, icon, command, color) in enumerate(buttons):
            row = idx // 4
            col = idx % 4
            
            # Card frame
            card = ctk.CTkFrame(grid_container, fg_color=("gray14", "gray14"),
                               corner_radius=12)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Icon
            icon_label = ctk.CTkLabel(card, text=icon, 
                                     font=ctk.CTkFont(size=36))
            icon_label.pack(pady=(20, 5))
            
            # Text
            text_label = ctk.CTkLabel(card, text=text,
                                     font=ctk.CTkFont(size=13, weight="bold"),
                                     text_color="gray90")
            text_label.pack(pady=(0, 10))
            
            # Button
            btn = ctk.CTkButton(card, text="Open", 
                               command=command,
                               fg_color=color,
                               hover_color=self.darken_color(color),
                               corner_radius=8,
                               height=35,
                               font=ctk.CTkFont(size=11, weight="bold"))
            btn.pack(pady=(0, 20), padx=20, fill="x")

    def build_footer(self):
        """Build footer"""
        footer = ctk.CTkFrame(self.content_frame, fg_color=("gray15", "gray15"),
                             height=60)
        footer.pack(fill="x", side="bottom", padx=10, pady=10)
        footer.pack_propagate(False)
        
        # Footer text
        quote = ("Leadership is the ability to facilitate movement in the "
                "needed direction and have people feel good about it")
        footer_label = ctk.CTkLabel(footer, text=quote,
                                   font=ctk.CTkFont(size=11, slant="italic"),
                                   text_color="#ff99aa")
        footer_label.pack(side="left", padx=20, pady=15)
        
        # Settings button
        settings_btn = ctk.CTkButton(footer, text="⚙️ Settings",
                                    width=120,
                                    command=self.settings)
        settings_btn.pack(side="right", padx=20, pady=15)

    def darken_color(self, hex_color):
        """Darken a hex color for hover effect"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r, g, b = int(r * 0.8), int(g * 0.8), int(b * 0.8)
        return f"#{r:02x}{g:02x}{b:02x}"

    def get_real_statistics(self):
        """
        Get real-time statistics from file system
        Returns: dict with all statistics
        """
        return self.stats_module.get_all_statistics()

    def update_statistics(self):
        """Update statistics display with current data"""
        if not hasattr(self, 'stat_labels') or not self.stat_labels:
            return
        
        try:
            # Get fresh statistics
            new_stats = self.get_real_statistics()
            
            # Stats configuration
            stats_config = [
                ("📚 Total Students", new_stats['total_students'], "#3498db"),
                ("✅ Present Today", new_stats['present_today'], "#2ecc71"),
                ("📸 Photos Collected", new_stats['photos_collected'], "#9b59b6"),
                ("🧠 Models Trained", new_stats['models_trained'], "#f39c12")
            ]
            
            # Update each stat card
            for i, (label, value, color) in enumerate(stats_config):
                if i < len(self.stat_labels):
                    # Get old value for comparison
                    old_value = self.stat_values.get(label, 0)
                    
                    # Update display
                    self.stat_labels[i].configure(text=str(value))
                    
                    # Flash effect if value changed
                    if old_value != value:
                        self.stat_values[label] = value
                        self.stat_labels[i].configure(text_color="white")
                        self.root.after(200, 
                                       lambda lbl=self.stat_labels[i], c=color: 
                                       lbl.configure(text_color=c))
        except Exception as e:
            print(f"Error updating statistics: {e}")

    def schedule_stats_update(self):
        """Schedule automatic statistics updates every 10 seconds"""
        if not self.running:
            return
        
        try:
            self.update_statistics()
        except:
            pass
        
        # Schedule next update (10 seconds)
        self.root.after(10000, self.schedule_stats_update)

    def refresh_statistics_manual(self):
        """Manual refresh triggered by button"""
        self.update_statistics()
        try:
            messagebox.showinfo("Statistics Refreshed", 
                               "All statistics have been updated with current data!")
        except:
            pass

    def update_clock(self):
        """Update clock display"""
        now = datetime.now().strftime("%I:%M:%S %p • %d %B %Y")
        try:
            self.clock_label.configure(text=now)
        except:
            pass
        if self.running:
            self.root.after(1000, self.update_clock)

    def update_video(self):
        """Update background video"""
        if not self.running or not self.cap:
            return
        
        ret, frame = self.cap.read()
        if not ret:
            try:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
            except:
                return
        
        if ret:
            try:
                w = self.root.winfo_width() or 1280
                h = self.root.winfo_height() or 780
                frame = cv2.resize(frame, (w, h))
                frame = cv2.GaussianBlur(frame, (21, 21), 0)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                img = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(img)
                
                self.video_canvas.delete("video")
                self.video_canvas.create_image(0, 0, anchor="nw", 
                                              image=photo, tags="video")
                self.video_canvas.image = photo
            except:
                pass
        
        if self.running:
            self.root.after(33, self.update_video)

    def toggle_music(self):
        """Toggle background music"""
        if not PYGAME_AVAILABLE or not MUSIC_PATH:
            messagebox.showinfo("Music", "Background music not available")
            return
        
        if not self.music_playing:
            try:
                pygame.mixer.music.play(-1)
                self.music_playing = True
                self.music_btn.configure(text="🔊")
            except:
                pass
        else:
            try:
                pygame.mixer.music.stop()
                self.music_playing = False
                self.music_btn.configure(text="🎵")
            except:
                pass

    # Module launchers
    def student_details(self):
        """Open Student Management"""
        try:
            from student_management import UpdatedStudentManagement
            UpdatedStudentManagement(self.root)
        except ImportError:
            messagebox.showerror("Error", 
                "Student management module not found!\n"
                "Ensure student_management.py is present.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open: {str(e)}")

    def face_recognition(self):
        """Open Face Recognition"""
        try:
            from face_recognition_module import FaceRecognitionModule
            FaceRecognitionModule(self.root)
        except ImportError:
            messagebox.showerror("Error",
                "Face recognition module not found!\n"
                "Ensure face_recognition_module.py is present.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open: {str(e)}")

    def attendance(self):
        """View Attendance"""
        try:
            from attendance_viewer import AttendanceViewer
            AttendanceViewer(self.root)
        except ImportError:
            messagebox.showinfo("Attendance",
                "Attendance viewer not found.\n"
                "Check the 'attendance' folder for CSV files.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open: {str(e)}")

    def help_desk(self):
        """Show Help"""
        help_text = """
FACE RECOGNITION ATTENDANCE SYSTEM - HELP

📋 WORKFLOW:
1. Student Details → Add student information
2. Photos → Capture 100+ photo samples  
3. Train Data → Train the AI model
4. Face Recognition → Start attendance marking

🎯 FEATURES:
• Automatic face detection and recognition
• Real-time attendance marking with liveness detection
• ID card verification support
• CSV export functionality
• Comprehensive student management

📁 FILE LOCATIONS:
• Student Data: student_data/students.csv
• Photo Samples: data/ folder
• Trained Model: trainer/trainer.yml
• Attendance: attendance/ folder

⚙️ REQUIREMENTS:
• Python 3.7+
• OpenCV with contrib modules
• Working webcam
• Good lighting conditions

💡 TIPS:
• Capture photos in good lighting
• Train with at least 100 samples per student
• Adjust confidence threshold for accuracy
• Enable liveness detection for security

📧 SUPPORT:
Developed by SMIT Students
For help, contact your system administrator.
        """
        
        help_win = ctk.CTkToplevel(self.root)
        help_win.title("Help Desk")
        help_win.geometry("700x600")
        help_win.transient(self.root)
        
        text = ctk.CTkTextbox(help_win, font=ctk.CTkFont(size=11))
        text.pack(fill="both", expand=True, padx=20, pady=20)
        text.insert("1.0", help_text)
        text.configure(state="disabled")
        
        close_btn = ctk.CTkButton(help_win, text="Close", 
                                  command=help_win.destroy)
        close_btn.pack(pady=(0, 20))

    def train_data(self):
        """Open Training Module"""
        try:
            from train_data_module import TrainDataModule
            TrainDataModule(self.root)
        except ImportError:
            messagebox.showerror("Error",
                "Train data module not found!\n"
                "Ensure train_data_module.py is present.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open: {str(e)}")

    def photos(self):
        """Photo Management"""
        msg = messagebox.askyesno("Photo Management",
            "To capture photos:\n\n"
            "1. Go to 'Student Details'\n"
            "2. Enter student information\n"
            "3. Click 'CAPTURE PHOTOS'\n\n"
            "Open photo capture with test student?")
        
        if msg:
            try:
                from photo_capture_module import PhotoCaptureModule
                PhotoCaptureModule(self.root, student_id=999, 
                                  student_name="Test Student")
            except ImportError:
                messagebox.showerror("Error",
                    "Photo capture module not found!\n"
                    "Ensure photo_capture_module.py is present.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open: {str(e)}")

    def developer(self):
        """Show Developer Info"""
        dev_text = """
🎓 FACE RECOGNITION ATTENDANCE SYSTEM

👨‍💻 Developed By: SMIT Students

📚 Project Details:
• Academic Project for Smart Attendance
• Face Recognition using OpenCV & LBPH
• Real-time Attendance Marking
• Liveness Detection for Security
• ID Card Verification Support

🛠️ Technologies:
• Python 3.x
• CustomTkinter (Modern UI)
• OpenCV (Face Recognition)
• PIL/Pillow (Image Processing)
• CSV (Data Storage)

📊 Features:
✓ Student Management System
✓ Photo Sample Collection
✓ AI Model Training
✓ Real-time Face Recognition
✓ Liveness Detection (Anti-Spoofing)
✓ ID Card Verification
✓ Automatic Attendance Marking
✓ Data Export Functionality
✓ Real-time Statistics Dashboard

🎯 Version: 2.0.0
📅 Year: 2024-2025

© SMIT - All Rights Reserved
        """
        
        dev_win = ctk.CTkToplevel(self.root)
        dev_win.title("Developer Information")
        dev_win.geometry("600x550")
        dev_win.transient(self.root)
        
        text = ctk.CTkTextbox(dev_win, font=ctk.CTkFont(size=11))
        text.pack(fill="both", expand=True, padx=20, pady=20)
        text.insert("1.0", dev_text)
        text.configure(state="disabled")
        
        close_btn = ctk.CTkButton(dev_win, text="Close",
                                  command=dev_win.destroy)
        close_btn.pack(pady=(0, 20))

    def settings(self):
        """Show Settings"""
        settings_text = """
⚙️ SYSTEM SETTINGS

Current Configuration:
• Camera Index: 0 (Default)
• Confidence Threshold: 50%
• Max Photo Samples: 100
• Recognition Algorithm: LBPH

Feature Status:
• Liveness Detection: Available
• ID Card Verification: Available  
• Video Background: """ + ("Enabled" if self.video_enabled else "Disabled") + """
• Background Music: """ + ("Available" if (PYGAME_AVAILABLE and MUSIC_PATH) else "Not Available") + """
• Real-time Statistics: Enabled (10s refresh)

To modify settings:
1. Face Recognition Module
   - Adjust confidence threshold
   - Toggle liveness detection
   - Toggle ID verification

2. Photo Capture Module
   - Set sample count (50-200)
   - Camera selection

3. Train Data Module
   - View training statistics
   - Model information

Note: Advanced settings can be modified in module code.
        """
        
        settings_win = ctk.CTkToplevel(self.root)
        settings_win.title("Settings")
        settings_win.geometry("550x450")
        settings_win.transient(self.root)
        
        text = ctk.CTkTextbox(settings_win, font=ctk.CTkFont(size=11))
        text.pack(fill="both", expand=True, padx=20, pady=20)
        text.insert("1.0", settings_text)
        text.configure(state="disabled")
        
        close_btn = ctk.CTkButton(settings_win, text="Close",
                                  command=settings_win.destroy)
        close_btn.pack(pady=(0, 20))

    def exit_app(self):
        """Exit application"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.destroy()

    def destroy(self):
        """Cleanup and exit"""
        self.running = False
        
        try:
            if self.cap:
                self.cap.release()
        except:
            pass
        
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.quit()
            except:
                pass
        
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass

    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = FaceRecognitionUI()
    app.run()