import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime

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
        settings_btn = tk.Button(footer_frame, text="⚙ Settings", fg='white', bg='#4a4a8a',
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
        self.show_message("Student Details", "Opening Student Details module...")
    
    def face_recognition(self):
        self.show_message("Face Recognition", "Initializing Face Recognition system...")
    
    def attendance(self):
        self.show_message("Attendance", "Loading Attendance records...")
    
    def help_desk(self):
        self.show_message("Help Desk", "Opening Help documentation...")
    
    def train_data(self):
        self.show_message("Train Data", "Starting face recognition training...")
    
    def photos(self):
        self.show_message("Photos", "Opening photo gallery...")
    
    def developer(self):
        self.show_message("Developer", "Developer: SMIT Students\nContact: smit@example.com")
    
    def settings(self):
        self.show_message("Settings", "Opening system settings...")
    
    def exit_app(self):
        if tk.messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()
    
    def show_message(self, title, message):
        # Create a simple message dialog
        msg_window = tk.Toplevel(self.root)
        msg_window.title(title)
        msg_window.geometry("400x200")
        msg_window.configure(bg='#16213e')
        msg_window.grab_set()
        
        # Center the window
        msg_window.transient(self.root)
        
        label = tk.Label(msg_window, text=message, fg='white', bg='#16213e', 
                        font=('Arial', 12), wraplength=350, justify='center')
        label.pack(expand=True)
        
        ok_btn = tk.Button(msg_window, text="OK", command=msg_window.destroy, 
                          bg='#4a4a8a', fg='white', font=('Arial', 10))
        ok_btn.pack(pady=20)
    
    def run(self):
        self.root.mainloop()

# Import messagebox after creating the class
import tkinter.messagebox

if __name__ == "__main__":
    app = FaceRecognitionUI()
    app.run()
