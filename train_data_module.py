import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np
import os
from datetime import datetime

class TrainDataModule:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Train Face Recognition Model")
        self.window.geometry("1000x700")
        self.window.configure(bg='#0a0a2e')
        self.window.state('zoomed')
        
        self.window.transient(parent)
        self.window.grab_set()
        
        # Training variables
        self.is_training = False
        self.total_faces = 0
        self.processed_faces = 0
        
        self.create_ui()
    
    def create_ui(self):
        # Main container
        main_container = tk.Frame(self.window, bg='#0a0a2e')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_container, text="TRAIN FACE RECOGNITION MODEL",
                              fg='#00ffff', bg='#0a0a2e', font=('Arial', 24, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Info section
        info_frame = tk.LabelFrame(main_container, text="Training Information",
                                  font=('Arial', 14, 'bold'), bg='#16213e',
                                  fg='#00ffff', bd=2, relief='raised')
        info_frame.pack(fill='x', pady=(0, 20))
        
        info_text = """
        This module will train the face recognition model using the collected photo samples.
        
        Steps:
        1. Photo samples are loaded from the 'data' directory
        2. Faces are detected and processed
        3. The LBPH (Local Binary Patterns Histograms) model is trained
        4. The trained model is saved for recognition
        
        Note: Make sure you have collected photo samples before training.
        """
        
        tk.Label(info_frame, text=info_text, fg='white', bg='#16213e',
                font=('Arial', 11), justify='left').pack(padx=20, pady=20)
        
        # Statistics frame
        stats_frame = tk.LabelFrame(main_container, text="Training Statistics",
                                   font=('Arial', 14, 'bold'), bg='#16213e',
                                   fg='#00ffff', bd=2, relief='raised')
        stats_frame.pack(fill='x', pady=(0, 20))
        
        stats_inner = tk.Frame(stats_frame, bg='#16213e')
        stats_inner.pack(padx=20, pady=20)
        
        # Statistics labels
        self.students_label = tk.Label(stats_inner, text="Students Found: 0",
                                      fg='white', bg='#16213e',
                                      font=('Arial', 12, 'bold'))
        self.students_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
        
        self.images_label = tk.Label(stats_inner, text="Total Images: 0",
                                    fg='white', bg='#16213e',
                                    font=('Arial', 12, 'bold'))
        self.images_label.grid(row=0, column=1, padx=20, pady=10, sticky='w')
        
        self.faces_label = tk.Label(stats_inner, text="Faces Detected: 0",
                                   fg='white', bg='#16213e',
                                   font=('Arial', 12, 'bold'))
        self.faces_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')
        
        self.status_label = tk.Label(stats_inner, text="Status: Ready",
                                    fg='#2ecc71', bg='#16213e',
                                    font=('Arial', 12, 'bold'))
        self.status_label.grid(row=1, column=1, padx=20, pady=10, sticky='w')
        
        # Progress frame
        progress_frame = tk.LabelFrame(main_container, text="Training Progress",
                                      font=('Arial', 14, 'bold'), bg='#16213e',
                                      fg='#00ffff', bd=2, relief='raised')
        progress_frame.pack(fill='x', pady=(0, 20))
        
        progress_inner = tk.Frame(progress_frame, bg='#16213e')
        progress_inner.pack(padx=20, pady=20, fill='x')
        
        self.progress_bar = ttk.Progressbar(progress_inner, length=800,
                                           mode='determinate')
        self.progress_bar.pack(fill='x', pady=10)
        
        self.progress_label = tk.Label(progress_inner, text="0%",
                                      fg='#00ffff', bg='#16213e',
                                      font=('Arial', 12, 'bold'))
        self.progress_label.pack()
        
        # Log frame
        log_frame = tk.LabelFrame(main_container, text="Training Log",
                                 font=('Arial', 14, 'bold'), bg='#16213e',
                                 fg='#00ffff', bd=2, relief='raised')
        log_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Text widget for log
        self.log_text = tk.Text(log_frame, height=10, bg='#2c3e50',
                               fg='white', font=('Courier', 10))
        self.log_text.pack(padx=10, pady=10, fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        # Buttons frame
        button_frame = tk.Frame(main_container, bg='#0a0a2e')
        button_frame.pack(fill='x')
        
        self.scan_btn = tk.Button(button_frame, text="🔍 SCAN IMAGES",
                                 bg='#3498db', fg='white',
                                 font=('Arial', 12, 'bold'),
                                 width=20, height=2,
                                 command=self.scan_images)
        self.scan_btn.pack(side='left', padx=10)
        
        self.train_btn = tk.Button(button_frame, text="🧠 START TRAINING",
                                  bg='#2ecc71', fg='white',
                                  font=('Arial', 12, 'bold'),
                                  width=20, height=2,
                                  command=self.start_training,
                                  state='disabled')
        self.train_btn.pack(side='left', padx=10)
        
        tk.Button(button_frame, text="🚪 CLOSE",
                 bg='#e74c3c', fg='white',
                 font=('Arial', 12, 'bold'),
                 width=20, height=2,
                 command=self.window.destroy).pack(side='right', padx=10)
    
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert('end', f"[{timestamp}] {message}\n")
        self.log_text.see('end')
        self.window.update()
    
    def scan_images(self):
        """Scan for images in data directory"""
        self.log("Starting image scan...")
        
        data_dir = "data"
        if not os.path.exists(data_dir):
            messagebox.showerror("Error", "Data directory not found! Please collect photo samples first.")
            self.log("ERROR: Data directory not found!")
            return
        
        # Count students and images
        students = set()
        total_images = 0
        
        for filename in os.listdir(data_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                # Extract student ID from filename (assuming format: User.ID.ImageNum.jpg)
                parts = filename.split('.')
                if len(parts) >= 2:
                    students.add(parts[1])
                    total_images += 1
        
        self.students_label.config(text=f"Students Found: {len(students)}")
        self.images_label.config(text=f"Total Images: {total_images}")
        self.log(f"Found {len(students)} students with {total_images} images")
        
        if total_images > 0:
            self.train_btn.config(state='normal')
            self.log("Ready to start training!")
        else:
            messagebox.showwarning("Warning", "No images found! Please collect photo samples first.")
            self.log("WARNING: No images found!")
    
    def start_training(self):
        """Start the training process"""
        if self.is_training:
            return
        
        self.is_training = True
        self.train_btn.config(state='disabled')
        self.scan_btn.config(state='disabled')
        self.status_label.config(text="Status: Training...", fg='#f39c12')
        
        self.log("="*50)
        self.log("STARTING TRAINING PROCESS")
        self.log("="*50)
        
        try:
            # Initialize face detector
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Prepare data
            faces = []
            ids = []
            
            data_dir = "data"
            image_files = [f for f in os.listdir(data_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            self.total_faces = len(image_files)
            self.processed_faces = 0
            
            self.log(f"Processing {self.total_faces} images...")
            
            for filename in image_files:
                img_path = os.path.join(data_dir, filename)
                
                # Extract student ID from filename
                parts = filename.split('.')
                if len(parts) >= 2:
                    student_id = int(parts[1])
                    
                    # Load image
                    img = Image.open(img_path).convert('L')  # Convert to grayscale
                    img_np = np.array(img, 'uint8')
                    
                    # Detect faces
                    detected_faces = face_cascade.detectMultiScale(img_np)
                    
                    for (x, y, w, h) in detected_faces:
                        faces.append(img_np[y:y+h, x:x+w])
                        ids.append(student_id)
                
                self.processed_faces += 1
                progress = (self.processed_faces / self.total_faces) * 100
                self.progress_bar['value'] = progress
                self.progress_label.config(text=f"{int(progress)}%")
                self.window.update()
            
            self.faces_label.config(text=f"Faces Detected: {len(faces)}")
            self.log(f"Detected {len(faces)} faces from {self.total_faces} images")
            
            if len(faces) == 0:
                raise Exception("No faces detected in the images!")
            
            # Train the recognizer
            self.log("Training LBPH Face Recognizer...")
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.train(faces, np.array(ids))
            
            # Save the model
            trainer_dir = "trainer"
            os.makedirs(trainer_dir, exist_ok=True)
            model_path = os.path.join(trainer_dir, "trainer.yml")
            recognizer.write(model_path)
            
            self.log(f"Model saved to: {model_path}")
            self.log("="*50)
            self.log("TRAINING COMPLETED SUCCESSFULLY!")
            self.log("="*50)
            
            self.status_label.config(text="Status: Completed", fg='#2ecc71')
            messagebox.showinfo("Success", 
                f"Training completed successfully!\n\nFaces trained: {len(faces)}\nModel saved to: {model_path}")
            
        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            self.status_label.config(text="Status: Failed", fg='#e74c3c')
            messagebox.showerror("Error", f"Training failed: {str(e)}")
        
        finally:
            self.is_training = False
            self.scan_btn.config(state='normal')
            self.train_btn.config(state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = TrainDataModule(root)
    root.mainloop()