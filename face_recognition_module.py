# # # import tkinter as tk
# # # from tkinter import ttk, messagebox
# # # import cv2
# # # from PIL import Image, ImageTk
# # # import numpy as np
# # # import os
# # # from datetime import datetime
# # # import csv

# # # class FaceRecognitionModule:
# # #     def __init__(self, parent):
# # #         self.parent = parent
# # #         self.window = tk.Toplevel(parent)
# # #         self.window.title("Face Recognition System")
# # #         self.window.geometry("1200x800")
# # #         self.window.configure(bg='#0a0a2e')
# # #         self.window.state('zoomed')
        
# # #         # Center the window
# # #         self.window.transient(parent)
# # #         self.window.grab_set()
        
# # #         # Initialize face detection
# # #         self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# # #         self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
# # #         # Video capture
# # #         self.cap = None
# # #         self.is_running = False
        
# # #         # Recognition variables
# # #         self.recognized_students = set()
# # #         self.confidence_threshold = 50
        
# # #         # Load trained model if exists
# # #         self.load_trained_model()
        
# # #         self.create_ui()
        
# # #         # Handle window close
# # #         self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
# # #     def create_ui(self):
# # #         # Main container
# # #         main_container = tk.Frame(self.window, bg='#0a0a2e')
# # #         main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
# # #         # Title
# # #         title_label = tk.Label(main_container, text="FACE RECOGNITION ATTENDANCE SYSTEM",
# # #                               fg='#00ffff', bg='#0a0a2e', font=('Arial', 24, 'bold'))
# # #         title_label.pack(pady=(0, 20))
        
# # #         # Content frame
# # #         content_frame = tk.Frame(main_container, bg='#0a0a2e')
# # #         content_frame.pack(fill='both', expand=True)
        
# # #         # Left panel - Video feed
# # #         self.create_video_panel(content_frame)
        
# # #         # Right panel - Controls and info
# # #         self.create_control_panel(content_frame)
        
# # #         # Bottom panel - Recognized students
# # #         self.create_recognition_panel(main_container)
    
# # #     def create_video_panel(self, parent):
# # #         video_frame = tk.LabelFrame(parent, text="Live Camera Feed",
# # #                                    font=('Arial', 14, 'bold'), bg='#16213e',
# # #                                    fg='#00ffff', bd=2, relief='raised')
# # #         video_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
# # #         # Video display label
# # #         self.video_label = tk.Label(video_frame, bg='black')
# # #         self.video_label.pack(padx=10, pady=10, fill='both', expand=True)
        
# # #         # Status label
# # #         self.status_label = tk.Label(video_frame, text="Camera Status: OFF",
# # #                                     fg='#ff6b6b', bg='#16213e',
# # #                                     font=('Arial', 12, 'bold'))
# # #         self.status_label.pack(pady=5)
    
# # #     def create_control_panel(self, parent):
# # #         control_frame = tk.LabelFrame(parent, text="Controls & Settings",
# # #                                      font=('Arial', 14, 'bold'), bg='#16213e',
# # #                                      fg='#00ffff', bd=2, relief='raised')
# # #         control_frame.pack(side='right', fill='both', padx=(10, 0))
        
# # #         # Time display
# # #         time_frame = tk.Frame(control_frame, bg='#16213e')
# # #         time_frame.pack(fill='x', padx=10, pady=10)
        
# # #         self.time_label = tk.Label(time_frame, text="", fg='#00ffff',
# # #                                   bg='#16213e', font=('Arial', 14, 'bold'))
# # #         self.time_label.pack()
# # #         self.update_time()
        
# # #         # Camera controls
# # #         tk.Label(control_frame, text="Camera Controls",
# # #                 font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(10, 5))
        
# # #         self.start_btn = tk.Button(control_frame, text="▶ START CAMERA",
# # #                                   bg='#2ecc71', fg='white',
# # #                                   font=('Arial', 12, 'bold'),
# # #                                   width=20, height=2,
# # #                                   command=self.start_camera)
# # #         self.start_btn.pack(pady=5, padx=10)
        
# # #         self.stop_btn = tk.Button(control_frame, text="⏹ STOP CAMERA",
# # #                                  bg='#e74c3c', fg='white',
# # #                                  font=('Arial', 12, 'bold'),
# # #                                  width=20, height=2,
# # #                                  command=self.stop_camera,
# # #                                  state='disabled')
# # #         self.stop_btn.pack(pady=5, padx=10)
        
# # #         # Recognition settings
# # #         tk.Label(control_frame, text="Recognition Settings",
# # #                 font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(20, 5))
        
# # #         # Confidence threshold
# # #         threshold_frame = tk.Frame(control_frame, bg='#16213e')
# # #         threshold_frame.pack(fill='x', padx=10, pady=5)
        
# # #         tk.Label(threshold_frame, text="Confidence:",
# # #                 fg='white', bg='#16213e').pack(side='left')
        
# # #         self.threshold_var = tk.IntVar(value=50)
# # #         threshold_scale = tk.Scale(threshold_frame, from_=0, to=100,
# # #                                   orient='horizontal', variable=self.threshold_var,
# # #                                   bg='#16213e', fg='white', highlightthickness=0,
# # #                                   command=self.update_threshold)
# # #         threshold_scale.pack(side='left', fill='x', expand=True, padx=5)
        
# # #         self.threshold_label = tk.Label(threshold_frame, text="50%",
# # #                                        fg='#00ffff', bg='#16213e',
# # #                                        font=('Arial', 10, 'bold'))
# # #         self.threshold_label.pack(side='left')
        
# # #         # Statistics
# # #         tk.Label(control_frame, text="Statistics",
# # #                 font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(20, 5))
        
# # #         stats_frame = tk.Frame(control_frame, bg='#16213e')
# # #         stats_frame.pack(fill='x', padx=10, pady=5)
        
# # #         self.faces_detected_label = tk.Label(stats_frame, text="Faces Detected: 0",
# # #                                             fg='white', bg='#16213e',
# # #                                             font=('Arial', 10))
# # #         self.faces_detected_label.pack(anchor='w', pady=2)
        
# # #         self.recognized_count_label = tk.Label(stats_frame, text="Recognized: 0",
# # #                                               fg='#2ecc71', bg='#16213e',
# # #                                               font=('Arial', 10))
# # #         self.recognized_count_label.pack(anchor='w', pady=2)
        
# # #         self.unknown_count_label = tk.Label(stats_frame, text="Unknown: 0",
# # #                                            fg='#e74c3c', bg='#16213e',
# # #                                            font=('Arial', 10))
# # #         self.unknown_count_label.pack(anchor='w', pady=2)
        
# # #         # Action buttons
# # #         tk.Label(control_frame, text="Actions",
# # #                 font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(20, 5))
        
# # #         tk.Button(control_frame, text="📊 View Attendance",
# # #                  bg='#3498db', fg='white',
# # #                  font=('Arial', 10, 'bold'),
# # #                  width=20, height=2,
# # #                  command=self.view_attendance).pack(pady=5, padx=10)
        
# # #         tk.Button(control_frame, text="🔄 Reset Session",
# # #                  bg='#f39c12', fg='white',
# # #                  font=('Arial', 10, 'bold'),
# # #                  width=20, height=2,
# # #                  command=self.reset_session).pack(pady=5, padx=10)
        
# # #         tk.Button(control_frame, text="💾 Export Attendance",
# # #                  bg='#9b59b6', fg='white',
# # #                  font=('Arial', 10, 'bold'),
# # #                  width=20, height=2,
# # #                  command=self.export_attendance).pack(pady=5, padx=10)
    
# # #     def create_recognition_panel(self, parent):
# # #         recognition_frame = tk.LabelFrame(parent, text="Recognized Students (Today)",
# # #                                         font=('Arial', 14, 'bold'), bg='#16213e',
# # #                                         fg='#00ffff', bd=2, relief='raised')
# # #         recognition_frame.pack(fill='both', expand=True, pady=(20, 0))
        
# # #         # Create treeview
# # #         columns = ("ID", "Name", "Time", "Confidence", "Status")
# # #         self.tree = ttk.Treeview(recognition_frame, columns=columns,
# # #                                 show='headings', height=8)
        
# # #         # Define headings
# # #         for col in columns:
# # #             self.tree.heading(col, text=col)
        
# # #         # Define column widths
# # #         self.tree.column("ID", width=100)
# # #         self.tree.column("Name", width=200)
# # #         self.tree.column("Time", width=150)
# # #         self.tree.column("Confidence", width=100)
# # #         self.tree.column("Status", width=100)
        
# # #         # Add scrollbar
# # #         scrollbar = ttk.Scrollbar(recognition_frame, orient="vertical",
# # #                                  command=self.tree.yview)
# # #         self.tree.configure(yscrollcommand=scrollbar.set)
        
# # #         self.tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
# # #         scrollbar.pack(side='right', fill='y', pady=10)
        
# # #         # Style the treeview
# # #         style = ttk.Style()
# # #         style.configure("Treeview", background="#2c3e50", foreground="white",
# # #                        fieldbackground="#2c3e50")
# # #         style.configure("Treeview.Heading", background="#34495e",
# # #                        foreground="white", font=('Arial', 10, 'bold'))
    
# # #     def update_time(self):
# # #         current_time = datetime.now().strftime("%H:%M:%S %p - %d/%m/%Y")
# # #         self.time_label.config(text=current_time)
# # #         if self.window.winfo_exists():
# # #             self.window.after(1000, self.update_time)
    
# # #     def update_threshold(self, value):
# # #         self.confidence_threshold = int(float(value))
# # #         self.threshold_label.config(text=f"{self.confidence_threshold}%")
    
