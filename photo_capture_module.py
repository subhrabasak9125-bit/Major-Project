import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import os
from datetime import datetime

class PhotoCaptureModule:
    def __init__(self, parent, student_id=None, student_name=None):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Photo Sample Capture")
        self.window.geometry("1000x700")
        self.window.configure(bg='#0a0a2e')
        
        self.window.transient(parent)
        self.window.grab_set()
        
        # Student info
        self.student_id = student_id
        self.student_name = student_name or f"Student_{student_id}"
        
        # Capture variables
        self.cap = None
        self.is_running = False
        self.photo_count = 0
        self.max_photos = 100
        
        # Face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Create data directory
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.create_ui()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_ui(self):
        # Main container
        main_container = tk.Frame(self.window, bg='#0a0a2e')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_container, text="PHOTO SAMPLE CAPTURE",
                              fg='#00ffff', bg='#0a0a2e', font=('Arial', 24, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Student info
        info_frame = tk.Frame(main_container, bg='#16213e', bd=2, relief='raised')
        info_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(info_frame, text=f"Student ID: {self.student_id}",
                fg='white', bg='#16213e', font=('Arial', 14, 'bold')).pack(side='left', padx=20, pady=10)
        
        tk.Label(info_frame, text=f"Name: {self.student_name}",
                fg='white', bg='#16213e', font=('Arial', 14, 'bold')).pack(side='left', padx=20, pady=10)
        
        # Content frame
        content_frame = tk.Frame(main_container, bg='#0a0a2e')
        content_frame.pack(fill='both', expand=True)
        
        # Left panel - Video feed
        video_frame = tk.LabelFrame(content_frame, text="Camera Feed",
                                   font=('Arial', 14, 'bold'), bg='#16213e',
                                   fg='#00ffff', bd=2, relief='raised')
        video_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Video display
        self.video_label = tk.Label(video_frame, bg='black')
        self.video_label.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Instructions
        instructions = """
        Position your face in the center of the frame.
        The system will automatically capture photos when a face is detected.
        Try different angles and expressions for better recognition.
        """
        tk.Label(video_frame, text=instructions, fg='white', bg='#16213e',
                font=('Arial', 10), justify='left').pack(padx=10, pady=5)
        
        # Right panel - Controls
        control_frame = tk.LabelFrame(content_frame, text="Capture Controls",
                                     font=('Arial', 14, 'bold'), bg='#16213e',
                                     fg='#00ffff', bd=2, relief='raised')
        control_frame.pack(side='right', fill='both')
        
        # Progress section
        tk.Label(control_frame, text="Capture Progress",
                font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(20, 10))
        
        self.progress_label = tk.Label(control_frame, text=f"0 / {self.max_photos}",
                                      fg='#00ffff', bg='#16213e',
                                      font=('Arial', 20, 'bold'))
        self.progress_label.pack(pady=10)
        
        self.progress_bar = ttk.Progressbar(control_frame, length=200,
                                           mode='determinate', maximum=self.max_photos)
        self.progress_bar.pack(pady=10, padx=20)
        
        # Status
        self.status_label = tk.Label(control_frame, text="Status: Ready",
                                    fg='#2ecc71', bg='#16213e',
                                    font=('Arial', 12, 'bold'))
        self.status_label.pack(pady=20)
        
        # Capture settings
        tk.Label(control_frame, text="Settings",
                font=('Arial', 12, 'bold'), fg='white', bg='#16213e').pack(pady=(20, 10))
        
        settings_frame = tk.Frame(control_frame, bg='#16213e')
        settings_frame.pack(padx=20, pady=10)
        
        tk.Label(settings_frame, text="Sample Count:",
                fg='white', bg='#16213e').grid(row=0, column=0, sticky='w', pady=5)
        
        self.sample_count_var = tk.IntVar(value=100)
        sample_spinbox = tk.Spinbox(settings_frame, from_=50, to=200,
                                   textvariable=self.sample_count_var,
                                   width=10)
        sample_spinbox.grid(row=0, column=1, padx=10, pady=5)
        
        # Apply button for settings
        tk.Button(settings_frame, text="Apply", bg='#3498db', fg='white',
                 command=self.apply_settings).grid(row=0, column=2, padx=5, pady=5)
        
        # Control buttons
        button_container = tk.Frame(control_frame, bg='#16213e')
        button_container.pack(pady=30, padx=20)
        
        self.start_btn = tk.Button(button_container, text="▶ START CAPTURE",
                                  bg='#2ecc71', fg='white',
                                  font=('Arial', 12, 'bold'),
                                  width=20, height=2,
                                  command=self.start_capture)
        self.start_btn.pack(pady=5)
        
        self.stop_btn = tk.Button(button_container, text="⏹ STOP CAPTURE",
                                 bg='#e74c3c', fg='white',
                                 font=('Arial', 12, 'bold'),
                                 width=20, height=2,
                                 command=self.stop_capture,
                                 state='disabled')
        self.stop_btn.pack(pady=5)
        
        tk.Button(button_container, text="🚪 CLOSE",
                 bg='#95a5a6', fg='white',
                 font=('Arial', 12, 'bold'),
                 width=20, height=2,
                 command=self.on_closing).pack(pady=5)
        
        # Statistics
        stats_frame = tk.LabelFrame(control_frame, text="Statistics",
                                   font=('Arial', 11, 'bold'), bg='#16213e',
                                   fg='#00ffff')
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        self.faces_detected_label = tk.Label(stats_frame, text="Faces Detected: 0",
                                            fg='white', bg='#16213e',
                                            font=('Arial', 10))
        self.faces_detected_label.pack(anchor='w', padx=10, pady=5)
        
        self.last_capture_label = tk.Label(stats_frame, text="Last Capture: --",
                                          fg='white', bg='#16213e',
                                          font=('Arial', 10))
        self.last_capture_label.pack(anchor='w', padx=10, pady=5)
    
    def apply_settings(self):
        """Apply capture settings"""
        self.max_photos = self.sample_count_var.get()
        self.progress_bar.config(maximum=self.max_photos)
        self.progress_label.config(text=f"{self.photo_count} / {self.max_photos}")
        messagebox.showinfo("Settings", f"Sample count updated to {self.max_photos}")
    
    def start_capture(self):
        """Start camera and photo capture"""
        if self.student_id is None:
            messagebox.showerror("Error", "No student ID provided!")
            return
        
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open camera!")
                return
            
            self.is_running = True
            self.photo_count = 0
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.status_label.config(text="Status: Capturing...", fg='#f39c12')
            
            self.process_capture()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
    
    def stop_capture(self):
        """Stop camera and capture"""
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
        
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_label.config(text="Status: Stopped", fg='#e74c3c')
        self.video_label.config(image='', bg='black')
        
        if self.photo_count > 0:
            messagebox.showinfo("Capture Complete", 
                f"Captured {self.photo_count} photos successfully!\n\nYou can now train the model.")
    
    def process_capture(self):
        """Process video frames and capture photos"""
        if not self.is_running or self.photo_count >= self.max_photos:
            if self.photo_count >= self.max_photos:
                self.stop_capture()
                messagebox.showinfo("Complete", 
                    f"Capture complete! {self.photo_count} photos saved.\n\nPlease train the model now.")
            return
        
        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            self.faces_detected_label.config(text=f"Faces Detected: {len(faces)}")
            
            for (x, y, w, h) in faces:
                # Draw rectangle
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Save face image
                if self.photo_count < self.max_photos:
                    face_img = gray[y:y+h, x:x+w]
                    
                    # Save with format: User.StudentID.PhotoNumber.jpg
                    filename = f"User.{self.student_id}.{self.photo_count + 1}.jpg"
                    filepath = os.path.join(self.data_dir, filename)
                    
                    cv2.imwrite(filepath, face_img)
                    
                    self.photo_count += 1
                    self.progress_bar['value'] = self.photo_count
                    self.progress_label.config(text=f"{self.photo_count} / {self.max_photos}")
                    
                    current_time = datetime.now().strftime("%H:%M:%S")
                    self.last_capture_label.config(text=f"Last Capture: {current_time}")
                
                # Display count on frame
                cv2.putText(frame, f"Captured: {self.photo_count}/{self.max_photos}",
                          (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # Convert and display frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img = img.resize((640, 480), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image=img)
            
            self.video_label.config(image=photo)
            self.video_label.image = photo
        
        if self.is_running:
            self.window.after(50, self.process_capture)  # Capture every 50ms
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            self.stop_capture()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    # Test with sample data
    app = PhotoCaptureModule(root, student_id=1, student_name="Test Student")
    root.mainloop()