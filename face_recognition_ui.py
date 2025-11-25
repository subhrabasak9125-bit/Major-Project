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
try:
    from statistics_module import RealTimeStatistics
    STATS_AVAILABLE = True
except ImportError:
    STATS_AVAILABLE = False
    print("Warning: Statistics module not available")

# Import DISHA voice assistant (try ultra version first, fallback to regular)
try:
    from disha_voice_assistant import UltraDISHAIntegration as DISHAIntegration
    DISHA_AVAILABLE = True
    DISHA_VERSION = "ULTRA"
    print("Ultra DISHA loaded successfully!")
except ImportError:
    try:
        from disha_voice_assistant import DISHAIntegration
        DISHA_AVAILABLE = True
        DISHA_VERSION = "STANDARD"
        print("Standard DISHA loaded successfully!")
    except ImportError:
        DISHA_AVAILABLE = False
        DISHA_VERSION = None
        print("Warning: DISHA voice assistant not available")

# Optional pygame for sound
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

# Configuration
VIDEO_PATH = "WhatsApp Video 2025-11-17 at 23.41.36_2c9c66ab.mp4"
MUSIC_PATH = None


class FaceRecognitionUI:
    def __init__(self, root=None):
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = root or ctk.CTk()
        self.root.title("SMIT Face Recognition Attendance System")
        self.root.geometry("1400x900")
        
        try:
            self.root.state("zoomed")
        except:
            pass

        # Initialize statistics
        self.stats_module = RealTimeStatistics() if STATS_AVAILABLE else None

        # Initialize DISHA
        self.disha = None
        self.disha_active = False

        # Video background
        self.cap = None
        self.video_enabled = False
        if os.path.exists(VIDEO_PATH):
            try:
                self.cap = cv2.VideoCapture(VIDEO_PATH)
                self.video_enabled = True
            except:
                pass

        # Music
        self.music_playing = False
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
        
        if self.stats_module:
            self.root.after(2000, self.schedule_stats_update)
        
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
        
        # Video background canvas
        if self.video_enabled:
            self.video_canvas = tk.Canvas(self.main_frame, bg="#0a0a2e", 
                                         highlightthickness=0)
            self.video_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Content frame
        self.content_frame = ctk.CTkFrame(self.main_frame, 
                                         fg_color=("gray10", "gray10"))
        self.content_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        
        # Build sections
        self.build_header()
        self.build_stats_cards()
        self.build_function_grid()
        self.build_footer()
        
        # Add floating DISHA button
        self.add_floating_disha()
        
    def build_header(self):
        """Build header with title and controls"""
        header = ctk.CTkFrame(self.content_frame, fg_color=("gray15", "gray15"), 
                             height=100)
        header.pack(fill="x", padx=15, pady=15)
        header.pack_propagate(False)
        
        # Title section
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="both", expand=True, padx=20)
        
        # Title with DISHA version indicator
        disha_indicator = f" | DISHA {DISHA_VERSION}" if DISHA_VERSION else ""
        title = ctk.CTkLabel(title_frame, 
                            text=f"SMIT FACE RECOGNITION ATTENDANCE SYSTEM{disha_indicator}",
                            font=ctk.CTkFont(size=26, weight="bold"),
                            text_color="#00d9ff")
        title.pack(anchor="w", pady=(10, 0))
        
        subtitle_text = "Smart Attendance | AI-Powered"
        if DISHA_VERSION == "ULTRA":
            subtitle_text += " | DISHA Ultra Voice Assistant"
        elif DISHA_VERSION == "STANDARD":
            subtitle_text += " | DISHA Voice Assistant"
        
        subtitle = ctk.CTkLabel(title_frame, 
                               text=subtitle_text,
                               font=ctk.CTkFont(size=13),
                               text_color="gray70")
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # Controls frame
        controls_frame = ctk.CTkFrame(header, fg_color="transparent")
        controls_frame.pack(side="right", padx=20)
        
        # Clock
        self.clock_label = ctk.CTkLabel(controls_frame, text="", 
                                       font=ctk.CTkFont(size=16, weight="bold"),
                                       text_color="#00d9ff")
        self.clock_label.grid(row=0, column=0, columnspan=2, pady=(5, 10))
        
        # Refresh button
        refresh_btn = ctk.CTkButton(controls_frame, 
                                   text="Refresh", 
                                   width=140,
                                   height=50,
                                   command=self.refresh_statistics_manual,
                                   fg_color="#2ecc71",
                                   hover_color="#27ae60",
                                   font=ctk.CTkFont(size=16, weight="bold"),
                                   corner_radius=10)
        refresh_btn.grid(row=1, column=0, padx=5, pady=5)
        
        # Music button
        if PYGAME_AVAILABLE and MUSIC_PATH:
            self.music_btn = ctk.CTkButton(controls_frame, 
                                          text="Music", 
                                          width=140,
                                          height=50,
                                          command=self.toggle_music,
                                          font=ctk.CTkFont(size=16, weight="bold"),
                                          corner_radius=10)
            self.music_btn.grid(row=1, column=1, padx=5, pady=5)

    def add_floating_disha(self):
        """Add floating DISHA button in bottom-right corner"""
        if not DISHA_AVAILABLE:
            return
        
        # Floating button container
        float_container = ctk.CTkFrame(self.content_frame, 
                                       fg_color="transparent")
        float_container.place(relx=0.95, rely=0.88, anchor="center")
        
        # DISHA button text based on version
        disha_text = "DISHA\nULTRA" if DISHA_VERSION == "ULTRA" else "DISHA"
        
        # DISHA button with glow effect
        self.disha_float_btn = ctk.CTkButton(
            float_container,
            text=disha_text,
            width=90,
            height=90,
            corner_radius=45,
            fg_color=("#9b59b6", "#8e44ad"),
            hover_color="#7d3c98",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.toggle_disha,
            border_width=3,
            border_color="#bb87dd"
        )
        self.disha_float_btn.pack()
        
        # Status label
        status_text = "Click to activate" if DISHA_VERSION else "Not available"
        self.disha_status_label = ctk.CTkLabel(
            float_container,
            text=status_text,
            font=ctk.CTkFont(size=10),
            text_color="gray60"
        )
        self.disha_status_label.pack(pady=(5, 0))
        
        # Start pulsing animation
        self.pulse_disha()
    
    def pulse_disha(self):
        """Create pulsing animation for DISHA button"""
        if not hasattr(self, 'disha_float_btn'):
            return
        
        try:
            if self.disha_active:
                # Active: green pulse
                colors = ["#27ae60", "#2ecc71"]
            else:
                # Inactive: purple pulse
                colors = ["#9b59b6", "#8e44ad"]
            
            current = self.disha_float_btn.cget("fg_color")
            new_color = colors[1] if current == colors[0] else colors[0]
            self.disha_float_btn.configure(fg_color=new_color)
        except:
            pass
        
        if self.running:
            self.root.after(1000, self.pulse_disha)

    def build_stats_cards(self):
        """Build statistics cards"""
        stats_container = ctk.CTkFrame(self.content_frame, 
                                      fg_color=("gray12", "gray12"),
                                      height=140)
        stats_container.pack(fill="x", padx=15, pady=(0, 15))
        stats_container.pack_propagate(False)
        
        for i in range(4):
            stats_container.columnconfigure(i, weight=1, uniform="stat")
        
        # Get statistics
        if self.stats_module:
            real_stats = self.get_real_statistics()
        else:
            real_stats = {
                'total_students': 0,
                'present_today': 0,
                'photos_collected': 0,
                'models_trained': 0
            }
        
        stats = [
            ("Total Students", real_stats['total_students'], "#3498db"),
            ("Present Today", real_stats['present_today'], "#2ecc71"),
            ("Photos Collected", real_stats['photos_collected'], "#9b59b6"),
            ("Models Trained", real_stats['models_trained'], "#f39c12")
        ]
        
        self.stat_labels = []
        self.stat_values = {}
        
        for i, (label, value, color) in enumerate(stats):
            card = ctk.CTkFrame(stats_container, fg_color=("gray14", "gray14"),
                               corner_radius=15, border_width=3, border_color=color)
            card.grid(row=0, column=i, padx=10, pady=15, sticky="nsew")
            
            title_label = ctk.CTkLabel(card, text=label,
                                      font=ctk.CTkFont(size=15, weight="bold"),
                                      text_color="gray80")
            title_label.pack(pady=(20, 10))
            
            value_label = ctk.CTkLabel(card, text=str(value),
                                      font=ctk.CTkFont(size=36, weight="bold"),
                                      text_color=color)
            value_label.pack(pady=(0, 20))
            
            self.stat_labels.append(value_label)
            self.stat_values[label] = value

    def build_function_grid(self):
        """Build main function buttons grid"""
        grid_container = ctk.CTkFrame(self.content_frame, 
                                     fg_color=("gray12", "gray12"))
        grid_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        for i in range(4):
            grid_container.columnconfigure(i, weight=1, uniform="btn")
        for i in range(2):
            grid_container.rowconfigure(i, weight=1, uniform="btn")
        
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
            
            card = ctk.CTkFrame(grid_container, fg_color=("gray14", "gray14"),
                               corner_radius=15)
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
            
            icon_label = ctk.CTkLabel(card, text=icon, 
                                     font=ctk.CTkFont(size=48))
            icon_label.pack(pady=(25, 10))
            
            text_label = ctk.CTkLabel(card, text=text,
                                     font=ctk.CTkFont(size=16, weight="bold"),
                                     text_color="gray90")
            text_label.pack(pady=(0, 15))
            
            btn = ctk.CTkButton(card, text="Open", 
                               command=command,
                               fg_color=color,
                               hover_color=self.darken_color(color),
                               corner_radius=10,
                               height=45,
                               font=ctk.CTkFont(size=14, weight="bold"))
            btn.pack(pady=(0, 25), padx=25, fill="x")

    def build_footer(self):
        """Build footer"""
        footer = ctk.CTkFrame(self.content_frame, fg_color=("gray15", "gray15"),
                             height=70)
        footer.pack(fill="x", side="bottom", padx=15, pady=15)
        footer.pack_propagate(False)
        
        quote = ("Leadership is the ability to facilitate movement in the "
                "needed direction and have people feel good about it")
        footer_label = ctk.CTkLabel(footer, text=quote,
                                   font=ctk.CTkFont(size=13, slant="italic"),
                                   text_color="#ff99aa")
        footer_label.pack(side="left", padx=25, pady=20)
        
        settings_btn = ctk.CTkButton(footer, text="Settings",
                                    width=140,
                                    height=45,
                                    font=ctk.CTkFont(size=14, weight="bold"),
                                    command=self.settings)
        settings_btn.pack(side="right", padx=25, pady=15)

    def toggle_disha(self):
        """Toggle DISHA voice assistant"""
        if not DISHA_AVAILABLE:
            messagebox.showerror("DISHA Not Available",
                "DISHA voice assistant is not available!\n\n"
                "Required packages:\n"
                "- pip install pyttsx3\n"
                "- pip install SpeechRecognition\n"
                "- pip install pyaudio")
            return
        
        if not self.disha_active:
            try:
                # Start DISHA with female voice (auto-detect or use index 1 for Windows Zira)
                self.disha = DISHAIntegration(self.root, preferred_voice_index=1)  # Force female voice
                self.disha.start()
                self.disha_active = True
                
                # Update UI
                self.disha_float_btn.configure(
                    fg_color="#27ae60",
                    border_color="#58d68d"
                )
                self.disha_status_label.configure(
                    text="ACTIVE",
                    text_color="#2ecc71"
                )
                
                disha_info = "DISHA is now listening!\n\nWake word: 'Hey DISHA'\n\n"
                if DISHA_VERSION == "ULTRA":
                    disha_info += "ULTRA VERSION - Natural language supported!\n\n"
                    disha_info += "Try saying naturally:\n"
                    disha_info += "- 'Hey DISHA, how many students do we have?'\n"
                    disha_info += "- 'DISHA, who's absent today?'\n"
                    disha_info += "- 'Yo DISHA, what's the attendance trend?'\n"
                    disha_info += "- 'Hey DISHA, open student management'\n"
                    disha_info += "- 'DISHA, how's the system doing?'"
                else:
                    disha_info += "Try saying:\n"
                    disha_info += "- 'Hey DISHA, how many students?'\n"
                    disha_info += "- 'Hey DISHA, open student management'\n"
                    disha_info += "- 'Hey DISHA, system status'\n"
                    disha_info += "- 'Hey DISHA, help'"
                
                messagebox.showinfo("DISHA Active", disha_info)
                    
            except Exception as e:
                messagebox.showerror("DISHA Error", 
                                   f"Failed to start DISHA:\n{str(e)}")
                self.disha_active = False
        else:
            try:
                # Stop DISHA
                if self.disha:
                    self.disha.stop()
                    self.disha = None
                self.disha_active = False
                
                # Update UI
                self.disha_float_btn.configure(
                    fg_color="#9b59b6",
                    border_color="#bb87dd"
                )
                self.disha_status_label.configure(
                    text="Click to activate",
                    text_color="gray60"
                )
                
                messagebox.showinfo("DISHA", "DISHA has been deactivated")
            except Exception as e:
                messagebox.showerror("DISHA Error", 
                                   f"Failed to stop DISHA:\n{str(e)}")

    def darken_color(self, hex_color):
        """Darken a hex color for hover effect"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r, g, b = int(r * 0.8), int(g * 0.8), int(b * 0.8)
        return f"#{r:02x}{g:02x}{b:02x}"

    def get_real_statistics(self):
        """Get real-time statistics"""
        if self.stats_module:
            return self.stats_module.get_all_statistics()
        return {
            'total_students': 0,
            'present_today': 0,
            'photos_collected': 0,
            'models_trained': 0
        }

    def update_statistics(self):
        """Update statistics display"""
        if not hasattr(self, 'stat_labels') or not self.stat_labels:
            return
        
        try:
            new_stats = self.get_real_statistics()
            
            stats_config = [
                ("Total Students", new_stats['total_students'], "#3498db"),
                ("Present Today", new_stats['present_today'], "#2ecc71"),
                ("Photos Collected", new_stats['photos_collected'], "#9b59b6"),
                ("Models Trained", new_stats['models_trained'], "#f39c12")
            ]
            
            for i, (label, value, color) in enumerate(stats_config):
                if i < len(self.stat_labels):
                    old_value = self.stat_values.get(label, 0)
                    self.stat_labels[i].configure(text=str(value))
                    
                    if old_value != value:
                        self.stat_values[label] = value
                        self.stat_labels[i].configure(text_color="white")
                        self.root.after(200, 
                                       lambda lbl=self.stat_labels[i], c=color: 
                                       lbl.configure(text_color=c))
        except Exception as e:
            print(f"Error updating statistics: {e}")

    def schedule_stats_update(self):
        """Schedule automatic statistics updates"""
        if not self.running:
            return
        
        try:
            self.update_statistics()
        except:
            pass
        
        self.root.after(10000, self.schedule_stats_update)

    def refresh_statistics_manual(self):
        """Manual refresh"""
        self.update_statistics()
        try:
            messagebox.showinfo("Statistics Refreshed", 
                               "All statistics have been updated!")
        except:
            pass

    def update_clock(self):
        """Update clock display"""
        now = datetime.now().strftime("%I:%M:%S %p | %d %B %Y")
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
                w = self.root.winfo_width() or 1400
                h = self.root.winfo_height() or 900
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
                self.music_btn.configure(text="Music ON")
            except:
                pass
        else:
            try:
                pygame.mixer.music.stop()
                self.music_playing = False
                self.music_btn.configure(text="Music")
            except:
                pass

    # Module launchers
    def student_details(self):
        try:
            from student_management import UpdatedStudentManagement
            UpdatedStudentManagement(self.root)
        except ImportError:
            messagebox.showerror("Error", 
                "Student management module not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open: {str(e)}")

    def face_recognition(self):
        try:
            from face_recognition_module import FaceRecognitionModule
            FaceRecognitionModule(self.root)
        except ImportError:
            messagebox.showerror("Error",
                "Face recognition module not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open: {str(e)}")

    def attendance(self):
        try:
            from attendance_viewer import AttendanceViewer
            AttendanceViewer(self.root)
        except ImportError:
            messagebox.showinfo("Attendance",
                "Attendance viewer not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open: {str(e)}")

    def help_desk(self):
        help_text = """
