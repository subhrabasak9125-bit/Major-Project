import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np
import os
from datetime import datetime
import csv

class FaceRecognitionModule:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Face Recognition System")
        self.window.geometry("1200x800")
        self.window.configure(bg='#0a0a2e')
        self.window.state('zoomed')
        
        # Center the window
        self.window.transient(parent)
        self.window.grab_set()
        
        # Initialize face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Video capture
        self.cap = None
        self.is_running = False
        
        # Recognition variables
        self.recognized_students = set()
        self.confidence_threshold = 50
        
        # Load trained model if exists
        self.load_trained_model()
        
        self.create_ui()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_ui(self):
        # Main container
        main_container = tk.Frame(self.window, bg='#0a0a2e')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_container, text="FACE RECOGNITION ATTENDANCE SYSTEM",
                              fg='#00ffff', bg='#0a0a2e', font=('Arial', 24, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Content frame
        content_frame = tk.Frame(main_container, bg='#0a0a2e')
        content_frame.pack(fill='both', expand=True)
        
        # Left panel - Video feed
        self.create_video_panel(content_frame)
        
        # Right panel - Controls and info
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
        
        # Status label
        self.status_label = tk.Label(video_frame, text="Camera Status: OFF",
                                    fg='#ff6b6b', bg='#16213e',
                                    font=('Arial', 12, 'bold'))
        self.status_label.pack(pady=5)
    
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
        
        # Recognition settings
        tk.Label(control_frame, text="Recognition Settings",
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
        
        # Statistics
        tk.Label(control_frame, text="Statistics",
                font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(20, 5))
        
        stats_frame = tk.Frame(control_frame, bg='#16213e')
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        self.faces_detected_label = tk.Label(stats_frame, text="Faces Detected: 0",
                                            fg='white', bg='#16213e',
                                            font=('Arial', 10))
        self.faces_detected_label.pack(anchor='w', pady=2)
        
        self.recognized_count_label = tk.Label(stats_frame, text="Recognized: 0",
                                              fg='#2ecc71', bg='#16213e',
                                              font=('Arial', 10))
        self.recognized_count_label.pack(anchor='w', pady=2)
        
        self.unknown_count_label = tk.Label(stats_frame, text="Unknown: 0",
                                           fg='#e74c3c', bg='#16213e',
                                           font=('Arial', 10))
        self.unknown_count_label.pack(anchor='w', pady=2)
        
        # Action buttons
        tk.Label(control_frame, text="Actions",
                font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(20, 5))
        
        tk.Button(control_frame, text="📊 View Attendance",
                 bg='#3498db', fg='white',
                 font=('Arial', 10, 'bold'),
                 width=20, height=2,
                 command=self.view_attendance).pack(pady=5, padx=10)
        
        tk.Button(control_frame, text="🔄 Reset Session",
                 bg='#f39c12', fg='white',
                 font=('Arial', 10, 'bold'),
                 width=20, height=2,
                 command=self.reset_session).pack(pady=5, padx=10)
        
        tk.Button(control_frame, text="💾 Export Attendance",
                 bg='#9b59b6', fg='white',
                 font=('Arial', 10, 'bold'),
                 width=20, height=2,
                 command=self.export_attendance).pack(pady=5, padx=10)
    
    def create_recognition_panel(self, parent):
        recognition_frame = tk.LabelFrame(parent, text="Recognized Students (Today)",
                                        font=('Arial', 14, 'bold'), bg='#16213e',
                                        fg='#00ffff', bd=2, relief='raised')
        recognition_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        # Create treeview
        columns = ("ID", "Name", "Time", "Confidence", "Status")
        self.tree = ttk.Treeview(recognition_frame, columns=columns,
                                show='headings', height=8)
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
        
        # Define column widths
        self.tree.column("ID", width=100)
        self.tree.column("Name", width=200)
        self.tree.column("Time", width=150)
        self.tree.column("Confidence", width=100)
        self.tree.column("Status", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(recognition_frame, orient="vertical",
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", background="#2c3e50", foreground="white",
                       fieldbackground="#2c3e50")
        style.configure("Treeview.Heading", background="#34495e",
                       foreground="white", font=('Arial', 10, 'bold'))
    
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S %p - %d/%m/%Y")
        self.time_label.config(text=current_time)
        if self.window.winfo_exists():
            self.window.after(1000, self.update_time)
    
    def update_threshold(self, value):
        self.confidence_threshold = int(float(value))
        self.threshold_label.config(text=f"{self.confidence_threshold}%")
    
    def load_trained_model(self):
        """Load the trained face recognition model"""
        model_path = "trainer/trainer.yml"
        if os.path.exists(model_path):
            try:
                self.recognizer.read(model_path)
                messagebox.showinfo("Success", "Trained model loaded successfully!")
            except Exception as e:
                messagebox.showwarning("Warning", 
                    f"Could not load model: {str(e)}\nPlease train the model first.")
        else:
            messagebox.showwarning("Warning", 
                "No trained model found. Please train the model first from the main menu.")
    
    def start_camera(self):
        """Start the camera and face recognition"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open camera!")
                return
            
            self.is_running = True
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.status_label.config(text="Camera Status: ACTIVE", fg='#2ecc71')
            
            self.process_video()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
    
    def stop_camera(self):
        """Stop the camera"""
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
        
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_label.config(text="Camera Status: OFF", fg='#ff6b6b')
        self.video_label.config(image='', bg='black')
    
    def process_video(self):
        """Process video frames for face recognition"""
        if not self.is_running:
            return
        
        ret, frame = self.cap.read()
        if ret:
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            faces_detected = len(faces)
            recognized = 0
            unknown = 0
            
            # Process each detected face
            for (x, y, w, h) in faces:
                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Try to recognize the face
                roi_gray = gray[y:y+h, x:x+w]
                
                try:
                    id_, confidence = self.recognizer.predict(roi_gray)
                    
                    # Check if confidence is good enough
                    if confidence < 100 - self.confidence_threshold:
                        # Load student name from file
                        name = self.get_student_name(id_)
                        confidence_text = f"{round(100 - confidence)}%"
                        
                        # Mark attendance
                        if id_ not in self.recognized_students:
                            self.mark_attendance(id_, name, confidence_text)
                            self.recognized_students.add(id_)
                        
                        recognized += 1
                        color = (0, 255, 0)  # Green
                    else:
                        name = "Unknown"
                        confidence_text = "Low"
                        unknown += 1
                        color = (0, 0, 255)  # Red
                    
                    # Display name and confidence
                    cv2.putText(frame, name, (x, y-10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                    cv2.putText(frame, confidence_text, (x, y+h+25),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    
                except Exception as e:
                    # If no model is loaded or error occurs
                    cv2.putText(frame, "Unknown", (x, y-10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    unknown += 1
            
            # Update statistics
            self.faces_detected_label.config(text=f"Faces Detected: {faces_detected}")
            self.recognized_count_label.config(text=f"Recognized: {recognized}")
            self.unknown_count_label.config(text=f"Unknown: {unknown}")
            
            # Convert frame to PhotoImage
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img = img.resize((640, 480), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image=img)
            
            self.video_label.config(image=photo)
            self.video_label.image = photo
        
        # Continue processing
        if self.is_running:
            self.window.after(10, self.process_video)
    
    def get_student_name(self, student_id):
        """Get student name from CSV file"""
        try:
            with open('student_data/students.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if int(row['StudentID']) == student_id:
                        return row['Name']
        except FileNotFoundError:
            pass
        return f"Student_{student_id}"
    
    def mark_attendance(self, student_id, name, confidence):
        """Mark attendance in the treeview and save to file"""
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Add to treeview
        self.tree.insert("", 0, values=(
            student_id,
            name,
            current_time,
            confidence,
            "Present"
        ))
        
        # Save to attendance file
        self.save_attendance(student_id, name, current_time, confidence)
    
    def save_attendance(self, student_id, name, time, confidence):
        """Save attendance to CSV file"""
        date = datetime.now().strftime("%Y-%m-%d")
        filename = f"attendance/attendance_{date}.csv"
        
        # Create directory if it doesn't exist
        os.makedirs("attendance", exist_ok=True)
        
        # Check if file exists
        file_exists = os.path.isfile(filename)
        
        try:
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file)
                
                # Write header if file is new
                if not file_exists:
                    writer.writerow(['StudentID', 'Name', 'Time', 'Confidence', 'Date'])
                
                # Write attendance record
                writer.writerow([student_id, name, time, confidence, date])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save attendance: {str(e)}")
    
    def view_attendance(self):
        """View today's attendance"""
        messagebox.showinfo("Attendance", 
            f"Total students marked present: {len(self.recognized_students)}")
    
    def reset_session(self):
        """Reset the current recognition session"""
        if messagebox.askyesno("Confirm", "Reset current session? This will clear recognized students."):
            self.recognized_students.clear()
            self.tree.delete(*self.tree.get_children())
            messagebox.showinfo("Success", "Session reset successfully!")
    
    def export_attendance(self):
        """Export attendance to file"""
        date = datetime.now().strftime("%Y-%m-%d")
        filename = f"attendance/attendance_{date}.csv"
        
        if os.path.exists(filename):
            messagebox.showinfo("Success", 
                f"Attendance exported to:\n{filename}")
        else:
            messagebox.showwarning("Warning", "No attendance records found for today.")
    
    def on_closing(self):
        """Handle window closing"""
        self.stop_camera()
        self.window.destroy()

if __name__ == "__main__":
    # Test the module
    root = tk.Tk()
    root.withdraw()
    app = FaceRecognitionModule(root)
    root.mainloop()