# # #     def load_trained_model(self):
# # #         """Load the trained face recognition model"""
# # #         model_path = "trainer/trainer.yml"
# # #         if os.path.exists(model_path):
# # #             try:
# # #                 self.recognizer.read(model_path)
# # #                 messagebox.showinfo("Success", "Trained model loaded successfully!")
# # #             except Exception as e:
# # #                 messagebox.showwarning("Warning", 
# # #                     f"Could not load model: {str(e)}\nPlease train the model first.")
# # #         else:
# # #             messagebox.showwarning("Warning", 
# # #                 "No trained model found. Please train the model first from the main menu.")
    
# # #     def start_camera(self):
# # #         """Start the camera and face recognition"""
# # #         try:
# # #             self.cap = cv2.VideoCapture(0)
# # #             if not self.cap.isOpened():
# # #                 messagebox.showerror("Error", "Could not open camera!")
# # #                 return
            
# # #             self.is_running = True
# # #             self.start_btn.config(state='disabled')
# # #             self.stop_btn.config(state='normal')
# # #             self.status_label.config(text="Camera Status: ACTIVE", fg='#2ecc71')
            
# # #             self.process_video()
            
# # #         except Exception as e:
# # #             messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
    
# # #     def stop_camera(self):
# # #         """Stop the camera"""
# # #         self.is_running = False
# # #         if self.cap is not None:
# # #             self.cap.release()
        
# # #         self.start_btn.config(state='normal')
# # #         self.stop_btn.config(state='disabled')
# # #         self.status_label.config(text="Camera Status: OFF", fg='#ff6b6b')
# # #         self.video_label.config(image='', bg='black')
    
# # #     def process_video(self):
# # #         """Process video frames for face recognition"""
# # #         if not self.is_running:
# # #             return
        
# # #         ret, frame = self.cap.read()
# # #         if ret:
# # #             # Convert to grayscale for face detection
# # #             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
# # #             # Detect faces
# # #             faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
# # #             faces_detected = len(faces)
# # #             recognized = 0
# # #             unknown = 0
            
# # #             # Process each detected face
# # #             for (x, y, w, h) in faces:
# # #                 # Draw rectangle around face
# # #                 cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
# # #                 # Try to recognize the face
# # #                 roi_gray = gray[y:y+h, x:x+w]
                
# # #                 try:
# # #                     id_, confidence = self.recognizer.predict(roi_gray)
                    
# # #                     # Check if confidence is good enough
# # #                     if confidence < 100 - self.confidence_threshold:
# # #                         # Load student name from file
# # #                         name = self.get_student_name(id_)
# # #                         confidence_text = f"{round(100 - confidence)}%"
                        
# # #                         # Mark attendance
# # #                         if id_ not in self.recognized_students:
# # #                             self.mark_attendance(id_, name, confidence_text)
# # #                             self.recognized_students.add(id_)
                        
# # #                         recognized += 1
# # #                         color = (0, 255, 0)  # Green
# # #                     else:
# # #                         name = "Unknown"
# # #                         confidence_text = "Low"
# # #                         unknown += 1
# # #                         color = (0, 0, 255)  # Red
                    
# # #                     # Display name and confidence
# # #                     cv2.putText(frame, name, (x, y-10),
# # #                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
# # #                     cv2.putText(frame, confidence_text, (x, y+h+25),
# # #                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    
# # #                 except Exception as e:
# # #                     # If no model is loaded or error occurs
# # #                     cv2.putText(frame, "Unknown", (x, y-10),
# # #                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
# # #                     unknown += 1
            
# # #             # Update statistics
# # #             self.faces_detected_label.config(text=f"Faces Detected: {faces_detected}")
# # #             self.recognized_count_label.config(text=f"Recognized: {recognized}")
# # #             self.unknown_count_label.config(text=f"Unknown: {unknown}")
            
# # #             # Convert frame to PhotoImage
# # #             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# # #             img = Image.fromarray(frame_rgb)
# # #             img = img.resize((640, 480), Image.Resampling.LANCZOS)
# # #             photo = ImageTk.PhotoImage(image=img)
            
# # #             self.video_label.config(image=photo)
# # #             self.video_label.image = photo
        
# # #         # Continue processing
# # #         if self.is_running:
# # #             self.window.after(10, self.process_video)
    
# # #     def get_student_name(self, student_id):
# # #         """Get student name from CSV file"""
# # #         try:
# # #             with open('student_data/students.csv', 'r') as file:
# # #                 reader = csv.DictReader(file)
# # #                 for row in reader:
# # #                     if int(row['StudentID']) == student_id:
# # #                         return row['Name']
# # #         except FileNotFoundError:
# # #             pass
# # #         return f"Student_{student_id}"
    
# # #     def mark_attendance(self, student_id, name, confidence):
# # #         """Mark attendance in the treeview and save to file"""
# # #         current_time = datetime.now().strftime("%H:%M:%S")
        
# # #         # Add to treeview
# # #         self.tree.insert("", 0, values=(
# # #             student_id,
# # #             name,
# # #             current_time,
# # #             confidence,
# # #             "Present"
# # #         ))
        
# # #         # Save to attendance file
# # #         self.save_attendance(student_id, name, current_time, confidence)
    
# # #     def save_attendance(self, student_id, name, time, confidence):
# # #         """Save attendance to CSV file"""
# # #         date = datetime.now().strftime("%Y-%m-%d")
# # #         filename = f"attendance/attendance_{date}.csv"
        
# # #         # Create directory if it doesn't exist
# # #         os.makedirs("attendance", exist_ok=True)
        
# # #         # Check if file exists
# # #         file_exists = os.path.isfile(filename)
        
# # #         try:
# # #             with open(filename, 'a', newline='') as file:
# # #                 writer = csv.writer(file)
                
# # #                 # Write header if file is new
# # #                 if not file_exists:
# # #                     writer.writerow(['StudentID', 'Name', 'Time', 'Confidence', 'Date'])
                
# # #                 # Write attendance record
# # #                 writer.writerow([student_id, name, time, confidence, date])
# # #         except Exception as e:
# # #             messagebox.showerror("Error", f"Failed to save attendance: {str(e)}")
    
# # #     def view_attendance(self):
# # #         """View today's attendance"""
# # #         messagebox.showinfo("Attendance", 
# # #             f"Total students marked present: {len(self.recognized_students)}")
    
# # #     def reset_session(self):
# # #         """Reset the current recognition session"""
# # #         if messagebox.askyesno("Confirm", "Reset current session? This will clear recognized students."):
# # #             self.recognized_students.clear()
# # #             self.tree.delete(*self.tree.get_children())
# # #             messagebox.showinfo("Success", "Session reset successfully!")
    
# # #     def export_attendance(self):
# # #         """Export attendance to file"""
# # #         date = datetime.now().strftime("%Y-%m-%d")
# # #         filename = f"attendance/attendance_{date}.csv"
        
# # #         if os.path.exists(filename):
# # #             messagebox.showinfo("Success", 
# # #                 f"Attendance exported to:\n{filename}")
# # #         else:
# # #             messagebox.showwarning("Warning", "No attendance records found for today.")
    
# # #     def on_closing(self):
# # #         """Handle window closing"""
# # #         self.stop_camera()
# # #         self.window.destroy()

# # # if __name__ == "__main__":
# # #     # Test the module
# # #     root = tk.Tk()
# # #     root.withdraw()
# # #     app = FaceRecognitionModule(root)
# # #     root.mainloop()

# # import tkinter as tk
# # from tkinter import ttk, messagebox
# # import cv2
# # from PIL import Image, ImageTk
# # import numpy as np
# # import os
# # from datetime import datetime
# # import csv

# # # Import liveness detection
# # try:
# #     from liveness_detection_module import LivenessIntegration
# #     LIVENESS_AVAILABLE = True
# # except ImportError:
# #     LIVENESS_AVAILABLE = False
# #     print("Warning: Liveness detection module not found. Running without liveness detection.")

# # class FaceRecognitionModule:
# #     def __init__(self, parent):
# #         self.parent = parent
# #         self.window = tk.Toplevel(parent)
# #         self.window.title("Face Recognition System with Liveness Detection")
# #         self.window.geometry("1200x800")
# #         self.window.configure(bg='#0a0a2e')
# #         self.window.state('zoomed')
        
# #         # Center the window
# #         self.window.transient(parent)
# #         self.window.grab_set()
        
# #         # Initialize face detection
# #         self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# #         self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
# #         # Video capture
# #         self.cap = None
# #         self.is_running = False
        
# #         # Recognition variables
# #         self.recognized_students = set()
# #         self.confidence_threshold = 50
        
# #         # Liveness detection integration
# #         if LIVENESS_AVAILABLE:
# #             self.liveness = LivenessIntegration()
# #             self.liveness_enabled = True
# #         else:
# #             self.liveness = None
# #             self.liveness_enabled = False
        
# #         # Load trained model if exists
# #         self.load_trained_model()
        
# #         self.create_ui()
        
# #         # Handle window close
# #         self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
# #     def create_ui(self):
# #         # Main container
# #         main_container = tk.Frame(self.window, bg='#0a0a2e')
# #         main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
# #         # Title
# #         title_text = "FACE RECOGNITION ATTENDANCE SYSTEM"
# #         if LIVENESS_AVAILABLE:
# #             title_text += " (with Liveness Detection)"
        
# #         title_label = tk.Label(main_container, text=title_text,
# #                               fg='#00ffff', bg='#0a0a2e', font=('Arial', 24, 'bold'))
# #         title_label.pack(pady=(0, 20))
        
# #         # Content frame
# #         content_frame = tk.Frame(main_container, bg='#0a0a2e')
# #         content_frame.pack(fill='both', expand=True)
        
# #         # Left panel - Video feed
# #         self.create_video_panel(content_frame)
        
# #         # Right panel - Controls and info
# #         self.create_control_panel(content_frame)
        