FACE RECOGNITION ATTENDANCE SYSTEM - HELP

WORKFLOW:
1. Student Details -> Add student information
2. Photos -> Capture 100+ photo samples  
3. Train Data -> Train the AI model
4. Face Recognition -> Start attendance marking

FEATURES:
- Automatic face detection and recognition
- Real-time attendance marking
- CSV export functionality
- DISHA voice assistant

FILE LOCATIONS:
- Student Data: student_data/students.csv
- Photo Samples: data/ folder
- Trained Model: trainer/trainer.yml
- Attendance: attendance/ folder

REQUIREMENTS:
- Python 3.7+
- OpenCV with contrib modules
- Working webcam

TIPS:
- Capture photos in good lighting
- Train with at least 100 samples per student
- Use DISHA for voice commands

DISHA COMMANDS:
"""
        if DISHA_VERSION == "ULTRA":
            help_text += """
ULTRA VERSION - Natural Language:
- "Hey DISHA, how many students do we have?"
- "Yo DISHA, who's absent today?"
- "DISHA, what's the attendance trend?"
- "Hey DISHA, find student named John"
"""
        else:
            help_text += """
- "Hey DISHA, how many students?"
- "Hey DISHA, open student management"
- "Hey DISHA, system status"
"""
        
        help_text += """
