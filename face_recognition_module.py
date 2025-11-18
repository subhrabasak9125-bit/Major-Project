
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
    
    def on_closing(self):
        self.stop_camera()
        self.window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = FaceRecognitionModule(root)

    root.mainloop()