# #         # Bottom panel - Recognized students
# #         self.create_recognition_panel(main_container)
    
# #     def create_video_panel(self, parent):
# #         video_frame = tk.LabelFrame(parent, text="Live Camera Feed",
# #                                    font=('Arial', 14, 'bold'), bg='#16213e',
# #                                    fg='#00ffff', bd=2, relief='raised')
# #         video_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
# #         # Video display label
# #         self.video_label = tk.Label(video_frame, bg='black')
# #         self.video_label.pack(padx=10, pady=10, fill='both', expand=True)
        
# #         # Status label
# #         self.status_label = tk.Label(video_frame, text="Camera Status: OFF",
# #                                     fg='#ff6b6b', bg='#16213e',
# #                                     font=('Arial', 12, 'bold'))
# #         self.status_label.pack(pady=5)
        
# #         # Liveness status (if available)
# #         if LIVENESS_AVAILABLE:
# #             self.liveness_status_label = tk.Label(video_frame, 
# #                                                  text="🛡️ Liveness Detection: ACTIVE",
# #                                                  fg='#2ecc71', bg='#16213e',
# #                                                  font=('Arial', 10, 'bold'))
# #             self.liveness_status_label.pack(pady=2)
    
# #     def create_control_panel(self, parent):
# #         control_frame = tk.LabelFrame(parent, text="Controls & Settings",
# #                                      font=('Arial', 14, 'bold'), bg='#16213e',
# #                                      fg='#00ffff', bd=2, relief='raised')
# #         control_frame.pack(side='right', fill='both', padx=(10, 0))
        
# #         # Time display
# #         time_frame = tk.Frame(control_frame, bg='#16213e')
# #         time_frame.pack(fill='x', padx=10, pady=10)
        
# #         self.time_label = tk.Label(time_frame, text="", fg='#00ffff',
# #                                   bg='#16213e', font=('Arial', 14, 'bold'))
# #         self.time_label.pack()
# #         self.update_time()
        
# #         # Camera controls
# #         tk.Label(control_frame, text="Camera Controls",
# #                 font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(10, 5))
        
# #         self.start_btn = tk.Button(control_frame, text="▶ START CAMERA",
# #                                   bg='#2ecc71', fg='white',
# #                                   font=('Arial', 12, 'bold'),
# #                                   width=20, height=2,
# #                                   command=self.start_camera)
# #         self.start_btn.pack(pady=5, padx=10)
        
# #         self.stop_btn = tk.Button(control_frame, text="⏹ STOP CAMERA",
# #                                  bg='#e74c3c', fg='white',
# #                                  font=('Arial', 12, 'bold'),
# #                                  width=20, height=2,
# #                                  command=self.stop_camera,
# #                                  state='disabled')
# #         self.stop_btn.pack(pady=5, padx=10)
        
# #         # Recognition settings
# #         tk.Label(control_frame, text="Recognition Settings",
# #                 font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(20, 5))
        
# #         # Confidence threshold
# #         threshold_frame = tk.Frame(control_frame, bg='#16213e')
# #         threshold_frame.pack(fill='x', padx=10, pady=5)
        
# #         tk.Label(threshold_frame, text="Confidence:",
# #                 fg='white', bg='#16213e').pack(side='left')
        
# #         self.threshold_var = tk.IntVar(value=50)
# #         threshold_scale = tk.Scale(threshold_frame, from_=0, to=100,
# #                                   orient='horizontal', variable=self.threshold_var,
# #                                   bg='#16213e', fg='white', highlightthickness=0,
# #                                   command=self.update_threshold)
# #         threshold_scale.pack(side='left', fill='x', expand=True, padx=5)
        
# #         self.threshold_label = tk.Label(threshold_frame, text="50%",
# #                                        fg='#00ffff', bg='#16213e',
# #                                        font=('Arial', 10, 'bold'))
# #         self.threshold_label.pack(side='left')
        
# #         # Liveness toggle (if available)
# #         if LIVENESS_AVAILABLE:
# #             liveness_frame = tk.Frame(control_frame, bg='#16213e')
# #             liveness_frame.pack(fill='x', padx=10, pady=5)
            
# #             self.liveness_var = tk.BooleanVar(value=True)
# #             liveness_check = tk.Checkbutton(liveness_frame, 
# #                                            text="Enable Liveness Detection",
# #                                            variable=self.liveness_var,
# #                                            bg='#16213e', fg='white',
# #                                            selectcolor='#2c3e50',
# #                                            font=('Arial', 10),
# #                                            command=self.toggle_liveness)
# #             liveness_check.pack(side='left')
        
# #         # Statistics
# #         tk.Label(control_frame, text="Statistics",
# #                 font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(20, 5))
        
# #         stats_frame = tk.Frame(control_frame, bg='#16213e')
# #         stats_frame.pack(fill='x', padx=10, pady=5)
        
# #         self.faces_detected_label = tk.Label(stats_frame, text="Faces Detected: 0",
# #                                             fg='white', bg='#16213e',
# #                                             font=('Arial', 10))
# #         self.faces_detected_label.pack(anchor='w', pady=2)
        
# #         self.recognized_count_label = tk.Label(stats_frame, text="Recognized: 0",
# #                                               fg='#2ecc71', bg='#16213e',
# #                                               font=('Arial', 10))
# #         self.recognized_count_label.pack(anchor='w', pady=2)
        
# #         self.unknown_count_label = tk.Label(stats_frame, text="Unknown: 0",
# #                                            fg='#e74c3c', bg='#16213e',
# #                                            font=('Arial', 10))
# #         self.unknown_count_label.pack(anchor='w', pady=2)
        
# #         if LIVENESS_AVAILABLE:
# #             self.spoof_count_label = tk.Label(stats_frame, text="Spoofs Blocked: 0",
# #                                              fg='#f39c12', bg='#16213e',
# #                                              font=('Arial', 10))
# #             self.spoof_count_label.pack(anchor='w', pady=2)
# #             self.spoof_blocked = 0
        
# #         # Action buttons
# #         tk.Label(control_frame, text="Actions",
# #                 font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(20, 5))
        
# #         tk.Button(control_frame, text="📊 View Attendance",
# #                  bg='#3498db', fg='white',
# #                  font=('Arial', 10, 'bold'),
# #                  width=20, height=2,
# #                  command=self.view_attendance).pack(pady=5, padx=10)
        
# #         tk.Button(control_frame, text="🔄 Reset Session",
# #                  bg='#f39c12', fg='white',
# #                  font=('Arial', 10, 'bold'),
# #                  width=20, height=2,
# #                  command=self.reset_session).pack(pady=5, padx=10)
        
# #         tk.Button(control_frame, text="💾 Export Attendance",
# #                  bg='#9b59b6', fg='white',
# #                  font=('Arial', 10, 'bold'),
# #                  width=20, height=2,
# #                  command=self.export_attendance).pack(pady=5, padx=10)
    
# #     def create_recognition_panel(self, parent):
# #         recognition_frame = tk.LabelFrame(parent, text="Recognized Students (Today)",
# #                                         font=('Arial', 14, 'bold'), bg='#16213e',
# #                                         fg='#00ffff', bd=2, relief='raised')
# #         recognition_frame.pack(fill='both', expand=True, pady=(20, 0))
        
# #         # Create treeview
# #         columns = ["ID", "Name", "Time", "Confidence", "Status"]
# #         if LIVENESS_AVAILABLE:
# #             columns.append("Liveness")
        
# #         self.tree = ttk.Treeview(recognition_frame, columns=columns,
# #                                 show='headings', height=8)
        
# #         # Define headings
# #         for col in columns:
# #             self.tree.heading(col, text=col)
        
# #         # Define column widths
# #         self.tree.column("ID", width=100)
# #         self.tree.column("Name", width=200)
# #         self.tree.column("Time", width=150)
# #         self.tree.column("Confidence", width=100)
# #         self.tree.column("Status", width=100)
# #         if LIVENESS_AVAILABLE:
# #             self.tree.column("Liveness", width=100)
        
# #         # Add scrollbar
# #         scrollbar = ttk.Scrollbar(recognition_frame, orient="vertical",
# #                                  command=self.tree.yview)
# #         self.tree.configure(yscrollcommand=scrollbar.set)
        
# #         self.tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
# #         scrollbar.pack(side='right', fill='y', pady=10)
        
# #         # Style the treeview
# #         style = ttk.Style()
# #         style.configure("Treeview", background="#2c3e50", foreground="white",
# #                        fieldbackground="#2c3e50")
# #         style.configure("Treeview.Heading", background="#34495e",
# #                        foreground="white", font=('Arial', 10, 'bold'))
    
# #     def update_time(self):
# #         current_time = datetime.now().strftime("%H:%M:%S %p - %d/%m/%Y")
# #         self.time_label.config(text=current_time)
# #         if self.window.winfo_exists():
# #             self.window.after(1000, self.update_time)
    
# #     def update_threshold(self, value):
# #         self.confidence_threshold = int(float(value))
# #         self.threshold_label.config(text=f"{self.confidence_threshold}%")
    
# #     def toggle_liveness(self):
# #         """Toggle liveness detection on/off"""
# #         if self.liveness:
# #             self.liveness_enabled = self.liveness_var.get()
# #             self.liveness.enable_liveness(self.liveness_enabled)
            
# #             status = "ACTIVE" if self.liveness_enabled else "DISABLED"
# #             color = "#2ecc71" if self.liveness_enabled else "#e74c3c"
# #             self.liveness_status_label.config(
# #                 text=f"🛡️ Liveness Detection: {status}",
# #                 fg=color
# #             )
    