SUPPORT:
Developed by SMIT Students
        """
        self.show_message("Help Desk", help_text)

    def train_data(self):
        try:
            from train_data_module import TrainDataModule
            TrainDataModule(self.root)
        except ImportError:
            messagebox.showerror("Error",
                "Train data module not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open: {str(e)}")

    def photos(self):
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
                    "Photo capture module not found!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open: {str(e)}")

    def developer(self):
        dev_text = f"""
FACE RECOGNITION ATTENDANCE SYSTEM

Developed By: SMIT Students

Project Details:
- Academic Project for Smart Attendance
- Face Recognition using OpenCV & LBPH
- Real-time Attendance Marking
- DISHA Voice Assistant Integration ({DISHA_VERSION if DISHA_VERSION else "Not Available"})

Technologies:
- Python 3.x
- CustomTkinter (Modern UI)
- OpenCV (Face Recognition)
- PIL/Pillow (Image Processing)
- CSV (Data Storage)

Features:
✓ Student Management System
✓ Photo Sample Collection
✓ AI Model Training
✓ Real-time Face Recognition
✓ Automatic Attendance Marking
✓ Data Export Functionality
✓ Real-time Statistics Dashboard
✓ {DISHA_VERSION if DISHA_VERSION else "Standard"} DISHA Voice Assistant

