import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import csv
import os

class UpdatedStudentManagement:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("SMIT Student Management System")
        self.window.geometry("1300x850")
        self.window.configure(bg='#0a0a2e')
        self.window.state('zoomed')
        
        self.window.transient(parent)
        self.window.grab_set()
        
        # Create data directories
        os.makedirs('student_data', exist_ok=True)
        os.makedirs('data/student_photos', exist_ok=True)
        
        self.create_ui()
        self.load_students()
    
    def create_ui(self):
        # Main container with gradient background
        main_container = tk.Frame(self.window, bg='#0a0a2e')
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Header with time
        header = tk.Frame(main_container, bg='#16213e', height=70)
        header.pack(fill='x', pady=(0,10))
        header.pack_propagate(False)
        
        tk.Label(header, text="SMIT STUDENT MANAGEMENT SYSTEM",
                fg='#00ffff', bg='#16213e', 
                font=('Arial', 20, 'bold')).pack(side='left', padx=20, pady=15)
        
        self.time_label = tk.Label(header, text="", fg='#00ffff', 
                                  bg='#16213e', font=('Arial', 12, 'bold'))
        self.time_label.pack(side='right', padx=20)
        self.update_time()
        
        # Student Information Section
        self.create_student_info_section(main_container)
        
        # Student Details Section
        self.create_student_details_section(main_container)
        
        # Action Buttons
        self.create_action_buttons(main_container)
        
        # Student Records Table
        self.create_records_table(main_container)
    
    def update_time(self):
        current_time = datetime.now().strftime("%I:%M:%S %p • %d %B %Y")
        self.time_label.config(text=current_time)
        if self.window.winfo_exists():
            self.window.after(1000, self.update_time)
    
    def create_student_info_section(self, parent):
        info_frame = tk.LabelFrame(parent, text="Academic Information",
                                  font=('Arial', 12, 'bold'), bg='#16213e',
                                  fg='#00ffff', bd=2, relief='raised')
        info_frame.pack(fill='x', pady=(0,10))
        
        inner = tk.Frame(info_frame, bg='#16213e')
        inner.pack(padx=20, pady=15)
        
        # Row 1: Department and Year
        row1 = tk.Frame(inner, bg='#16213e')
        row1.grid(row=0, column=0, columnspan=4, sticky='ew', pady=5)
        
        tk.Label(row1, text="Department:", fg='white', bg='#16213e',
                font=('Arial', 10, 'bold')).pack(side='left', padx=(0,10))
        
        self.dept_combo = ttk.Combobox(row1, 
                                      values=["DCSE", "DCE", "DME", "DEE", "DETC"],
                                      width=18, state="readonly", font=('Arial', 10))
        self.dept_combo.pack(side='left', padx=(0,30))
        self.dept_combo.set("Select Department")
        
        tk.Label(row1, text="Academic Year:", fg='white', bg='#16213e',
                font=('Arial', 10, 'bold')).pack(side='left', padx=(0,10))
        
        years = [f"{y}-{y+3}" for y in range(1999, 2027)]
        self.year_combo = ttk.Combobox(row1, values=years, width=18,
                                      state="readonly", font=('Arial', 10))
        self.year_combo.pack(side='left')
        self.year_combo.set("Select Year")
        
        # Row 2: Semester
        row2 = tk.Frame(inner, bg='#16213e')
        row2.grid(row=1, column=0, columnspan=4, sticky='ew', pady=5)
        
        tk.Label(row2, text="Semester:", fg='white', bg='#16213e',
                font=('Arial', 10, 'bold')).pack(side='left', padx=(0,10))
        
        self.sem_combo = ttk.Combobox(row2,
                                     values=[f"Semester-{i}" for i in range(1, 7)],
                                     width=18, state="readonly", font=('Arial', 10))
        self.sem_combo.pack(side='left')
        self.sem_combo.set("Select Semester")
    
    def create_student_details_section(self, parent):
        details_frame = tk.LabelFrame(parent, text="Student Personal Details",
                                     font=('Arial', 12, 'bold'), bg='#16213e',
                                     fg='#00ffff', bd=2, relief='raised')
        details_frame.pack(fill='x', pady=(0,10))
        
        inner = tk.Frame(details_frame, bg='#16213e')
        inner.pack(padx=20, pady=15)
        
        # Configure grid
        for i in range(6):
            inner.columnconfigure(i, weight=1)
        
        # Row 1: Student ID and Name
        tk.Label(inner, text="Student ID:", fg='white', bg='#16213e',
                font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.student_id_entry = tk.Entry(inner, width=20, font=('Arial', 10))
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(inner, text="Full Name:", fg='white', bg='#16213e',
                font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.student_name_entry = tk.Entry(inner, width=30, font=('Arial', 10))
        self.student_name_entry.grid(row=0, column=3, columnspan=2, padx=5, pady=5, sticky='ew')
        
        # Row 2: Registration Number and Gender
        tk.Label(inner, text="Registration No:", fg='white', bg='#16213e',
                font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.reg_entry = tk.Entry(inner, width=20, font=('Arial', 10))
        self.reg_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(inner, text="Gender:", fg='white', bg='#16213e',
                font=('Arial', 10, 'bold')).grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.gender_combo = ttk.Combobox(inner, values=["Male", "Female", "Other"],
                                        width=18, state="readonly", font=('Arial', 10))
        self.gender_combo.grid(row=1, column=3, padx=5, pady=5)
        self.gender_combo.set("Male")
        
        # Row 3: DOB with Calendar Picker and Blood Group
        tk.Label(inner, text="Date of Birth:", fg='white', bg='#16213e',
                font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        
        # DateEntry widget with calendar picker
        self.dob_calendar = DateEntry(inner, width=18, background='#3498db',
                                     foreground='white', borderwidth=2,
                                     font=('Arial', 10), date_pattern='dd/mm/yyyy',
                                     mindate=datetime(1980, 1, 1),
                                     maxdate=datetime.now())
        self.dob_calendar.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        tk.Label(inner, text="Blood Group:", fg='white', bg='#16213e',
                font=('Arial', 10, 'bold')).grid(row=2, column=2, sticky='w', padx=5, pady=5)
        self.blood_combo = ttk.Combobox(inner, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                                       width=18, state="readonly", font=('Arial', 10))
        self.blood_combo.grid(row=2, column=3, padx=5, pady=5)
        self.blood_combo.set("Select")
        
        # Row 4: Email and Phone
        tk.Label(inner, text="Email:", fg='white', bg='#16213e',
                font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.email_entry = tk.Entry(inner, width=35, font=('Arial', 10))
        self.email_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        
        tk.Label(inner, text="Phone:", fg='white', bg='#16213e',
                font=('Arial', 10, 'bold')).grid(row=3, column=3, sticky='w', padx=5, pady=5)
        self.phone_entry = tk.Entry(inner, width=20, font=('Arial', 10))
        self.phone_entry.grid(row=3, column=4, padx=5, pady=5)
        
        # Row 5: Father's Name
        tk.Label(inner, text="Father's Name:", fg='white', bg='#16213e',
                font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky='w', padx=5, pady=5)
        self.father_entry = tk.Entry(inner, width=30, font=('Arial', 10))
        self.father_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        
        # Row 6: Address
        tk.Label(inner, text="Address:", fg='white', bg='#16213e',
                font=('Arial', 10, 'bold')).grid(row=5, column=0, sticky='w', padx=5, pady=5)
        self.address_entry = tk.Entry(inner, width=60, font=('Arial', 10))
        self.address_entry.grid(row=5, column=1, columnspan=4, padx=5, pady=5, sticky='ew')
    
    def create_action_buttons(self, parent):
        btn_frame = tk.Frame(parent, bg='#0a0a2e')
        btn_frame.pack(fill='x', pady=10)
        
        buttons = [
            ("💾 SAVE", "#2ecc71", self.save_student),
            ("✏️ UPDATE", "#3498db", self.update_student),
            ("🗑️ DELETE", "#e74c3c", self.delete_student),
            ("🔄 RESET", "#f39c12", self.reset_form),
            ("📸 CAPTURE PHOTOS", "#9b59b6", self.add_photo_sample),
            ("📊 EXPORT DATA", "#1abc9c", self.export_data),
        ]
        
        for text, color, command in buttons:
            tk.Button(btn_frame, text=text, bg=color, fg='white',
                     font=('Arial', 10, 'bold'), width=18, height=2,
                     command=command).pack(side='left', padx=5)
    
    def create_records_table(self, parent):
        table_frame = tk.LabelFrame(parent, text="Student Records",
                                   font=('Arial', 12, 'bold'), bg='#16213e',
                                   fg='#00ffff', bd=2, relief='raised')
        table_frame.pack(fill='both', expand=True)
        
        # Search bar
        search_frame = tk.Frame(table_frame, bg='#16213e')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="Search:", fg='white', bg='#16213e',
                font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        self.search_combo = ttk.Combobox(search_frame,
                                        values=["Student ID", "Name", "Registration No", "Department"],
                                        width=15, state="readonly")
        self.search_combo.pack(side='left', padx=5)
        self.search_combo.set("Select")
        
        self.search_entry = tk.Entry(search_frame, width=25, font=('Arial', 10))
        self.search_entry.pack(side='left', padx=5)
        
        tk.Button(search_frame, text="🔍 SEARCH", bg='#3498db', fg='white',
                 font=('Arial', 9, 'bold'), command=self.search_student).pack(side='left', padx=5)
        
        tk.Button(search_frame, text="📋 SHOW ALL", bg='#2ecc71', fg='white',
                 font=('Arial', 9, 'bold'), command=self.show_all).pack(side='left', padx=5)
        
        # Statistics
        stats_frame = tk.Frame(search_frame, bg='#16213e')
        stats_frame.pack(side='right', padx=10)
        
        self.stats_label = tk.Label(stats_frame, text="Total Students: 0",
                                    fg='#00ffff', bg='#16213e',
                                    font=('Arial', 10, 'bold'))
        self.stats_label.pack()
        
        # Table
        table_container = tk.Frame(table_frame, bg='#16213e')
        table_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ("ID", "Name", "Reg No", "Dept", "Year", "Sem", "DOB", "Gender", "Email", "Phone")
        self.tree = ttk.Treeview(table_container, columns=columns, show='headings', height=12)
        
        widths = {"ID": 80, "Name": 150, "Reg No": 120, "Dept": 80, 
                 "Year": 100, "Sem": 90, "DOB": 100, "Gender": 70, "Email": 180, "Phone": 110}
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths.get(col, 100))
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        self.tree.bind('<Double-1>', self.on_student_select)
        
        # Style
        style = ttk.Style()
        style.configure("Treeview", background="#2c3e50", foreground="white",
                       fieldbackground="#2c3e50", font=('Arial', 9))
        style.configure("Treeview.Heading", background="#34495e",
                       foreground="white", font=('Arial', 10, 'bold'))
    
    def validate_data(self):
        """Validate student data"""
        if not self.student_id_entry.get().strip():
            messagebox.showerror("Error", "Please enter Student ID!")
            return False
        
        if not self.student_name_entry.get().strip():
            messagebox.showerror("Error", "Please enter Student Name!")
            return False
        
        if self.dept_combo.get() == "Select Department":
            messagebox.showerror("Error", "Please select Department!")
            return False
        
        if self.year_combo.get() == "Select Year":
            messagebox.showerror("Error", "Please select Academic Year!")
            return False
        
        if self.sem_combo.get() == "Select Semester":
            messagebox.showerror("Error", "Please select Semester!")
            return False
        
        try:
            int(self.student_id_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Student ID must be numeric!")
            return False
        
        return True
    
    def save_student(self):
        """Save student to CSV"""
        if not self.validate_data():
            return
        
        student_data = {
            'StudentID': self.student_id_entry.get().strip(),
            'Name': self.student_name_entry.get().strip(),
            'Department': self.dept_combo.get(),
            'Year': self.year_combo.get(),
            'Semester': self.sem_combo.get(),
            'RegistrationNo': self.reg_entry.get().strip(),
            'Gender': self.gender_combo.get(),
            'DOB': self.dob_calendar.get_date().strftime('%d/%m/%Y'),
            'BloodGroup': self.blood_combo.get(),
            'Email': self.email_entry.get().strip(),
            'Phone': self.phone_entry.get().strip(),
            'FatherName': self.father_entry.get().strip(),
            'Address': self.address_entry.get().strip()
        }
        
        if self.student_exists(student_data['StudentID']):
            messagebox.showerror("Error", "Student ID already exists! Use UPDATE instead.")
            return
        
        csv_file = 'student_data/students.csv'
        file_exists = os.path.isfile(csv_file)
        
        try:
            with open(csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=student_data.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(student_data)
            
            self.add_to_tree(student_data)
            messagebox.showinfo("Success", "Student saved successfully!")
            
            if messagebox.askyesno("Photos", "Capture photo samples now?"):
                self.add_photo_sample()
            else:
                self.reset_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def student_exists(self, student_id):
        csv_file = 'student_data/students.csv'
        if not os.path.isfile(csv_file):
            return False
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('StudentID') == student_id:
                        return True
        except:
            pass
        return False
    
    def update_student(self):
        """Update existing student"""
        if not self.validate_data():
            return
        
        student_id = self.student_id_entry.get().strip()
        
        if not self.student_exists(student_id):
            messagebox.showerror("Error", "Student not found! Use SAVE for new students.")
            return
        
        csv_file = 'student_data/students.csv'
        temp_file = 'student_data/students_temp.csv'
        
        student_data = {
            'StudentID': student_id,
            'Name': self.student_name_entry.get().strip(),
            'Department': self.dept_combo.get(),
            'Year': self.year_combo.get(),
            'Semester': self.sem_combo.get(),
            'RegistrationNo': self.reg_entry.get().strip(),
            'Gender': self.gender_combo.get(),
            'DOB': self.dob_calendar.get_date().strftime('%d/%m/%Y'),
            'BloodGroup': self.blood_combo.get(),
            'Email': self.email_entry.get().strip(),
            'Phone': self.phone_entry.get().strip(),
            'FatherName': self.father_entry.get().strip(),
            'Address': self.address_entry.get().strip()
        }
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                students = list(reader)
            
            for i, student in enumerate(students):
                if student['StudentID'] == student_id:
                    students[i] = student_data
                    break
            
            with open(temp_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(students)
            
            os.replace(temp_file, csv_file)
            self.load_students()
            messagebox.showinfo("Success", "Student updated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update: {str(e)}")
    
    def delete_student(self):
        """Delete student"""
        student_id = self.student_id_entry.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Enter Student ID to delete!")
            return
        
        if not self.student_exists(student_id):
            messagebox.showerror("Error", "Student ID not found!")
            return
        
        if not messagebox.askyesno("Confirm", f"Delete student {student_id}?"):
            return
        
        csv_file = 'student_data/students.csv'
        temp_file = 'student_data/students_temp.csv'
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                students = [row for row in reader if row['StudentID'] != student_id]
            
            with open(temp_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(students)
            
            os.replace(temp_file, csv_file)
            self.load_students()
            self.reset_form()
            messagebox.showinfo("Success", "Student deleted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete: {str(e)}")
    
    def reset_form(self):
        """Clear all fields"""
        self.student_id_entry.delete(0, 'end')
        self.student_name_entry.delete(0, 'end')
        self.dept_combo.set("Select Department")
        self.year_combo.set("Select Year")
        self.sem_combo.set("Select Semester")
        self.reg_entry.delete(0, 'end')
        self.gender_combo.set("Male")
        self.dob_calendar.set_date(datetime.now())
        self.blood_combo.set("Select")
        self.email_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.father_entry.delete(0, 'end')
        self.address_entry.delete(0, 'end')
    
    def add_photo_sample(self):
        """Open photo capture"""
        student_id = self.student_id_entry.get().strip()
        student_name = self.student_name_entry.get().strip()
        
        if not student_id or not student_name:
            messagebox.showerror("Error", "Enter Student ID and Name first!")
            return
        
        try:
            from photo_capture_module import PhotoCaptureModule
            PhotoCaptureModule(self.window, student_id=int(student_id), student_name=student_name)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open photo capture: {str(e)}")
    
    def export_data(self):
        """Export to JSON"""
        try:
            csv_file = 'student_data/students.csv'
            json_file = 'student_data/students_export.json'
            
            if not os.path.isfile(csv_file):
                messagebox.showwarning("Warning", "No data to export!")
                return
            
            students = []
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                students = list(reader)
            
            import json
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(students, f, indent=4, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"Data exported to {json_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def load_students(self):
        """Load all students"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        csv_file = 'student_data/students.csv'
        if not os.path.isfile(csv_file):
            return
        
        count = 0
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.add_to_tree(row)
                    count += 1
            self.stats_label.config(text=f"Total Students: {count}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load: {str(e)}")
    
    def add_to_tree(self, data):
        """Add student to treeview"""
        self.tree.insert("", "end", values=(
            data.get('StudentID', ''),
            data.get('Name', ''),
            data.get('RegistrationNo', ''),
            data.get('Department', ''),
            data.get('Year', ''),
            data.get('Semester', ''),
            data.get('DOB', ''),
            data.get('Gender', ''),
            data.get('Email', ''),
            data.get('Phone', '')
        ))
    
    def search_student(self):
        """Search students"""
        search_by = self.search_combo.get()
        search_val = self.search_entry.get().strip()
        
        if search_by == "Select" or not search_val:
            messagebox.showwarning("Warning", "Select search criteria and enter value!")
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        csv_file = 'student_data/students.csv'
        if not os.path.isfile(csv_file):
            messagebox.showinfo("Info", "No student records found!")
            return
        
        search_map = {
            "Student ID": "StudentID",
            "Name": "Name",
            "Registration No": "RegistrationNo",
            "Department": "Department"
        }
        
        found = 0
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                column = search_map.get(search_by)
                
                for row in reader:
                    if search_val.lower() in str(row.get(column, '')).lower():
                        self.add_to_tree(row)
                        found += 1
            
            if found == 0:
                messagebox.showinfo("Search", "No matching records found!")
            else:
                messagebox.showinfo("Search", f"Found {found} matching record(s)!")
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
    
    def show_all(self):
        """Show all students"""
        self.load_students()
    
    def on_student_select(self, event):
        """Populate form on double-click"""
        selected = self.tree.selection()
        if not selected:
            return
        
        values = self.tree.item(selected[0], 'values')
        if not values:
            return
        
        self.reset_form()
        
        self.student_id_entry.insert(0, values[0])
        self.student_name_entry.insert(0, values[1])
        self.reg_entry.insert(0, values[2])
        self.dept_combo.set(values[3])
        self.year_combo.set(values[4])
        self.sem_combo.set(values[5])
        
        # Set DOB from calendar
        try:
            dob_str = values[6]
            if dob_str:
                dob_obj = datetime.strptime(dob_str, '%d/%m/%Y')
                self.dob_calendar.set_date(dob_obj)
        except:
            pass
        
        self.gender_combo.set(values[7])
        self.email_entry.insert(0, values[8])
        self.phone_entry.insert(0, values[9])
        
        # Load additional details
        csv_file = 'student_data/students.csv'
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['StudentID'] == values[0]:
                        self.blood_combo.set(row.get('BloodGroup', 'Select'))
                        self.father_entry.insert(0, row.get('FatherName', ''))
                        self.address_entry.insert(0, row.get('Address', ''))
                        break
        except Exception:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = UpdatedStudentManagement(root)

    root.mainloop()