# #     def load_trained_model(self):
# #         """Load the trained face recognition model"""
# #         model_path = "trainer/trainer.yml"
# #         if os.path.exists(model_path):
# #             try:
# #                 self.recognizer.read(model_path)
# #                 msg = "Trained model loaded successfully!"
# #                 if LIVENESS_AVAILABLE:
# #                     msg += "\n\n🛡️ Liveness Detection is ACTIVE"
# #                 messagebox.showinfo("Success", msg)
# #             except Exception as e:
# #                 messagebox.showwarning("Warning", 
# #                     f"Could not load model: {str(e)}\nPlease train the model first.")
# #         else:
# #             messagebox.showwarning("Warning", 
# #                 "No trained model found. Please train the model first from the main menu.")
    
# #     def start_camera(self):
# #         """Start the camera and face recognition"""
# #         try:
# #             self.cap = cv2.VideoCapture(0)
# #             if not self.cap.isOpened():
# #                 messagebox.showerror("Error", "Could not open camera!")
# #                 return
            
# #             self.is_running = True
# #             self.start_btn.config(state='disabled')
# #             self.stop_btn.config(state='normal')
# #             self.status_label.config(text="Camera Status: ACTIVE", fg='#2ecc71')
            
# #             # Reset liveness detector
# #             if self.liveness:
# #                 self.liveness.reset_detector()
            
# #             self.process_video()
            
# #         except Exception as e:
# #             messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
    
# #     def stop_camera(self):
# #         """Stop the camera"""
# #         self.is_running = False
# #         if self.cap is not None:
# #             self.cap.release()
        
# #         self.start_btn.config(state='normal')
# #         self.stop_btn.config(state='disabled')
# #         self.status_label.config(text="Camera Status: OFF", fg='#ff6b6b')
# #         self.video_label.config(image='', bg='black')
    
# #     def process_video(self):
# #         """Process video frames for face recognition with liveness detection"""
# #         if not self.is_running:
# #             return
        
# #         ret, frame = self.cap.read()
# #         if ret:
# #             # Convert to grayscale for face detection
# #             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
# #             # Detect faces
# #             faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
# #             faces_detected = len(faces)
# #             recognized = 0
# #             unknown = 0
            
# #             # Process each detected face
# #             for (x, y, w, h) in faces:
# #                 # Try to recognize the face
# #                 roi_gray = gray[y:y+h, x:x+w]
                
# #                 try:
# #                     id_, confidence = self.recognizer.predict(roi_gray)
                    
# #                     # Check if confidence is good enough
# #                     if confidence < 100 - self.confidence_threshold:
# #                         # Load student name from file
# #                         name = self.get_student_name(id_)
# #                         confidence_text = f"{round(100 - confidence)}%"
                        
# #                         # Liveness detection check
# #                         liveness_passed = True
# #                         liveness_conf = 100
# #                         liveness_status = "N/A"
                        
# #                         if self.liveness_enabled and self.liveness and id_ not in self.recognized_students:
# #                             # Run liveness check
# #                             frame, liveness_passed, liveness_info = self.liveness.process_frame_with_liveness(
# #                                 frame, [(x, y, w, h)], self.recognizer, id_, confidence
# #                             )
                            
# #                             liveness_conf = liveness_info['confidence']
# #                             liveness_status = liveness_info['status']
                            
# #                             if not liveness_passed:
# #                                 # Spoof detected - don't mark attendance
# #                                 self.spoof_blocked += 1
# #                                 self.spoof_count_label.config(
# #                                     text=f"Spoofs Blocked: {self.spoof_blocked}"
# #                                 )
# #                                 name = "SPOOF DETECTED"
# #                                 color = (0, 0, 255)  # Red
# #                             else:
# #                                 color = (0, 255, 0)  # Green
# #                                 recognized += 1
# #                         else:
# #                             color = (0, 255, 0)  # Green
# #                             recognized += 1
# #                             if not self.liveness_enabled:
# #                                 liveness_status = "Disabled"
                        
# #                         # Mark attendance only if liveness passed (or disabled)
# #                         if (not self.liveness_enabled or liveness_passed) and id_ not in self.recognized_students:
# #                             self.mark_attendance(id_, name, confidence_text, liveness_status)
# #                             self.recognized_students.add(id_)
                        
# #                         # Draw rectangle and info (if not using liveness visualization)
# #                         if not (self.liveness_enabled and self.liveness):
# #                             cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
# #                             cv2.putText(frame, name, (x, y-10),
# #                                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
# #                             cv2.putText(frame, confidence_text, (x, y+h+25),
# #                                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    
# #                     else:
# #                         name = "Unknown"
# #                         confidence_text = "Low"
# #                         unknown += 1
# #                         color = (0, 0, 255)  # Red
                        
# #                         cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
# #                         cv2.putText(frame, name, (x, y-10),
# #                                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
# #                         cv2.putText(frame, confidence_text, (x, y+h+25),
# #                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    
# #                 except Exception as e:
# #                     # If no model is loaded or error occurs
# #                     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
# #                     cv2.putText(frame, "Unknown", (x, y-10),
# #                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
# #                     unknown += 1
            
# #             # Update statistics
# #             self.faces_detected_label.config(text=f"Faces Detected: {faces_detected}")
# #             self.recognized_count_label.config(text=f"Recognized: {recognized}")
# #             self.unknown_count_label.config(text=f"Unknown: {unknown}")
            
# #             # Convert frame to PhotoImage
# #             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #             img = Image.fromarray(frame_rgb)
# #             img = img.resize((640, 480), Image.Resampling.LANCZOS)
# #             photo = ImageTk.PhotoImage(image=img)
            
# #             self.video_label.config(image=photo)
# #             self.video_label.image = photo
        
# #         # Continue processing
# #         if self.is_running:
# #             self.window.after(10, self.process_video)
    
# #     def get_student_name(self, student_id):
# #         """Get student name from CSV file"""
# #         try:
# #             with open('student_data/students.csv', 'r') as file:
# #                 reader = csv.DictReader(file)
# #                 for row in reader:
# #                     if int(row['StudentID']) == student_id:
# #                         return row['Name']
# #         except FileNotFoundError:
# #             pass
# #         return f"Student_{student_id}"
    
# #     def mark_attendance(self, student_id, name, confidence, liveness_status="N/A"):
# #         """Mark attendance in the treeview and save to file"""
# #         current_time = datetime.now().strftime("%H:%M:%S")
        
# #         # Prepare values for treeview
# #         values = [student_id, name, current_time, confidence, "Present"]
# #         if LIVENESS_AVAILABLE:
# #             values.append(liveness_status)
        
# #         # Add to treeview
# #         self.tree.insert("", 0, values=tuple(values))
        
# #         # Save to attendance file
# #         self.save_attendance(student_id, name, current_time, confidence, liveness_status)
    
# #     def save_attendance(self, student_id, name, time, confidence, liveness_status="N/A"):
# #         """Save attendance to CSV file"""
# #         date = datetime.now().strftime("%Y-%m-%d")
# #         filename = f"attendance/attendance_{date}.csv"
        
# #         # Create directory if it doesn't exist
# #         os.makedirs("attendance", exist_ok=True)
        
# #         # Check if file exists
# #         file_exists = os.path.isfile(filename)
        
# #         try:
# #             with open(filename, 'a', newline='') as file:
# #                 fieldnames = ['StudentID', 'Name', 'Time', 'Confidence', 'Date']
# #                 if LIVENESS_AVAILABLE:
# #                     fieldnames.append('LivenessStatus')
                
# #                 writer = csv.DictWriter(file, fieldnames=fieldnames)
                
# #                 # Write header if file is new
# #                 if not file_exists:
# #                     writer.writeheader()
                
# #                 # Write attendance record
# #                 row_data = {
# #                     'StudentID': student_id,
# #                     'Name': name,
# #                     'Time': time,
# #                     'Confidence': confidence,
# #                     'Date': date
# #                 }
                
# #                 if LIVENESS_AVAILABLE:
# #                     row_data['LivenessStatus'] = liveness_status
                
# #                 writer.writerow(row_data)
                
# #         except Exception as e:
# #             messagebox.showerror("Error", f"Failed to save attendance: {str(e)}")
    
# #     def view_attendance(self):
# #         """View today's attendance"""
# #         msg = f"Total students marked present: {len(self.recognized_students)}"
# #         if LIVENESS_AVAILABLE:
# #             msg += f"\nSpoofs blocked: {self.spoof_blocked}"
# #         messagebox.showinfo("Attendance", msg)
    
# #     def reset_session(self):
# #         """Reset the current recognition session"""
# #         if messagebox.askyesno("Confirm", "Reset current session? This will clear recognized students."):
# #             self.recognized_students.clear()
# #             self.tree.delete(*self.tree.get_children())
            
# #             if LIVENESS_AVAILABLE:
# #                 self.spoof_blocked = 0
# #                 self.spoof_count_label.config(text="Spoofs Blocked: 0")
# #                 if self.liveness:
# #                     self.liveness.reset_detector()
# #                     self.liveness.clear_results()
            
# #             messagebox.showinfo("Success", "Session reset successfully!")
    
# #     def export_attendance(self):
# #         """Export attendance to file"""
# #         date = datetime.now().strftime("%Y-%m-%d")
# #         filename = f"attendance/attendance_{date}.csv"
        
# #         if os.path.exists(filename):
# #             msg = f"Attendance exported to:\n{filename}"
# #             if LIVENESS_AVAILABLE:
# #                 msg += "\n\nNote: Liveness status included in export"
# #             messagebox.showinfo("Success", msg)
# #         else:
# #             messagebox.showwarning("Warning", "No attendance records found for today.")
    
# #     def on_closing(self):
# #         """Handle window closing"""
# #         self.stop_camera()
# #         self.window.destroy()

