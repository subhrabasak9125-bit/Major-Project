import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os

class StudentManagementUI:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Student Management System")
        self.window.geometry("1200x800")
        self.window.configure(bg='#f0f0f0')
        self.window.state('zoomed')
        
        # Center the window
        self.window.transient(parent)
        self.window.grab_set()
        
        # Initialize variables to store entry widgets
        self.dept_combo = None
        self.course_combo = None
        self.year_combo = None
        self.sem_combo = None
        self.student_id_entry = None
        self.student_name_entry = None
        self.division_combo = None
        self.roll_entry = None
        self.gender_combo = None
        self.dob_entry = None
        self.email_entry = None
        self.phone_entry = None
        self.address_entry = None
        self.teacher_entry = None
        self.search_combo = None
        self.search_entry = None
        self.tree = None
        
        # Create student data directory
        os.makedirs('student_data', exist_ok=True)
        
        self.create_student_management_ui()
        
        # Load existing students
        self.load_students()
    
    def create_student_management_ui(self):
        # Main container
        main_container = tk.Frame(self.window, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Time display (top right)
        time_frame = tk.Frame(main_container, bg='#f0f0f0')
        time_frame.pack(fill='x', pady=(0, 10))
        
        self.time_label = tk.Label(time_frame, text="", fg='#2c3e50', bg='#f0f0f0', 
                                 font=('Arial', 12, 'bold'))
        self.time_label.pack(side='right')
        self.update_time()
        
        # Student Information Section
        self.create_student_info_section(main_container)
        
        # Student Class Information Section
        self.create_student_class_section(main_container)
        
        # Student Details Section
        self.create_student_details_section(main_container)
    
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S %p")
        self.time_label.config(text=current_time)
        if self.window.winfo_exists():
            self.window.after(1000, self.update_time)
    
    def create_student_info_section(self, parent):
        # Student Information Frame
        info_frame = tk.LabelFrame(parent, text="Student Information", 
                                 font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        info_frame.pack(fill='x', pady=(0, 10))
        
        # Current Course Information
        tk.Label(info_frame, text="Current Course Information", 
                font=('Arial', 10, 'bold'), bg='#f0f0f0').pack(anchor='w', padx=10, pady=(10, 5))
        
        # Department and Courses
        course_frame = tk.Frame(info_frame, bg='#f0f0f0')
        course_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(course_frame, text="Department:", bg='#f0f0f0').pack(side='left', padx=(0, 5))
        self.dept_combo = ttk.Combobox(course_frame, values=["Computer", "Mechanical", "Electrical", "Civil"], 
                                width=15, state="readonly")
        self.dept_combo.pack(side='left', padx=(0, 20))
        self.dept_combo.set("Select Department")
        
        tk.Label(course_frame, text="Courses:", bg='#f0f0f0').pack(side='left', padx=(0, 5))
        self.course_combo = ttk.Combobox(course_frame, values=["EE", "TE", "CE", "ME", "BE"], 
                                  width=15, state="readonly")
        self.course_combo.pack(side='left')
        self.course_combo.set("Select Course")
        
        # Year and Semester
        year_sem_frame = tk.Frame(info_frame, bg='#f0f0f0')
        year_sem_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(year_sem_frame, text="Year:", bg='#f0f0f0').pack(side='left', padx=(0, 5))
        self.year_combo = ttk.Combobox(year_sem_frame, values=["2020-2021", "2021-2022", "2022-2023", "2023-2024", "2024-2025"], 
                                width=15, state="readonly")
        self.year_combo.pack(side='left', padx=(0, 20))
        self.year_combo.set("Select Year")
        
        tk.Label(year_sem_frame, text="Semester:", bg='#f0f0f0').pack(side='left', padx=(0, 5))
        self.sem_combo = ttk.Combobox(year_sem_frame, values=["Semester-1", "Semester-2", "Semester-3", "Semester-4", 
                                                              "Semester-5", "Semester-6", "Semester-7", "Semester-8"], 
                               width=15, state="readonly")
        self.sem_combo.pack(side='left')
        self.sem_combo.set("Select Semester")
    
    def create_student_class_section(self, parent):
        # Student Class Information Frame
        class_frame = tk.LabelFrame(parent, text="Student Class Information", 
                                  font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        class_frame.pack(fill='x', pady=(0, 10))
        
        # Student ID and Name
        id_name_frame = tk.Frame(class_frame, bg='#f0f0f0')
        id_name_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(id_name_frame, text="StudentID No:", bg='#f0f0f0').pack(side='left', padx=(0, 5))
        self.student_id_entry = tk.Entry(id_name_frame, width=20)
        self.student_id_entry.pack(side='left', padx=(0, 20))
        
        tk.Label(id_name_frame, text="Student Name:", bg='#f0f0f0').pack(side='left', padx=(0, 5))
        self.student_name_entry = tk.Entry(id_name_frame, width=20)
        self.student_name_entry.pack(side='left')
        
        # Class Division and Roll No
        class_roll_frame = tk.Frame(class_frame, bg='#f0f0f0')
        class_roll_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(class_roll_frame, text="Class Division:", bg='#f0f0f0').pack(side='left', padx=(0, 5))
        self.division_combo = ttk.Combobox(class_roll_frame, values=["A", "B", "C", "D"], 
                                    width=15, state="readonly")
        self.division_combo.pack(side='left', padx=(0, 20))
        self.division_combo.set("Select Division")
        
        tk.Label(class_roll_frame, text="Roll No:", bg='#f0f0f0').pack(side='left', padx=(0, 5))
        self.roll_entry = tk.Entry(class_roll_frame, width=15)
        self.roll_entry.pack(side='left')
        
        # Gender and DOB
        gender_dob_frame = tk.Frame(class_frame, bg='#f0f0f0')
        gender_dob_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(gender_dob_frame, text="Gender:", bg='#f0f0f0').pack(side='left', padx=(0, 5))
        self.gender_combo = ttk.Combobox(gender_dob_frame, values=["Male", "Female", "Other"], 
                                  width=15, state="readonly")
        self.gender_combo.pack(side='left', padx=(0, 20))
        self.gender_combo.set("Male")
        
        tk.Label(gender_dob_frame, text="DOB (DD/MM/YYYY):", bg='#f0f0f0').pack(side='left', padx=(0, 5))
        self.dob_entry = tk.Entry(gender_dob_frame, width=15)
        self.dob_entry.pack(side='left')
        self.dob_entry.insert(0, "01/01/2000")
        
        # Email and Phone
        email_phone_frame = tk.Frame(class_frame, bg='#f0f0f0')
        email_phone_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(email_phone_frame, text="Email:", bg='#f0f0f0').pack(side='left', padx=(0, 5))
        self.email_entry = tk.Entry(email_phone_frame, width=30)
        self.email_entry.pack(side='left', padx=(0, 20))
        
        tk.Label(email_phone_frame, text="Phone No:", bg='#f0f0f0').pack(side='left', padx=(0, 5))
        self.phone_entry = tk.Entry(email_phone_frame, width=15)
        self.phone_entry.pack(side='left')
        
        # Address and Teacher
        address_teacher_frame = tk.Frame(class_frame, bg='#f0f0f0')
        address_teacher_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(address_teacher_frame, text="Address:", bg='#f0f0f0').pack(side='left', padx=(0, 5))
        self.address_entry = tk.Entry(address_teacher_frame, width=30)
        self.address_entry.pack(side='left', padx=(0, 20))
        
        tk.Label(address_teacher_frame, text="Teacher Name:", bg='#f0f0f0').pack(side='left', padx=(0, 5))
        self.teacher_entry = tk.Entry(address_teacher_frame, width=15)
        self.teacher_entry.pack(side='left')
        
        # Photo Sample Checkboxes
        photo_frame = tk.Frame(class_frame, bg='#f0f0f0')
        photo_frame.pack(fill='x', padx=20, pady=10)
        
        self.take_photo_var = tk.BooleanVar()
        self.no_photo_var = tk.BooleanVar()
        
        take_photo_cb = tk.Checkbutton(photo_frame, text="Take Photo Sample", 
                                     variable=self.take_photo_var, bg='#f0f0f0',
                                     command=self.on_take_photo_toggle)
        take_photo_cb.pack(side='left', padx=(0, 20))
        
        no_photo_cb = tk.Checkbutton(photo_frame, text="No Photo Sample", 
                                   variable=self.no_photo_var, bg='#f0f0f0',
                                   command=self.on_no_photo_toggle)
        no_photo_cb.pack(side='left')
        
        # Action Buttons
        action_frame = tk.Frame(class_frame, bg='#f0f0f0')
        action_frame.pack(fill='x', padx=20, pady=10)
        
        # First row of buttons
        row1_frame = tk.Frame(action_frame, bg='#f0f0f0')
        row1_frame.pack(fill='x', pady=5)
        
        tk.Button(row1_frame, text="SAVE", bg='#2ecc71', fg='white', 
                 font=('Arial', 10, 'bold'), width=12, height=2,
                 command=self.save_student).pack(side='left', padx=5)
        
        tk.Button(row1_frame, text="UPDATE", bg='#3498db', fg='white', 
                 font=('Arial', 10, 'bold'), width=12, height=2,
                 command=self.update_student).pack(side='left', padx=5)
        
        tk.Button(row1_frame, text="DELETE", bg='#e74c3c', fg='white', 
                 font=('Arial', 10, 'bold'), width=12, height=2,
                 command=self.delete_student).pack(side='left', padx=5)
        
        tk.Button(row1_frame, text="RESET", bg='#f39c12', fg='white', 
                 font=('Arial', 10, 'bold'), width=12, height=2,
                 command=self.reset_form).pack(side='left', padx=5)
        
        # Second row of buttons
        row2_frame = tk.Frame(action_frame, bg='#f0f0f0')
        row2_frame.pack(fill='x', pady=5)
        
        tk.Button(row2_frame, text="ADD PHOTO SAMPLE", bg='#9b59b6', fg='white', 
                 font=('Arial', 10, 'bold'), width=25, height=2,
                 command=self.add_photo_sample).pack(side='left', padx=5)
        
        tk.Button(row2_frame, text="UPDATE PHOTO SAMPLE", bg='#34495e', fg='white', 
                 font=('Arial', 10, 'bold'), width=25, height=2,
                 command=self.update_photo_sample).pack(side='left', padx=5)
    
    def create_student_details_section(self, parent):
        # Student Details Frame
        details_frame = tk.LabelFrame(parent, text="Student Details", 
                                    font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        details_frame.pack(fill='both', expand=True)
        
        # Search Section
        search_frame = tk.Frame(details_frame, bg='#f0f0f0')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="View Student Details & Search System", 
                font=('Arial', 10, 'bold'), bg='#f0f0f0').pack(anchor='w', pady=(0, 10))
        
        search_option_frame = tk.Frame(search_frame, bg='#f0f0f0')
        search_option_frame.pack(fill='x', pady=5)
        
        tk.Label(search_option_frame, text="Search By", bg='#f0f0f0').pack(side='left', padx=(0, 10))
        self.search_combo = ttk.Combobox(search_option_frame, 
                                  values=["Student ID", "Student Name", "Roll No", "Department"], 
                                  width=15, state="readonly")
        self.search_combo.pack(side='left', padx=(0, 10))
        self.search_combo.set("Select Option")
        
        self.search_entry = tk.Entry(search_option_frame, width=20)
        self.search_entry.pack(side='left', padx=(0, 10))
        
        tk.Button(search_option_frame, text="SEARCH", bg='#3498db', fg='white', 
                 font=('Arial', 10, 'bold'), width=10,
                 command=self.search_student).pack(side='left', padx=(0, 10))
        
        tk.Button(search_option_frame, text="SHOW ALL", bg='#2ecc71', fg='white', 
                 font=('Arial', 10, 'bold'), width=10,
                 command=self.show_all_students).pack(side='left')
        
        # Data display table
        table_frame = tk.Frame(details_frame, bg='#f0f0f0')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create a treeview to display student data
        columns = ("Department", "Course", "Year", "Semester", "StudentID", "Student Name", 
                  "Class Div", "Roll No", "Email", "Phone")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)
        
        # Define headings and column widths
        column_widths = {
            "Department": 100,
            "Course": 80,
            "Year": 100,
            "Semester": 100,
            "StudentID": 80,
            "Student Name": 150,
            "Class Div": 80,
            "Roll No": 80,
            "Email": 180,
            "Phone": 120
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col])
        
        # Bind double-click event to populate form
        self.tree.bind('<Double-1>', self.on_student_select)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def on_take_photo_toggle(self):
        if self.take_photo_var.get():
            self.no_photo_var.set(False)
    
    def on_no_photo_toggle(self):
        if self.no_photo_var.get():
            self.take_photo_var.set(False)
    
    def validate_student_data(self):
        """Validate all student data before saving"""
        if not self.student_id_entry.get().strip():
            messagebox.showerror("Validation Error", "Please enter Student ID!")
            return False
        
        if not self.student_name_entry.get().strip():
            messagebox.showerror("Validation Error", "Please enter Student Name!")
            return False
        
        if self.dept_combo.get() == "Select Department":
            messagebox.showerror("Validation Error", "Please select Department!")
            return False
        
        if self.course_combo.get() == "Select Course":
            messagebox.showerror("Validation Error", "Please select Course!")
            return False
        
        if self.year_combo.get() == "Select Year":
            messagebox.showerror("Validation Error", "Please select Year!")
            return False
        
        if self.sem_combo.get() == "Select Semester":
            messagebox.showerror("Validation Error", "Please select Semester!")
            return False
        
        if self.division_combo.get() == "Select Division":
            messagebox.showerror("Validation Error", "Please select Class Division!")
            return False
        
        # Validate student ID is numeric
        try:
            int(self.student_id_entry.get())
        except ValueError:
            messagebox.showerror("Validation Error", "Student ID must be numeric!")
            return False
        
        return True
    
    def save_student(self):
        """Save student information to CSV file"""
        if not self.validate_student_data():
            return
        
        student_data = {
            'StudentID': self.student_id_entry.get().strip(),
            'Name': self.student_name_entry.get().strip(),
            'Department': self.dept_combo.get(),
            'Course': self.course_combo.get(),
            'Year': self.year_combo.get(),
            'Semester': self.sem_combo.get(),
            'Division': self.division_combo.get(),
            'RollNo': self.roll_entry.get().strip(),
            'Gender': self.gender_combo.get(),
            'DOB': self.dob_entry.get().strip(),
            'Email': self.email_entry.get().strip(),
            'Phone': self.phone_entry.get().strip(),
            'Address': self.address_entry.get().strip(),
            'Teacher': self.teacher_entry.get().strip()
        }
        
        # Check if student already exists
        if self.student_exists(student_data['StudentID']):
            messagebox.showerror("Error", "Student ID already exists! Use UPDATE instead.")
            return
        
        # Save to CSV
        csv_file = 'student_data/students.csv'
        file_exists = os.path.isfile(csv_file)
        
        try:
            with open(csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=student_data.keys())
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(student_data)
            
            # Add to treeview
            self.tree.insert("", "end", values=(
                student_data['Department'],
                student_data['Course'],
                student_data['Year'],
                student_data['Semester'],
                student_data['StudentID'],
                student_data['Name'],
                student_data['Division'],
                student_data['RollNo'],
                student_data['Email'],
                student_data['Phone']
            ))
            
            messagebox.showinfo("Success", "Student information saved successfully!")
            
            # Ask if user wants to take photo sample
            if messagebox.askyesno("Photo Sample", "Do you want to capture photo samples for this student?"):
                self.add_photo_sample()
            else:
                self.reset_form()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save student: {str(e)}")
    
    def student_exists(self, student_id):
        """Check if student ID already exists"""
        csv_file = 'student_data/students.csv'
        if not os.path.isfile(csv_file):
            return False
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['StudentID'] == student_id:
                        return True
        except Exception:
            pass
        
        return False
    
    def update_student(self):
        """Update existing student information"""
        if not self.validate_student_data():
            return
        
        student_id = self.student_id_entry.get().strip()
        
        if not self.student_exists(student_id):
            messagebox.showerror("Error", "Student ID not found! Use SAVE for new students.")
            return
        
        csv_file = 'student_data/students.csv'
        temp_file = 'student_data/students_temp.csv'
        
        student_data = {
            'StudentID': student_id,
            'Name': self.student_name_entry.get().strip(),
            'Department': self.dept_combo.get(),
            'Course': self.course_combo.get(),
            'Year': self.year_combo.get(),
            'Semester': self.sem_combo.get(),
            'Division': self.division_combo.get(),
            'RollNo': self.roll_entry.get().strip(),
            'Gender': self.gender_combo.get(),
            'DOB': self.dob_entry.get().strip(),
            'Email': self.email_entry.get().strip(),
            'Phone': self.phone_entry.get().strip(),
            'Address': self.address_entry.get().strip(),
            'Teacher': self.teacher_entry.get().strip()
        }
        
        try:
            # Read all students and update the matching one
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                students = list(reader)
            
            # Update the student
            for i, student in enumerate(students):
                if student['StudentID'] == student_id:
                    students[i] = student_data
                    break
            
            # Write back to file
            with open(temp_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(students)
            
            # Replace original file
            os.replace(temp_file, csv_file)
            
            # Refresh treeview
            self.load_students()
            
            messagebox.showinfo("Success", "Student information updated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student: {str(e)}")
    
    def delete_student(self):
        """Delete student record"""
        student_id = self.student_id_entry.get().strip()
        
        if not student_id:
            messagebox.showerror("Error", "Please enter Student ID to delete!")
            return
        
        if not self.student_exists(student_id):
            messagebox.showerror("Error", "Student ID not found!")
            return
        
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete Student ID: {student_id}?"):
            return
        
        csv_file = 'student_data/students.csv'
        temp_file = 'student_data/students_temp.csv'
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                students = [row for row in reader if row['StudentID'] != student_id]
            
            with open(temp_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(students)
            
            os.replace(temp_file, csv_file)
            
            # Refresh treeview
            self.load_students()
            
            # Reset form
            self.reset_form()
            
            messagebox.showinfo("Success", "Student record deleted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
    
    def reset_form(self):
        """Reset all form fields"""
        self.student_id_entry.delete(0, 'end')
        self.student_name_entry.delete(0, 'end')
        self.dept_combo.set("Select Department")
        self.course_combo.set("Select Course")
        self.year_combo.set("Select Year")
        self.sem_combo.set("Select Semester")
        self.division_combo.set("Select Division")
        self.roll_entry.delete(0, 'end')
        self.gender_combo.set("Male")
        self.dob_entry.delete(0, 'end')
        self.dob_entry.insert(0, "01/01/2000")
        self.email_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.address_entry.delete(0, 'end')
        self.teacher_entry.delete(0, 'end')
        self.take_photo_var.set(False)
        self.no_photo_var.set(False)
    
    def add_photo_sample(self):
        """Open photo capture module for student"""
        student_id = self.student_id_entry.get().strip()
        student_name = self.student_name_entry.get().strip()
        
        if not student_id:
            messagebox.showerror("Error", "Please enter Student ID first!")
            return
        
        if not student_name:
            messagebox.showerror("Error", "Please enter Student Name first!")
            return
        
        try:
            from photo_capture_module import PhotoCaptureModule
            PhotoCaptureModule(self.window, student_id=int(student_id), student_name=student_name)
        except ValueError:
            messagebox.showerror("Error", "Student ID must be a valid number!")
        except ImportError:
            messagebox.showerror("Error", "Photo capture module not found! Please ensure photo_capture_module.py is in the same directory.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open photo capture: {str(e)}")
    
    def update_photo_sample(self):
        """Update photo samples for existing student"""
        self.add_photo_sample()
    
    def load_students(self):
        """Load students from CSV file into treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        csv_file = 'student_data/students.csv'
        if not os.path.isfile(csv_file):
            return
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.tree.insert("", "end", values=(
                        row.get('Department', ''),
                        row.get('Course', ''),
                        row.get('Year', ''),
                        row.get('Semester', ''),
                        row.get('StudentID', ''),
                        row.get('Name', ''),
                        row.get('Division', ''),
                        row.get('RollNo', ''),
                        row.get('Email', ''),
                        row.get('Phone', '')
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load students: {str(e)}")
    
    def search_student(self):
        """Search for students based on selected criteria"""
        search_by = self.search_combo.get()
        search_value = self.search_entry.get().strip()
        
        if search_by == "Select Option":
            messagebox.showerror("Error", "Please select search criteria!")
            return
        
        if not search_value:
            messagebox.showerror("Error", "Please enter search value!")
            return
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        csv_file = 'student_data/students.csv'
        if not os.path.isfile(csv_file):
            messagebox.showinfo("Info", "No student records found!")
            return
        
        found_count = 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Map search criteria to CSV column names
                search_map = {
                    "Student ID": "StudentID",
                    "Student Name": "Name",
                    "Roll No": "RollNo",
                    "Department": "Department"
                }
                
                column_name = search_map.get(search_by)
                
                for row in reader:
                    if search_value.lower() in str(row.get(column_name, '')).lower():
                        self.tree.insert("", "end", values=(
                            row.get('Department', ''),
                            row.get('Course', ''),
                            row.get('Year', ''),
                            row.get('Semester', ''),
                            row.get('StudentID', ''),
                            row.get('Name', ''),
                            row.get('Division', ''),
                            row.get('RollNo', ''),
                            row.get('Email', ''),
                            row.get('Phone', '')
                        ))
                        found_count += 1
            
            if found_count == 0:
                messagebox.showinfo("Search Result", "No matching records found!")
            else:
                messagebox.showinfo("Search Result", f"Found {found_count} matching record(s)!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
    
    def show_all_students(self):
        """Show all students in the treeview"""
        self.load_students()
        messagebox.showinfo("Info", "Showing all students!")
    
    def on_student_select(self, event):
        """Populate form when a student is selected from treeview"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        # Get values from selected row
        values = self.tree.item(selected_item[0], 'values')
        
        if not values:
            return
        
        # Clear form first
        self.reset_form()
        
        # Populate form fields
        self.dept_combo.set(values[0])
        self.course_combo.set(values[1])
        self.year_combo.set(values[2])
        self.sem_combo.set(values[3])
        self.student_id_entry.insert(0, values[4])
        self.student_name_entry.insert(0, values[5])
        self.division_combo.set(values[6])
        self.roll_entry.insert(0, values[7])
        self.email_entry.insert(0, values[8])
        self.phone_entry.insert(0, values[9])
        
        # Load additional details from CSV
        csv_file = 'student_data/students.csv'
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['StudentID'] == values[4]:
                        self.gender_combo.set(row.get('Gender', 'Male'))
                        self.dob_entry.delete(0, 'end')
                        self.dob_entry.insert(0, row.get('DOB', '01/01/2000'))
                        self.address_entry.insert(0, row.get('Address', ''))
                        self.teacher_entry.insert(0, row.get('Teacher', ''))
                        break
        except Exception:
            pass
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    # Test the module
    root = tk.Tk()
    root.withdraw()
    app = StudentManagementUI(root)
    root.mainloop()