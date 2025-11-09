import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
from datetime import datetime
import sqlite3
import os

class FaceRecognitionUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Face Recognition Attendance System Software")
        self.root.geometry("1280x720")
        self.root.configure(bg='#0a0a2e')
        self.root.state('zoomed')  # Maximize window
        
        # Initialize database
        self.init_database()
        
        # Create header
        self.create_header()
        
        # Create main content area
        self.create_main_content()
        
        # Create footer
        self.create_footer()
        
        # Start time update
        self.update_time()
    
    def init_database(self):
        """Initialize SQLite database for student records"""
        try:
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    year TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    photo_path TEXT,
                    created_date TEXT
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    def get_db_connection(self):
        """Get database connection"""
        return sqlite3.connect('students.db')
    
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
        """Open Student Details module"""
        self.open_student_details_window()
    
    def open_student_details_window(self):
        """Create and open student details management window"""
        student_window = tk.Toplevel(self.root)
        student_window.title("Student Details Management")
        student_window.geometry("1200x800")
        student_window.configure(bg='#0a0a2e')
        student_window.grab_set()
        
        # Header
        header_frame = tk.Frame(student_window, bg='#16213e', height=60)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="👥 STUDENT DETAILS MANAGEMENT", 
                              fg='#00ffff', bg='#16213e', font=('Arial', 18, 'bold'))
        title_label.pack(expand=True)
        
        # Main content frame
        main_frame = tk.Frame(student_window, bg='#0a0a2e')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left side - Form
        form_frame = tk.LabelFrame(main_frame, text="Add/Edit Student", fg='white', bg='#16213e', 
                                  font=('Arial', 12, 'bold'), bd=2, relief='groove')
        form_frame.pack(side='left', fill='y', padx=(0, 10), pady=10)
        
        # Form fields
        fields = [
            ("Student ID:", "student_id"),
            ("Full Name:", "name"),
            ("Department:", "department"),
            ("Year:", "year"),
            ("Email:", "email"),
            ("Phone:", "phone")
        ]
        
        self.form_vars = {}
        for i, (label, var_name) in enumerate(fields):
            # Label
            lbl = tk.Label(form_frame, text=label, fg='white', bg='#16213e', font=('Arial', 10))
            lbl.grid(row=i, column=0, sticky='w', padx=10, pady=8)
            
            # Entry
            if var_name == "department":
                # Dropdown for department
                self.form_vars[var_name] = tk.StringVar()
                entry = ttk.Combobox(form_frame, textvariable=self.form_vars[var_name], 
                                   values=["Computer Science", "Information Technology", 
                                          "Electronics", "Mechanical", "Civil", "Electrical"],
                                   width=25, font=('Arial', 10))
            elif var_name == "year":
                # Dropdown for year
                self.form_vars[var_name] = tk.StringVar()
                entry = ttk.Combobox(form_frame, textvariable=self.form_vars[var_name],
                                   values=["1st Year", "2nd Year", "3rd Year", "4th Year"],
                                   width=25, font=('Arial', 10))
            else:
                # Regular entry
                self.form_vars[var_name] = tk.StringVar()
                entry = tk.Entry(form_frame, textvariable=self.form_vars[var_name], 
                               width=28, font=('Arial', 10), bg='#2a2a4e', fg='white',
                               insertbackground='white')
            
            entry.grid(row=i, column=1, padx=10, pady=8, sticky='w')
        
        # Photo section
        photo_frame = tk.Frame(form_frame, bg='#16213e')
        photo_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        self.photo_path_var = tk.StringVar()
        photo_btn = tk.Button(photo_frame, text="📸 Select Photo", command=self.select_photo,
                             bg='#4a4a8a', fg='white', font=('Arial', 10))
        photo_btn.pack(pady=5)
        
        self.photo_label = tk.Label(photo_frame, text="No photo selected", fg='#888', 
                                   bg='#16213e', font=('Arial', 9))
        self.photo_label.pack()
        
        # Action buttons
        button_frame = tk.Frame(form_frame, bg='#16213e')
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        
        add_btn = tk.Button(button_frame, text="➕ Add Student", command=self.add_student,
                           bg='#4caf50', fg='white', font=('Arial', 10, 'bold'), width=12)
        add_btn.pack(side='left', padx=5)
        
        update_btn = tk.Button(button_frame, text="✏️ Update", command=self.update_student,
                              bg='#2196f3', fg='white', font=('Arial', 10, 'bold'), width=12)
        update_btn.pack(side='left', padx=5)
        
        clear_btn = tk.Button(button_frame, text="🗑️ Clear", command=self.clear_form,
                             bg='#ff9800', fg='white', font=('Arial', 10, 'bold'), width=12)
        clear_btn.pack(side='left', padx=5)
        
        delete_btn = tk.Button(button_frame, text="❌ Delete", command=self.delete_student,
                              bg='#f44336', fg='white', font=('Arial', 10, 'bold'), width=12)
        delete_btn.pack(side='left', padx=5)
        
        # Right side - Student list
        list_frame = tk.LabelFrame(main_frame, text="Student Records", fg='white', bg='#16213e',
                                  font=('Arial', 12, 'bold'), bd=2, relief='groove')
        list_frame.pack(side='right', fill='both', expand=True, padx=(10, 0), pady=10)
        
        # Search frame
        search_frame = tk.Frame(list_frame, bg='#16213e')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="🔍 Search:", fg='white', bg='#16213e', 
                font=('Arial', 10)).pack(side='left')
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30,
                               font=('Arial', 10), bg='#2a2a4e', fg='white',
                               insertbackground='white')
        search_entry.pack(side='left', padx=10)
        search_entry.bind('<KeyRelease>', self.search_students)
        
        # Treeview for student list
        tree_frame = tk.Frame(list_frame, bg='#16213e')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Configure treeview style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#2a2a4e", foreground="white",
                       fieldbackground="#2a2a4e", font=('Arial', 9))
        style.configure("Treeview.Heading", background="#4a4a8a", foreground="white",
                       font=('Arial', 10, 'bold'))
        
        # Create treeview
        columns = ("ID", "Student ID", "Name", "Department", "Year", "Email", "Phone")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                yscrollcommand=scrollbar.set)
        
        # Define column headings and widths
        column_widths = {"ID": 50, "Student ID": 100, "Name": 150, "Department": 120, 
                        "Year": 80, "Email": 180, "Phone": 120}
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), minwidth=50)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_student_select)
        
        # Load initial data
        self.load_students()
        
        # Store reference to current window
        self.student_window = student_window
    
    def select_photo(self):
        """Open file dialog to select student photo"""
        file_path = filedialog.askopenfilename(
            title="Select Student Photo",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if file_path:
            self.photo_path_var.set(file_path)
            filename = os.path.basename(file_path)
            self.photo_label.config(text=f"Selected: {filename}", fg='#4caf50')
    
    def add_student(self):
        """Add new student to database"""
        # Validate required fields
        required_fields = ['student_id', 'name', 'department', 'year']
        for field in required_fields:
            if not self.form_vars[field].get().strip():
                messagebox.showerror("Error", f"Please fill in {field.replace('_', ' ').title()}")
                return
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO students (student_id, name, department, year, email, phone, photo_path, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.form_vars['student_id'].get().strip(),
                self.form_vars['name'].get().strip(),
                self.form_vars['department'].get().strip(),
                self.form_vars['year'].get().strip(),
                self.form_vars['email'].get().strip(),
                self.form_vars['phone'].get().strip(),
                self.photo_path_var.get(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Student added successfully!")
            self.clear_form()
            self.load_students()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Student ID already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def update_student(self):
        """Update selected student"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to update")
            return
        
        # Get the ID of selected student
        item = self.tree.item(selected[0])
        student_db_id = item['values'][0]
        
        # Validate required fields
        required_fields = ['student_id', 'name', 'department', 'year']
        for field in required_fields:
            if not self.form_vars[field].get().strip():
                messagebox.showerror("Error", f"Please fill in {field.replace('_', ' ').title()}")
                return
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE students 
                SET student_id=?, name=?, department=?, year=?, email=?, phone=?, photo_path=?
                WHERE id=?
            ''', (
                self.form_vars['student_id'].get().strip(),
                self.form_vars['name'].get().strip(),
                self.form_vars['department'].get().strip(),
                self.form_vars['year'].get().strip(),
                self.form_vars['email'].get().strip(),
                self.form_vars['phone'].get().strip(),
                self.photo_path_var.get(),
                student_db_id
            ))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Student updated successfully!")
            self.clear_form()
            self.load_students()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Student ID already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def delete_student(self):
        """Delete selected student"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to delete")
            return
        
        item = self.tree.item(selected[0])
        student_name = item['values'][2]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student_name}?"):
            try:
                student_db_id = item['values'][0]
                conn = self.get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute('DELETE FROM students WHERE id=?', (student_db_id,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.clear_form()
                self.load_students()
                
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def clear_form(self):
        """Clear all form fields"""
        for var in self.form_vars.values():
            var.set("")
        self.photo_path_var.set("")
        self.photo_label.config(text="No photo selected", fg='#888')
    
    def load_students(self):
        """Load students from database into treeview"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students ORDER BY name')
            students = cursor.fetchall()
            conn.close()
            
            for student in students:
                self.tree.insert('', 'end', values=student[:7])  # Exclude created_date for display
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load students: {str(e)}")
    
    def search_students(self, event=None):
        """Search students based on search term"""
        search_term = self.search_var.get().lower()
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            if search_term:
                cursor.execute('''
                    SELECT * FROM students 
                    WHERE LOWER(student_id) LIKE ? OR LOWER(name) LIKE ? OR LOWER(department) LIKE ?
                    ORDER BY name
                ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            else:
                cursor.execute('SELECT * FROM students ORDER BY name')
            
            students = cursor.fetchall()
            conn.close()
            
            for student in students:
                self.tree.insert('', 'end', values=student[:7])
                
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
    
    def on_student_select(self, event):
        """Handle student selection from treeview"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            
            # Fill form with selected student data
            self.form_vars['student_id'].set(values[1])
            self.form_vars['name'].set(values[2])
            self.form_vars['department'].set(values[3])
            self.form_vars['year'].set(values[4])
            self.form_vars['email'].set(values[5] if values[5] else "")
            self.form_vars['phone'].set(values[6] if values[6] else "")
            
            # Get photo path from database
            try:
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT photo_path FROM students WHERE id=?', (values[0],))
                result = cursor.fetchone()
                conn.close()
                
                if result and result[0]:
                    self.photo_path_var.set(result[0])
                    filename = os.path.basename(result[0])
                    self.photo_label.config(text=f"Selected: {filename}", fg='#4caf50')
                else:
                    self.photo_path_var.set("")
                    self.photo_label.config(text="No photo selected", fg='#888')
                    
            except Exception as e:
                print(f"Error loading photo path: {e}")

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
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
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

if __name__ == "__main__":
    app = FaceRecognitionUI()
    app.run()