# # if __name__ == "__main__":
# #     # Test the module
# #     root = tk.Tk()
# #     root.withdraw()
# #     app = FaceRecognitionModule(root)
# #     root.mainloop()
# """
# face_recognition_module.py - COMPLETE FIXED VERSION
# Handles all encoding issues and missing attributes
# SMIT Face Recognition Attendance System
# """

import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np
import os
from datetime import datetime
import csv

# Import liveness detection (optional)
try:
    from liveness_detection_module import LivenessIntegration
    LIVENESS_AVAILABLE = True
except ImportError:
    LIVENESS_AVAILABLE = False

class FaceRecognitionModule:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Face Recognition System")
        self.window.geometry("1200x800")
        self.window.configure(bg='#0a0a2e')
        self.window.state('zoomed')
        
        self.window.transient(parent)
        self.window.grab_set()
        
        # Initialize face detection
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Video capture
        self.cap = None
        self.is_running = False
        
        # Recognition variables
        self.recognized_students = set()
        self.confidence_threshold = 50
        
        # Liveness detection integration
        if LIVENESS_AVAILABLE:
            try:
                self.liveness = LivenessIntegration()
                self.liveness_enabled = True
            except:
                self.liveness = None
                self.liveness_enabled = False
        else:
            self.liveness = None
            self.liveness_enabled = False
        
        # Load trained model
        self.load_trained_model()
        
        self.create_ui()
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_ui(self):
        # Main container
        main_container = tk.Frame(self.window, bg='#0a0a2e')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_text = "FACE RECOGNITION ATTENDANCE SYSTEM"
        if LIVENESS_AVAILABLE and self.liveness_enabled:
            title_text += " (with Liveness Detection)"
        
        title_label = tk.Label(main_container, text=title_text,
                              fg='#00ffff', bg='#0a0a2e', font=('Arial', 20, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Content frame
        content_frame = tk.Frame(main_container, bg='#0a0a2e')
        content_frame.pack(fill='both', expand=True)
        
        # Left panel - Video feed
        self.create_video_panel(content_frame)
        
        # Right panel - Controls
        self.create_control_panel(content_frame)
        
        # Bottom panel - Recognized students
        self.create_recognition_panel(main_container)
    
    def create_video_panel(self, parent):
        video_frame = tk.LabelFrame(parent, text="Live Camera Feed",
                                   font=('Arial', 14, 'bold'), bg='#16213e',
                                   fg='#00ffff', bd=2, relief='raised')
        video_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Video display label
        self.video_label = tk.Label(video_frame, bg='black')
        self.video_label.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Status labels
        status_container = tk.Frame(video_frame, bg='#16213e')
        status_container.pack(pady=5)
        
        self.status_label = tk.Label(status_container, text="Camera Status: OFF",
                                    fg='#ff6b6b', bg='#16213e',
                                    font=('Arial', 12, 'bold'))
        self.status_label.pack()
        
        if LIVENESS_AVAILABLE and self.liveness_enabled:
            self.liveness_status_label = tk.Label(status_container, 
                                                 text="Liveness Detection: ACTIVE",
                                                 fg='#2ecc71', bg='#16213e',
                                                 font=('Arial', 10, 'bold'))
            self.liveness_status_label.pack()
    
    def create_control_panel(self, parent):
        control_frame = tk.LabelFrame(parent, text="Controls & Settings",
                                     font=('Arial', 14, 'bold'), bg='#16213e',
                                     fg='#00ffff', bd=2, relief='raised')
        control_frame.pack(side='right', fill='both', padx=(10, 0))
        
        # Time display
        time_frame = tk.Frame(control_frame, bg='#16213e')
        time_frame.pack(fill='x', padx=10, pady=10)
        
        self.time_label = tk.Label(time_frame, text="", fg='#00ffff',
                                  bg='#16213e', font=('Arial', 14, 'bold'))
        self.time_label.pack()
        self.update_time()
        
        # Camera controls
        tk.Label(control_frame, text="Camera Controls",
                font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(10, 5))
        
        self.start_btn = tk.Button(control_frame, text="▶ START CAMERA",
                                  bg='#2ecc71', fg='white',
                                  font=('Arial', 12, 'bold'),
                                  width=20, height=2,
                                  command=self.start_camera)
        self.start_btn.pack(pady=5, padx=10)
        
        self.stop_btn = tk.Button(control_frame, text="⏹ STOP CAMERA",
                                 bg='#e74c3c', fg='white',
                                 font=('Arial', 12, 'bold'),
                                 width=20, height=2,
                                 command=self.stop_camera,
                                 state='disabled')
        self.stop_btn.pack(pady=5, padx=10)
        
        # Settings
        tk.Label(control_frame, text="Settings",
                font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(20, 5))
        
        # Confidence threshold
        threshold_frame = tk.Frame(control_frame, bg='#16213e')
        threshold_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(threshold_frame, text="Confidence:",
                fg='white', bg='#16213e').pack(side='left')
        
        self.threshold_var = tk.IntVar(value=50)
        threshold_scale = tk.Scale(threshold_frame, from_=0, to=100,
                                  orient='horizontal', variable=self.threshold_var,
                                  bg='#16213e', fg='white', highlightthickness=0,
                                  command=self.update_threshold)
        threshold_scale.pack(side='left', fill='x', expand=True, padx=5)
        
        self.threshold_label = tk.Label(threshold_frame, text="50%",
                                       fg='#00ffff', bg='#16213e',
                                       font=('Arial', 10, 'bold'))
        self.threshold_label.pack(side='left')
        
        # Liveness toggle (if available)
        if LIVENESS_AVAILABLE:
            liveness_frame = tk.Frame(control_frame, bg='#16213e')
            liveness_frame.pack(fill='x', padx=10, pady=5)
            
            self.liveness_var = tk.BooleanVar(value=True)
            tk.Checkbutton(liveness_frame, text="Enable Liveness Detection",
                          variable=self.liveness_var, bg='#16213e', fg='white',
                          selectcolor='#2c3e50', font=('Arial', 10),
                          command=self.toggle_liveness).pack(side='left')
        
        # Statistics
        tk.Label(control_frame, text="Statistics",
                font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(20, 5))
        
        stats_frame = tk.Frame(control_frame, bg='#16213e')
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        self.faces_detected_label = tk.Label(stats_frame, text="Faces: 0",
                                            fg='white', bg='#16213e', font=('Arial', 10))
        self.faces_detected_label.pack(anchor='w', pady=2)
        
        self.recognized_count_label = tk.Label(stats_frame, text="Recognized: 0",
                                              fg='#2ecc71', bg='#16213e', font=('Arial', 10))
        self.recognized_count_label.pack(anchor='w', pady=2)
        
        # Action buttons
        tk.Label(control_frame, text="Actions",
                font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(20, 5))
        
        tk.Button(control_frame, text="📊 View Attendance", bg='#3498db', fg='white',
                 font=('Arial', 10, 'bold'), width=20, height=2,
                 command=self.view_attendance).pack(pady=5, padx=10)
        
        tk.Button(control_frame, text="🔄 Reset Session", bg='#f39c12', fg='white',
                 font=('Arial', 10, 'bold'), width=20, height=2,
                 command=self.reset_session).pack(pady=5, padx=10)
    
    def create_recognition_panel(self, parent):
        recognition_frame = tk.LabelFrame(parent, text="Recognized Students (Today)",
                                        font=('Arial', 14, 'bold'), bg='#16213e',
                                        fg='#00ffff', bd=2, relief='raised')
        recognition_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        columns = ["ID", "Name", "Time", "Confidence", "Status"]
        if LIVENESS_AVAILABLE and self.liveness_enabled:
            columns.append("Liveness")
        
        self.tree = ttk.Treeview(recognition_frame, columns=columns,
                                show='headings', height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column("ID", width=100)
        self.tree.column("Name", width=200)
        self.tree.column("Time", width=120)
        self.tree.column("Confidence", width=100)
        self.tree.column("Status", width=100)
        if LIVENESS_AVAILABLE and self.liveness_enabled:
            self.tree.column("Liveness", width=100)
        
        scrollbar = ttk.Scrollbar(recognition_frame, orient="vertical",
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        style = ttk.Style()
        style.configure("Treeview", background="#2c3e50", foreground="white",
                       fieldbackground="#2c3e50", font=('Arial', 10))
        style.configure("Treeview.Heading", background="#34495e",
                       foreground="white", font=('Arial', 11, 'bold'))
    
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S %p - %d/%m/%Y")
        self.time_label.config(text=current_time)
        if self.window.winfo_exists():
            self.window.after(1000, self.update_time)
    
    def update_threshold(self, value):
        self.confidence_threshold = int(float(value))
        self.threshold_label.config(text=f"{self.confidence_threshold}%")
    
    def toggle_liveness(self):
        if self.liveness:
            self.liveness_enabled = self.liveness_var.get()
            self.liveness.enable_liveness(self.liveness_enabled)
            status = "ACTIVE" if self.liveness_enabled else "DISABLED"
            color = "#2ecc71" if self.liveness_enabled else "#e74c3c"
            if hasattr(self, 'liveness_status_label'):
                self.liveness_status_label.config(
                    text=f"Liveness Detection: {status}", fg=color
                )
    
    def load_trained_model(self):
        model_path = "trainer/trainer.yml"
        if os.path.exists(model_path):
            try:
                self.recognizer.read(model_path)
                msg = "Trained model loaded successfully!"
                if LIVENESS_AVAILABLE and self.liveness_enabled:
                    msg += "\n\nLiveness Detection is ACTIVE"
                messagebox.showinfo("Success", msg)
            except Exception as e:
                messagebox.showwarning("Warning", f"Could not load model: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No trained model found.")
    
    def start_camera(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open camera!")
                return
            
            self.is_running = True
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.status_label.config(text="Camera Status: ACTIVE", fg='#2ecc71')
            
            if self.liveness:
                self.liveness.reset_detector()
            
            self.process_video()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
    
    def stop_camera(self):
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
        
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_label.config(text="Camera Status: OFF", fg='#ff6b6b')
        self.video_label.config(image='', bg='black')
    
    def process_video(self):
        if not self.is_running:
            return
        
        ret, frame = self.cap.read()
        if ret:
            frame = self.process_face_recognition(frame)
            
            # Display frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img = img.resize((640, 480), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image=img)
            
            self.video_label.config(image=photo)
            self.video_label.image = photo
        
        if self.is_running:
            self.window.after(10, self.process_video)
    
    def process_face_recognition(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        self.faces_detected_label.config(text=f"Faces: {len(faces)}")
        recognized = len(self.recognized_students)
        self.recognized_count_label.config(text=f"Recognized: {recognized}")
        
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            
            try:
                id_, confidence = self.recognizer.predict(roi_gray)
                
                if confidence < 100 - self.confidence_threshold:
                    name = self.get_student_name(id_)
                    confidence_text = f"{round(100 - confidence)}%"
                    
                    # Liveness check
                    liveness_passed = True
                    liveness_status = "N/A"
                    
                    if self.liveness_enabled and self.liveness and id_ not in self.recognized_students:
                        frame, liveness_passed, liveness_info = self.liveness.process_frame_with_liveness(
                            frame, [(x, y, w, h)], self.recognizer, id_, confidence
                        )
                        liveness_status = liveness_info['status']
                    
                    # Mark attendance if liveness passed
                    if liveness_passed and id_ not in self.recognized_students:
                        self.mark_attendance(id_, name, confidence_text, liveness_status)
                        self.recognized_students.add(id_)
                    
                    color = (0, 255, 0) if liveness_passed else (0, 0, 255)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, name, (x, y-10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                else:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(frame, "Unknown", (x, y-10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                
            except Exception as e:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, "Unknown", (x, y-10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        return frame
    
    def get_student_name(self, student_id):
        """Get student name from CSV file with proper encoding"""
        try:
            with open('student_data/students.csv', 'r', encoding='utf-8', errors='ignore') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        if int(row['StudentID']) == student_id:
                            # Clean the name - remove special characters if needed
                            name = row['Name']
                            # Replace problematic characters
                            name = name.encode('ascii', 'ignore').decode('ascii')
                            return name if name else f"Student_{student_id}"
                    except (ValueError, KeyError):
                        continue
        except Exception as e:
            print(f"Error reading student name: {e}")
        
        return f"Student_{student_id}"
    
    def mark_attendance(self, student_id, name, confidence, liveness_status="N/A"):
        """Mark attendance in the treeview and save to file"""
        current_time = datetime.now().strftime("%H:%M:%S")
        
        values = [student_id, name, current_time, confidence, "Present"]
        if LIVENESS_AVAILABLE and self.liveness_enabled:
            values.append(liveness_status)
        
        self.tree.insert("", 0, values=tuple(values))
        self.save_attendance(student_id, name, current_time, confidence, liveness_status)
    
    def save_attendance(self, student_id, name, time, confidence, liveness_status="N/A"):
        """Save attendance to CSV file with proper encoding"""
        date = datetime.now().strftime("%Y-%m-%d")
        filename = f"attendance/attendance_{date}.csv"
        os.makedirs("attendance", exist_ok=True)
        
        file_exists = os.path.isfile(filename)
        
        try:
            # Clean the name - ASCII only to avoid encoding issues
            clean_name = str(name).encode('ascii', 'ignore').decode('ascii')
            if not clean_name:
                clean_name = f"Student_{student_id}"
            
            # Open with UTF-8 encoding and error handling
            with open(filename, 'a', newline='', encoding='utf-8', errors='replace') as file:
                fieldnames = ['StudentID', 'Name', 'Time', 'Confidence', 'Date', 'Status']
                if LIVENESS_AVAILABLE and self.liveness_enabled:
                    fieldnames.append('LivenessStatus')
                
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                row_data = {
                    'StudentID': str(student_id),
                    'Name': clean_name,
                    'Time': time,
                    'Confidence': confidence,
                    'Date': date,
                    'Status': 'Present'
                }
                
                if LIVENESS_AVAILABLE and self.liveness_enabled:
                    row_data['LivenessStatus'] = liveness_status
                
                writer.writerow(row_data)
                
        except Exception as e:
            print(f"Error saving attendance: {e}")
            # Try alternative method without special characters
            try:
                with open(filename, 'a', encoding='ascii', errors='ignore') as file:
                    file.write(f"{student_id},{clean_name},{time},{confidence},{date},Present\n")
            except:
                pass
    
    def view_attendance(self):
        msg = f"Total students marked present: {len(self.recognized_students)}"
        messagebox.showinfo("Attendance", msg)
    
    def reset_session(self):
        if messagebox.askyesno("Confirm", "Reset current session?"):
            self.recognized_students.clear()
            self.tree.delete(*self.tree.get_children())
            
            if self.liveness:
                self.liveness.reset_detector()
                self.liveness.clear_results()
            
            messagebox.showinfo("Success", "Session reset successfully!")
    

    def get_real_time_stats(self):
        """Get real-time statistics for the current session"""
        return {
            'faces_detected': len(self.recognized_students),
            'total_recognized': len(self.recognized_students),
            'session_start': datetime.now().strftime("%H:%M:%S")
        }
    
    def on_closing(self):
        self.stop_camera()
        self.window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = FaceRecognitionModule(root)
    root.mainloop()


# import tkinter as tk
# from tkinter import ttk, messagebox
# import cv2
# from PIL import Image, ImageTk
# import numpy as np
# import os
# from datetime import datetime
# import csv

# # Import ID card scanner
# try:
#     from id_card_scanner_module import EnhancedIDCardScanner
#     ID_SCANNER_AVAILABLE = True
# except ImportError:
#     ID_SCANNER_AVAILABLE = False
#     print("Warning: ID card scanner module not found.")

# # Import liveness detection
# try:
#     from liveness_detection_module import LivenessIntegration
#     LIVENESS_AVAILABLE = True
# except ImportError:
#     LIVENESS_AVAILABLE = False

# class FaceRecognitionWithIDCard:
#     def __init__(self, parent):
#         self.parent = parent
#         self.window = tk.Toplevel(parent)
#         self.window.title("Face Recognition + ID Card Verification")
#         self.window.geometry("1400x900")
#         self.window.configure(bg='#0a0a2e')
#         self.window.state('zoomed')
        
#         self.window.transient(parent)
#         self.window.grab_set()
        
#         # Initialize components
#         self.face_cascade = cv2.CascadeClassifier(
#             cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
#         )
#         self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
#         # Video capture
#         self.cap = None
#         self.is_running = False
        
#         # Recognition variables
#         self.recognized_students = set()
#         self.confidence_threshold = 50
        
#         # ID Card Scanner
#         if ID_SCANNER_AVAILABLE:
#             self.id_scanner = EnhancedIDCardScanner()
#             self.id_verification_enabled = True
#         else:
#             self.id_scanner = None
#             self.id_verification_enabled = False
        
#         # Liveness detection
#         if LIVENESS_AVAILABLE:
#             self.liveness = LivenessIntegration()
#             self.liveness_enabled = True
#         else:
#             self.liveness = None
#             self.liveness_enabled = False
        
#         # Verification state
#         self.current_verification_state = "FACE"  # FACE -> ID_CARD -> COMPLETE
#         self.pending_verification = {}  # Store pending verifications
        
#         # Load trained model
#         self.load_trained_model()
        
#         self.create_ui()
        
#         self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
#     def create_ui(self):
#         # Main container
#         main_container = tk.Frame(self.window, bg='#0a0a2e')
#         main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
#         # Title
#         title_text = "FACE RECOGNITION + ID CARD VERIFICATION SYSTEM"
#         title_label = tk.Label(main_container, text=title_text,
#                               fg='#00ffff', bg='#0a0a2e', 
#                               font=('Arial', 20, 'bold'))
#         title_label.pack(pady=(0, 15))
        
#         # Content frame
#         content_frame = tk.Frame(main_container, bg='#0a0a2e')
#         content_frame.pack(fill='both', expand=True)
        
#         # Left panel - Video feed
#         self.create_video_panel(content_frame)
        
#         # Right panel - Controls
#         self.create_control_panel(content_frame)
        
#         # Bottom panel - Recognized students
#         self.create_recognition_panel(main_container)
    
#     def create_video_panel(self, parent):
#         video_frame = tk.LabelFrame(parent, text="Live Camera Feed",
#                                    font=('Arial', 14, 'bold'), bg='#16213e',
#                                    fg='#00ffff', bd=2, relief='raised')
#         video_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
#         # Video display
#         self.video_label = tk.Label(video_frame, bg='black')
#         self.video_label.pack(padx=10, pady=10, fill='both', expand=True)
        
#         # Status container
#         status_container = tk.Frame(video_frame, bg='#16213e')
#         status_container.pack(pady=5)
        
#         # Camera status
#         self.status_label = tk.Label(status_container, 
#                                     text="Camera Status: OFF",
#                                     fg='#ff6b6b', bg='#16213e',
#                                     font=('Arial', 12, 'bold'))
#         self.status_label.pack()
        
#         # Verification step indicator
#         self.verification_step_label = tk.Label(status_container,
#                                                text="",
#                                                fg='#00ffff', bg='#16213e',
#                                                font=('Arial', 11, 'bold'))
#         self.verification_step_label.pack(pady=5)
        
#         # Instructions
#         self.instruction_label = tk.Label(status_container,
#                                          text="",
#                                          fg='yellow', bg='#16213e',
#                                          font=('Arial', 10))
#         self.instruction_label.pack(pady=5)
    
#     def create_control_panel(self, parent):
#         control_frame = tk.LabelFrame(parent, text="Controls & Settings",
#                                      font=('Arial', 14, 'bold'), bg='#16213e',
#                                      fg='#00ffff', bd=2, relief='raised')
#         control_frame.pack(side='right', fill='both')
        
#         # Time display
#         time_frame = tk.Frame(control_frame, bg='#16213e')
#         time_frame.pack(fill='x', padx=10, pady=10)
        
#         self.time_label = tk.Label(time_frame, text="", fg='#00ffff',
#                                   bg='#16213e', font=('Arial', 14, 'bold'))
#         self.time_label.pack()
#         self.update_time()
        
#         # Camera controls
#         tk.Label(control_frame, text="Camera Controls",
#                 font=('Arial', 12, 'bold'), fg='white', 
#                 bg='#16213e').pack(pady=(10, 5))
        
#         self.start_btn = tk.Button(control_frame, text="▶ START CAMERA",
#                                   bg='#2ecc71', fg='white',
#                                   font=('Arial', 12, 'bold'),
#                                   width=20, height=2,
#                                   command=self.start_camera)
#         self.start_btn.pack(pady=5, padx=10)
        
#         self.stop_btn = tk.Button(control_frame, text="■ STOP CAMERA",
#                                  bg='#e74c3c', fg='white',
#                                  font=('Arial', 12, 'bold'),
#                                  width=20, height=2,
#                                  command=self.stop_camera,
#                                  state='disabled')
#         self.stop_btn.pack(pady=5, padx=10)
        
#         # Settings
#         tk.Label(control_frame, text="Verification Settings",
#                 font=('Arial', 12, 'bold'), fg='white', 
#                 bg='#16213e').pack(pady=(20, 5))
        
#         # Confidence threshold
#         threshold_frame = tk.Frame(control_frame, bg='#16213e')
#         threshold_frame.pack(fill='x', padx=10, pady=5)
        
#         tk.Label(threshold_frame, text="Confidence:",
#                 fg='white', bg='#16213e').pack(side='left')
        
#         self.threshold_var = tk.IntVar(value=50)
#         threshold_scale = tk.Scale(threshold_frame, from_=0, to=100,
#                                   orient='horizontal', 
#                                   variable=self.threshold_var,
#                                   bg='#16213e', fg='white', 
#                                   highlightthickness=0,
#                                   command=self.update_threshold)
#         threshold_scale.pack(side='left', fill='x', expand=True, padx=5)
        
#         self.threshold_label = tk.Label(threshold_frame, text="50%",
#                                        fg='#00ffff', bg='#16213e',
#                                        font=('Arial', 10, 'bold'))
#         self.threshold_label.pack(side='left')
        
#         # Feature toggles
#         toggles_frame = tk.Frame(control_frame, bg='#16213e')
#         toggles_frame.pack(fill='x', padx=10, pady=10)
        
#         # ID verification toggle
#         if ID_SCANNER_AVAILABLE:
#             self.id_verify_var = tk.BooleanVar(value=True)
#             tk.Checkbutton(toggles_frame, 
#                           text="✓ ID Card Verification",
#                           variable=self.id_verify_var,
#                           bg='#16213e', fg='white',
#                           selectcolor='#2c3e50',
#                           font=('Arial', 10, 'bold'),
#                           command=self.toggle_id_verification).pack(anchor='w')
        
#         # Liveness detection toggle
#         if LIVENESS_AVAILABLE:
#             self.liveness_var = tk.BooleanVar(value=True)
#             tk.Checkbutton(toggles_frame,
#                           text="✓ Liveness Detection",
#                           variable=self.liveness_var,
#                           bg='#16213e', fg='white',
#                           selectcolor='#2c3e50',
#                           font=('Arial', 10),
#                           command=self.toggle_liveness).pack(anchor='w')
        
#         # Statistics
#         tk.Label(control_frame, text="Statistics",
#                 font=('Arial', 12, 'bold'), fg='white', 
#                 bg='#16213e').pack(pady=(20, 5))
        
#         stats_frame = tk.Frame(control_frame, bg='#16213e')
#         stats_frame.pack(fill='x', padx=10, pady=5)
        
#         self.faces_detected_label = tk.Label(stats_frame, 
#                                             text="Faces: 0",
#                                             fg='white', bg='#16213e',
#                                             font=('Arial', 10))
#         self.faces_detected_label.pack(anchor='w', pady=2)
        
#         self.recognized_count_label = tk.Label(stats_frame, 
#                                               text="Verified: 0",
#                                               fg='#2ecc71', bg='#16213e',
#                                               font=('Arial', 10))
#         self.recognized_count_label.pack(anchor='w', pady=2)
        
#         self.pending_label = tk.Label(stats_frame,
#                                      text="Pending ID Scan: 0",
#                                      fg='#f39c12', bg='#16213e',
#                                      font=('Arial', 10))
#         self.pending_label.pack(anchor='w', pady=2)
        
#         # Actions
#         tk.Label(control_frame, text="Actions",
#                 font=('Arial', 12, 'bold'), fg='white', 
#                 bg='#16213e').pack(pady=(20, 5))
        
#         tk.Button(control_frame, text="📊 View Attendance",
#                  bg='#3498db', fg='white',
#                  font=('Arial', 10, 'bold'),
#                  width=20, height=2,
#                  command=self.view_attendance).pack(pady=5, padx=10)
        
#         tk.Button(control_frame, text="🔄 Reset Session",
#                  bg='#f39c12', fg='white',
#                  font=('Arial', 10, 'bold'),
#                  width=20, height=2,
#                  command=self.reset_session).pack(pady=5, padx=10)
    
#     def create_recognition_panel(self, parent):
#         recognition_frame = tk.LabelFrame(parent, 
#                                         text="Verified Students (Today)",
#                                         font=('Arial', 14, 'bold'), 
#                                         bg='#16213e',
#                                         fg='#00ffff', bd=2, relief='raised')
#         recognition_frame.pack(fill='both', expand=True, pady=(15, 0))
        
#         # Columns
#         columns = ["ID", "Name", "Time", "Face Conf", 
#                    "ID Verified", "Status"]
#         if LIVENESS_AVAILABLE:
#             columns.insert(4, "Liveness")
        
#         self.tree = ttk.Treeview(recognition_frame, columns=columns,
#                                 show='headings', height=8)
        
#         # Define headings
#         for col in columns:
#             self.tree.heading(col, text=col)
        
#         # Column widths
#         self.tree.column("ID", width=80)
#         self.tree.column("Name", width=180)
#         self.tree.column("Time", width=100)
#         self.tree.column("Face Conf", width=90)
#         if LIVENESS_AVAILABLE:
#             self.tree.column("Liveness", width=90)
#         self.tree.column("ID Verified", width=90)
#         self.tree.column("Status", width=100)
        
#         # Scrollbar
#         scrollbar = ttk.Scrollbar(recognition_frame, orient="vertical",
#                                  command=self.tree.yview)
#         self.tree.configure(yscrollcommand=scrollbar.set)
        
#         self.tree.pack(side='left', fill='both', expand=True, 
#                       padx=10, pady=10)
#         scrollbar.pack(side='right', fill='y', pady=10)
        
#         # Style
#         style = ttk.Style()
#         style.configure("Treeview", background="#2c3e50", 
#                        foreground="white",
#                        fieldbackground="#2c3e50", font=('Arial', 9))
#         style.configure("Treeview.Heading", background="#34495e",
#                        foreground="white", font=('Arial', 10, 'bold'))
    
#     def update_time(self):
#         current_time = datetime.now().strftime("%H:%M:%S %p • %d/%m/%Y")
#         self.time_label.config(text=current_time)
#         if self.window.winfo_exists():
#             self.window.after(1000, self.update_time)
    
#     def update_threshold(self, value):
#         self.confidence_threshold = int(float(value))
#         self.threshold_label.config(text=f"{self.confidence_threshold}%")
    
#     def toggle_id_verification(self):
#         if self.id_scanner:
#             self.id_verification_enabled = self.id_verify_var.get()
    
#     def toggle_liveness(self):
#         if self.liveness:
#             self.liveness_enabled = self.liveness_var.get()
#             self.liveness.enable_liveness(self.liveness_enabled)
    
#     def load_trained_model(self):
#         model_path = "trainer/trainer.yml"
#         if os.path.exists(model_path):
#             try:
#                 self.recognizer.read(model_path)
#                 msg = "Trained model loaded successfully!"
#                 if ID_SCANNER_AVAILABLE:
#                     msg += "\n\n✓ ID Card Verification ENABLED"
#                 if LIVENESS_AVAILABLE:
#                     msg += "\n✓ Liveness Detection ENABLED"
#                 messagebox.showinfo("Success", msg)
#             except Exception as e:
#                 messagebox.showwarning("Warning", 
#                     f"Could not load model: {str(e)}")
#         else:
#             messagebox.showwarning("Warning", 
#                 "No trained model found. Train the model first.")
    
#     def start_camera(self):
#         try:
#             self.cap = cv2.VideoCapture(0)
#             if not self.cap.isOpened():
#                 messagebox.showerror("Error", "Could not open camera!")
#                 return
            
#             self.is_running = True
#             self.start_btn.config(state='disabled')
#             self.stop_btn.config(state='normal')
#             self.status_label.config(text="Camera Status: ACTIVE", 
#                                     fg='#2ecc71')
            
#             if self.liveness:
#                 self.liveness.reset_detector()
            
#             self.process_video()
            
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
    
#     def stop_camera(self):
#         self.is_running = False
#         if self.cap is not None:
#             self.cap.release()
        
#         self.start_btn.config(state='normal')
#         self.stop_btn.config(state='disabled')
#         self.status_label.config(text="Camera Status: OFF", fg='#ff6b6b')
#         self.video_label.config(image='', bg='black')
#         self.verification_step_label.config(text="")
#         self.instruction_label.config(text="")
    
#     def process_video(self):
#         if not self.is_running:
#             return
        
#         ret, frame = self.cap.read()
#         if ret:
#             frame = self.process_frame(frame)
            
#             # Display
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             img = Image.fromarray(frame_rgb)
#             img = img.resize((800, 600), Image.Resampling.LANCZOS)
#             photo = ImageTk.PhotoImage(image=img)
            
#             self.video_label.config(image=photo)
#             self.video_label.image = photo
        
#         if self.is_running:
#             self.window.after(10, self.process_video)
    
#     def process_frame(self, frame):
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
#         self.faces_detected_label.config(text=f"Faces: {len(faces)}")
#         verified = len(self.recognized_students)
#         self.recognized_count_label.config(text=f"Verified: {verified}")
#         pending = len(self.pending_verification)
#         self.pending_label.config(text=f"Pending ID Scan: {pending}")
        
#         # Update verification step display
#         if pending > 0:
#             self.verification_step_label.config(
#                 text="⚠️ STEP 2: Show ID Card to Camera",
#                 fg='#f39c12'
#             )
#             self.instruction_label.config(
#                 text="Hold ID card steady in front of camera"
#             )
#         else:
#             self.verification_step_label.config(
#                 text="STEP 1: Face Recognition",
#                 fg='#00ffff'
#             )
#             self.instruction_label.config(
#                 text="Position your face in frame"
#             )
        
#         # Check if we're in ID scanning mode
#         if len(self.pending_verification) > 0:
#             # Try to detect ID card
#             if self.id_scanner and self.id_verification_enabled:
#                 frame = self.process_id_card(frame)
#         else:
#             # Process face recognition
#             frame = self.process_face_recognition(frame, gray, faces)
        
#         return frame
    
#     def process_face_recognition(self, frame, gray, faces):
#         for (x, y, w, h) in faces:
#             roi_gray = gray[y:y+h, x:x+w]
            
#             try:
#                 id_, confidence = self.recognizer.predict(roi_gray)
                
#                 if confidence < 100 - self.confidence_threshold:
#                     name = self.get_student_name(id_)
#                     confidence_text = f"{round(100 - confidence)}%"
                    
#                     # Check if already verified
#                     if id_ in self.recognized_students:
#                         color = (128, 128, 128)  # Gray - already done
#                         cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
#                         cv2.putText(frame, "Already Verified", (x, y-10),
#                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
#                         continue
                    
#                     # Liveness check
#                     liveness_passed = True
#                     liveness_status = "N/A"
                    
#                     if self.liveness_enabled and self.liveness:
#                         frame, liveness_passed, liveness_info = \
#                             self.liveness.process_frame_with_liveness(
#                                 frame, [(x, y, w, h)], self.recognizer, 
#                                 id_, confidence
#                             )
#                         liveness_status = liveness_info['status']
                        
#                         if not liveness_passed:
#                             continue
                    
#                     # Face recognized and liveness passed
#                     if self.id_verification_enabled:
#                         # Add to pending verification
#                         if id_ not in self.pending_verification:
#                             self.pending_verification[id_] = {
#                                 'name': name,
#                                 'confidence': confidence_text,
#                                 'liveness_status': liveness_status,
#                                 'timestamp': datetime.now()
#                             }
                            
#                             color = (255, 165, 0)  # Orange - pending ID
#                             cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
#                             cv2.putText(frame, f"{name} - Show ID Card", 
#                                       (x, y-10),
#                                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
#                     else:
#                         # No ID verification required - mark attendance
#                         self.mark_attendance(id_, name, confidence_text, 
#                                            liveness_status, "No ID Check")
#                         self.recognized_students.add(id_)
                        
#                         color = (0, 255, 0)  # Green
#                         cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
#                         cv2.putText(frame, f"{name} - Verified", (x, y-10),
#                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
#                 else:
#                     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
#                     cv2.putText(frame, "Unknown", (x, y-10),
#                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
#             except Exception as e:
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
#                 cv2.putText(frame, "Unknown", (x, y-10),
#                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
#         return frame
    
#     def process_id_card(self, frame):
#         # Try to detect and verify ID card
#         card_rect, card_img, detect_score = \
#             self.id_scanner.detect_id_card_advanced(frame)
        
#         if card_rect and card_img is not None:
#             # Extract text from ID card
#             text = self.id_scanner.extract_text_advanced(card_img)
#             scanned_data = self.id_scanner.parse_smit_id_card(text)
            
#             # Try to match with pending verifications
#             for student_id, pending_data in list(self.pending_verification.items()):
#                 expected_name = pending_data['name']
                
#                 # Verify ID card
#                 match, id_confidence, details = \
#                     self.id_scanner.verify_with_database(
#                         scanned_data, student_id, expected_name
#                     )
                
#                 if match:
#                     # ID verified! Mark attendance
#                     self.mark_attendance(
#                         student_id,
#                         expected_name,
#                         pending_data['confidence'],
#                         pending_data.get('liveness_status', 'N/A'),
#                         f"ID Verified ({id_confidence}%)"
#                     )
                    
#                     # Remove from pending
#                     del self.pending_verification[student_id]
#                     self.recognized_students.add(student_id)
                    
#                     # Draw success
#                     frame = self.id_scanner.draw_enhanced_detection(
#                         frame, card_rect, scanned_data, 
#                         'verified', id_confidence
#                     )
                    
#                     messagebox.showinfo("Verified!", 
#                         f"✓ {expected_name} verified successfully!\n\n"
#                         f"Face Confidence: {pending_data['confidence']}\n"
#                         f"ID Confidence: {id_confidence}%")
                    
#                     break
#                 else:
#                     # ID didn't match
#                     frame = self.id_scanner.draw_enhanced_detection(
#                         frame, card_rect, scanned_data, 
#                         'failed', id_confidence
#                     )
        
#         return frame
    
#     def get_student_name(self, student_id):
#         try:
#             with open('student_data/students.csv', 'r', 
#                      encoding='utf-8', errors='ignore') as file:
#                 reader = csv.DictReader(file)
#                 for row in reader:
#                     try:
#                         if int(row['StudentID']) == student_id:
#                             name = row['Name']
#                             name = name.encode('ascii', 'ignore').decode('ascii')
#                             return name if name else f"Student_{student_id}"
#                     except (ValueError, KeyError):
#                         continue
#         except Exception as e:
#             print(f"Error reading student name: {e}")
        
#         return f"Student_{student_id}"
    
#     def mark_attendance(self, student_id, name, face_confidence, 
#                        liveness_status, id_status):
#         current_time = datetime.now().strftime("%H:%M:%S")
        
#         # Prepare values
#         values = [student_id, name, current_time, face_confidence]
#         if LIVENESS_AVAILABLE:
#             values.append(liveness_status)
#         values.append(id_status)
#         values.append("✓ Verified")
        
#         # Add to treeview
#         self.tree.insert("", 0, values=tuple(values))
        
#         # Save to file
#         self.save_attendance(student_id, name, current_time, 
#                            face_confidence, liveness_status, id_status)
    
#     def save_attendance(self, student_id, name, time, face_conf, 
#                        liveness_status, id_status):
#         date = datetime.now().strftime("%Y-%m-%d")
#         filename = f"attendance/attendance_{date}.csv"
#         os.makedirs("attendance", exist_ok=True)
        
#         file_exists = os.path.isfile(filename)
        
#         try:
#             clean_name = str(name).encode('ascii', 'ignore').decode('ascii')
#             if not clean_name:
#                 clean_name = f"Student_{student_id}"
            
#             with open(filename, 'a', newline='', encoding='utf-8', 
#                      errors='replace') as file:
#                 fieldnames = ['StudentID', 'Name', 'Time', 
#                             'FaceConfidence', 'Date', 'Status']
                
#                 if LIVENESS_AVAILABLE:
#                     fieldnames.append('LivenessStatus')
#                 if ID_SCANNER_AVAILABLE:
#                     fieldnames.append('IDVerification')
                
#                 writer = csv.DictWriter(file, fieldnames=fieldnames)
                
#                 if not file_exists:
#                     writer.writeheader()
                
#                 row_data = {
#                     'StudentID': str(student_id),
#                     'Name': clean_name,
#                     'Time': time,
#                     'FaceConfidence': face_conf,
#                     'Date': date,
#                     'Status': 'Present'
#                 }
                
#                 if LIVENESS_AVAILABLE:
#                     row_data['LivenessStatus'] = liveness_status
#                 if ID_SCANNER_AVAILABLE:
#                     row_data['IDVerification'] = id_status
                
#                 writer.writerow(row_data)
                
#         except Exception as e:
#             print(f"Error saving attendance: {e}")
    
#     def view_attendance(self):
#         msg = f"Total students verified: {len(self.recognized_students)}\n"
#         msg += f"Pending ID verification: {len(self.pending_verification)}"
#         messagebox.showinfo("Attendance", msg)
    
#     def reset_session(self):
#         if messagebox.askyesno("Confirm", "Reset current session?"):
#             self.recognized_students.clear()
#             self.pending_verification.clear()
#             self.tree.delete(*self.tree.get_children())
            
#             if self.liveness:
#                 self.liveness.reset_detector()
#                 self.liveness.clear_results()
            
#             messagebox.showinfo("Success", "Session reset successfully!")
    
#     def on_closing(self):
#         self.stop_camera()
#         self.window.destroy()


# if __name__ == "__main__":
#     root = tk.Tk()
#     root.withdraw()
#     app = FaceRecognitionWithIDCard(root)
#     root.mainloop()
# FaceRecognitionModule = FaceRecognitionWithIDCard