Version: 3.0.0
Year: 2024-2025

© SMIT - All Rights Reserved
        """
        self.show_message("Developer Information", dev_text)

    def settings(self):
        settings_text = f"""
SYSTEM SETTINGS

Current Configuration:
- Camera Index: 0 (Default)
- Confidence Threshold: 50%
- Max Photo Samples: 100
- Recognition Algorithm: LBPH

Feature Status:
- Video Background: {"Enabled" if self.video_enabled else "Disabled"}
- Background Music: {"Available" if (PYGAME_AVAILABLE and MUSIC_PATH) else "Not Available"}
- Real-time Statistics: {"Enabled" if STATS_AVAILABLE else "Disabled"}
- DISHA Voice Assistant: {DISHA_VERSION if DISHA_VERSION else "Not Available"}

DISHA Voice Assistant:
- Click floating DISHA button to activate
"""
        if DISHA_VERSION == "ULTRA":
            settings_text += "- ULTRA VERSION: Natural language supported\n"
            settings_text += "- Just speak naturally - no exact commands needed\n"
        else:
            settings_text += "- Say 'Hey DISHA' + command\n"
        
        settings_text += "- Voice commands available for all operations"
        
        self.show_message("Settings", settings_text)

    def show_message(self, title, message):
        msg_win = ctk.CTkToplevel(self.root)
        msg_win.title(title)
        msg_win.geometry("750x650")
        msg_win.transient(self.root)
        
        text = ctk.CTkTextbox(msg_win, font=ctk.CTkFont(size=12))
        text.pack(fill="both", expand=True, padx=25, pady=25)
        text.insert("1.0", message)
        text.configure(state="disabled")
        
        close_btn = ctk.CTkButton(msg_win, text="Close", 
                                  command=msg_win.destroy,
                                  height=50,
                                  width=180,
                                  font=ctk.CTkFont(size=15, weight="bold"))
        close_btn.pack(pady=(0, 25))

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.destroy()

    def destroy(self):
        self.running = False
        
        if self.disha:
            try:
                self.disha.stop()
            except:
                pass
        
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
        self.root.mainloop()


if __name__ == "__main__":
    app = FaceRecognitionUI()
    app.run()
