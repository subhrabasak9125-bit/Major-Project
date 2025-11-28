# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog
# from datetime import datetime
# import csv
# import os

# class AttendanceViewer:
#     def __init__(self, parent):
#         self.parent = parent
#         self.window = tk.Toplevel(parent)
#         self.window.title("Attendance Viewer & Reports")
#         self.window.geometry("1200x800")
#         self.window.configure(bg='#0a0a2e')
#         self.window.state('zoomed')
        
#         self.window.transient(parent)
#         self.window.grab_set()
        
#         self.create_ui()
#         self.load_attendance_dates()
    
#     def create_ui(self):
#         # Main container
#         main_container = tk.Frame(self.window, bg='#0a0a2e')
#         main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
#         # Title
#         title_label = tk.Label(main_container, text="ATTENDANCE VIEWER & REPORTS",
#                               fg='#00ffff', bg='#0a0a2e', font=('Arial', 24, 'bold'))
#         title_label.pack(pady=(0, 20))
        
#         # Control panel
#         self.create_control_panel(main_container)
        
#         # Attendance table
#         self.create_attendance_table(main_container)
        
#         # Statistics panel
#         self.create_statistics_panel(main_container)
    
#     def create_control_panel(self, parent):
#         control_frame = tk.LabelFrame(parent, text="Attendance Controls",
#                                      font=('Arial', 14, 'bold'), bg='#16213e',
#                                      fg='#00ffff', bd=2, relief='raised')
#         control_frame.pack(fill='x', pady=(0, 20))
        
#         inner_frame = tk.Frame(control_frame, bg='#16213e')
#         inner_frame.pack(padx=20, pady=15)
        
#         # Date selection
#         tk.Label(inner_frame, text="Select Date:", fg='white', bg='#16213e',
#                 font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
#         self.date_combo = ttk.Combobox(inner_frame, width=20, state="readonly")
#         self.date_combo.grid(row=0, column=1, padx=10, pady=10)
#         self.date_combo.bind('<<ComboboxSelected>>', self.on_date_select)
        
#         # Search
#         tk.Label(inner_frame, text="Search Student:", fg='white', bg='#16213e',
#                 font=('Arial', 12, 'bold')).grid(row=0, column=2, padx=10, pady=10, sticky='w')
        
#         self.search_entry = tk.Entry(inner_frame, width=20)
#         self.search_entry.grid(row=0, column=3, padx=10, pady=10)
        
#         tk.Button(inner_frame, text="🔍 SEARCH", bg='#3498db', fg='white',
#                  font=('Arial', 10, 'bold'), width=12,
#                  command=self.search_attendance).grid(row=0, column=4, padx=10, pady=10)
        
#         # Buttons row 2
#         tk.Button(inner_frame, text="📊 TODAY", bg='#2ecc71', fg='white',
#                  font=('Arial', 10, 'bold'), width=12,
#                  command=self.load_today).grid(row=1, column=0, padx=10, pady=10)
        
#         tk.Button(inner_frame, text="📅 ALL DATES", bg='#9b59b6', fg='white',
#                  font=('Arial', 10, 'bold'), width=12,
#                  command=self.load_all_dates).grid(row=1, column=1, padx=10, pady=10)
        
#         tk.Button(inner_frame, text="💾 EXPORT CSV", bg='#f39c12', fg='white',
#                  font=('Arial', 10, 'bold'), width=12,
#                  command=self.export_csv).grid(row=1, column=2, padx=10, pady=10)
        
#         tk.Button(inner_frame, text="📄 EXPORT TXT", bg='#34495e', fg='white',
#                  font=('Arial', 10, 'bold'), width=12,
#                  command=self.export_txt).grid(row=1, column=3, padx=10, pady=10)
        
#         tk.Button(inner_frame, text="🔄 REFRESH", bg='#16a085', fg='white',
#                  font=('Arial', 10, 'bold'), width=12,
#                  command=self.refresh_data).grid(row=1, column=4, padx=10, pady=10)
    
#     def create_attendance_table(self, parent):
#         table_frame = tk.LabelFrame(parent, text="Attendance Records",
#                                    font=('Arial', 14, 'bold'), bg='#16213e',
#                                    fg='#00ffff', bd=2, relief='raised')
#         table_frame.pack(fill='both', expand=True, pady=(0, 20))
        
#         # Create treeview
#         columns = ("StudentID", "Name", "Date", "Time", "Confidence", "Status")
#         self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
#         # Define headings and widths
#         column_widths = {
#             "StudentID": 100,
#             "Name": 200,
#             "Date": 120,
#             "Time": 120,
#             "Confidence": 100,
#             "Status": 100
#         }
        
#         for col in columns:
#             self.tree.heading(col, text=col)
#             self.tree.column(col, width=column_widths[col])
        
#         # Scrollbars
#         vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
#         hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
#         self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
#         # Pack
#         self.tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
#         vsb.pack(side='right', fill='y', pady=10)
#         hsb.pack(side='bottom', fill='x', padx=10)
        
#         # Style
#         style = ttk.Style()
#         style.configure("Treeview", background="#2c3e50", foreground="white",
#                        fieldbackground="#2c3e50", font=('Arial', 10))
#         style.configure("Treeview.Heading", background="#34495e",
#                        foreground="white", font=('Arial', 11, 'bold'))
    
#     def create_statistics_panel(self, parent):
#         stats_frame = tk.LabelFrame(parent, text="Statistics",
#                                    font=('Arial', 14, 'bold'), bg='#16213e',
#                                    fg='#00ffff', bd=2, relief='raised')
#         stats_frame.pack(fill='x')
        
#         inner_frame = tk.Frame(stats_frame, bg='#16213e')
#         inner_frame.pack(padx=20, pady=15)
        
#         # Statistics labels
#         self.total_label = tk.Label(inner_frame, text="Total Records: 0",
#                                    fg='white', bg='#16213e', font=('Arial', 12, 'bold'))
#         self.total_label.grid(row=0, column=0, padx=20, pady=5)
        
#         self.students_label = tk.Label(inner_frame, text="Unique Students: 0",
#                                       fg='#2ecc71', bg='#16213e', font=('Arial', 12, 'bold'))
#         self.students_label.grid(row=0, column=1, padx=20, pady=5)
        
#         self.dates_label = tk.Label(inner_frame, text="Date Range: --",
#                                    fg='#3498db', bg='#16213e', font=('Arial', 12, 'bold'))
#         self.dates_label.grid(row=0, column=2, padx=20, pady=5)
        
#         self.avg_label = tk.Label(inner_frame, text="Avg. Confidence: --",
#                                  fg='#f39c12', bg='#16213e', font=('Arial', 12, 'bold'))
#         self.avg_label.grid(row=0, column=3, padx=20, pady=5)
    
#     def load_attendance_dates(self):
#         """Load available attendance dates"""
#         attendance_dir = "attendance"
#         if not os.path.exists(attendance_dir):
#             os.makedirs(attendance_dir)
#             return
        
#         dates = []
#         for filename in os.listdir(attendance_dir):
#             if filename.startswith("attendance_") and filename.endswith(".csv"):
#                 date_str = filename.replace("attendance_", "").replace(".csv", "")
#                 dates.append(date_str)
        
#         dates.sort(reverse=True)  # Most recent first
#         self.date_combo['values'] = dates
        
#         if dates:
#             self.date_combo.current(0)
#             self.load_attendance_by_date(dates[0])
    
#     def on_date_select(self, event):
#         """Handle date selection"""
#         selected_date = self.date_combo.get()
#         if selected_date:
#             self.load_attendance_by_date(selected_date)
    
#     def load_attendance_by_date(self, date):
#         """Load attendance for specific date"""
#         # Clear existing items
#         for item in self.tree.get_children():
#             self.tree.delete(item)
        
#         filename = f"attendance/attendance_{date}.csv"
#         if not os.path.exists(filename):
#             messagebox.showwarning("Warning", f"No attendance file found for {date}")
#             return
        
#         try:
#             with open(filename, 'r', encoding='utf-8') as file:
#                 reader = csv.DictReader(file)
#                 records = list(reader)
                
#                 for row in records:
#                     self.tree.insert("", "end", values=(
#                         row.get('StudentID', ''),
#                         row.get('Name', ''),
#                         row.get('Date', date),
#                         row.get('Time', ''),
#                         row.get('Confidence', ''),
#                         'Present'
#                     ))
                
#                 # Update statistics
#                 self.update_statistics(records, date)
                
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to load attendance: {str(e)}")
    
#     def load_today(self):
#         """Load today's attendance"""
#         today = datetime.now().strftime("%Y-%m-%d")
        
#         # Update combo box
#         dates = list(self.date_combo['values'])
#         if today not in dates:
#             dates.insert(0, today)
#             self.date_combo['values'] = dates
        
#         self.date_combo.set(today)
#         self.load_attendance_by_date(today)
    
#     def load_all_dates(self):
#         """Load attendance from all dates"""
#         # Clear existing items
#         for item in self.tree.get_children():
#             self.tree.delete(item)
        
#         attendance_dir = "attendance"
#         if not os.path.exists(attendance_dir):
#             messagebox.showinfo("Info", "No attendance records found!")
#             return
        
#         all_records = []
        
#         try:
#             for filename in os.listdir(attendance_dir):
#                 if filename.startswith("attendance_") and filename.endswith(".csv"):
#                     filepath = os.path.join(attendance_dir, filename)
                    
#                     with open(filepath, 'r', encoding='utf-8') as file:
#                         reader = csv.DictReader(file)
#                         for row in reader:
#                             self.tree.insert("", "end", values=(
#                                 row.get('StudentID', ''),
#                                 row.get('Name', ''),
#                                 row.get('Date', ''),
#                                 row.get('Time', ''),
#                                 row.get('Confidence', ''),
#                                 'Present'
#                             ))
#                             all_records.append(row)
            
#             # Update statistics
#             if all_records:
#                 self.update_statistics(all_records, "All Dates")
#             else:
#                 messagebox.showinfo("Info", "No attendance records found!")
                
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to load all attendance: {str(e)}")
    
#     def search_attendance(self):
#         """Search for specific student"""
#         search_term = self.search_entry.get().strip().lower()
        
#         if not search_term:
#             messagebox.showwarning("Warning", "Please enter a search term!")
#             return
        
#         # Clear existing items
#         for item in self.tree.get_children():
#             self.tree.delete(item)
        
#         attendance_dir = "attendance"
#         found_count = 0
#         found_records = []
        
#         try:
#             for filename in os.listdir(attendance_dir):
#                 if filename.startswith("attendance_") and filename.endswith(".csv"):
#                     filepath = os.path.join(attendance_dir, filename)
                    
#                     with open(filepath, 'r', encoding='utf-8') as file:
#                         reader = csv.DictReader(file)
#                         for row in reader:
#                             if (search_term in str(row.get('StudentID', '')).lower() or
#                                 search_term in row.get('Name', '').lower()):
#                                 self.tree.insert("", "end", values=(
#                                     row.get('StudentID', ''),
#                                     row.get('Name', ''),
#                                     row.get('Date', ''),
#                                     row.get('Time', ''),
#                                     row.get('Confidence', ''),
#                                     'Present'
#                                 ))
#                                 found_records.append(row)
#                                 found_count += 1
            
#             if found_count == 0:
#                 messagebox.showinfo("Search Result", "No matching records found!")
#             else:
#                 self.update_statistics(found_records, f"Search: {search_term}")
#                 messagebox.showinfo("Search Result", f"Found {found_count} record(s)!")
                
#         except Exception as e:
#             messagebox.showerror("Error", f"Search failed: {str(e)}")
    
#     def update_statistics(self, records, date_info):
#         """Update statistics display"""
#         if not records:
#             self.total_label.config(text="Total Records: 0")
#             self.students_label.config(text="Unique Students: 0")
#             self.dates_label.config(text="Date Range: --")
#             self.avg_label.config(text="Avg. Confidence: --")
#             return
        
#         total = len(records)
#         unique_students = len(set(row.get('StudentID', '') for row in records))
        
#         # Calculate average confidence
#         confidences = []
#         for row in records:
#             conf_str = row.get('Confidence', '0%').replace('%', '')
#             try:
#                 confidences.append(float(conf_str))
#             except:
#                 pass
        
#         avg_conf = sum(confidences) / len(confidences) if confidences else 0
        
#         self.total_label.config(text=f"Total Records: {total}")
#         self.students_label.config(text=f"Unique Students: {unique_students}")
#         self.dates_label.config(text=f"Date: {date_info}")
#         self.avg_label.config(text=f"Avg. Confidence: {avg_conf:.1f}%")
    
#     def refresh_data(self):
#         """Refresh attendance data"""
#         self.load_attendance_dates()
#         messagebox.showinfo("Success", "Data refreshed successfully!")
    
#     def export_csv(self):
#         """Export attendance to CSV"""
#         items = self.tree.get_children()
#         if not items:
#             messagebox.showwarning("Warning", "No data to export!")
#             return
        
#         filename = filedialog.asksaveasfilename(
#             defaultextension=".csv",
#             filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
#             initialfile=f"attendance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
#         )
        
#         if not filename:
#             return
        
#         try:
#             with open(filename, 'w', newline='', encoding='utf-8') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(["StudentID", "Name", "Date", "Time", "Confidence", "Status"])
                
#                 for item in items:
#                     writer.writerow(self.tree.item(item, 'values'))
            
#             messagebox.showinfo("Success", f"Data exported to:\n{filename}")
            
#         except Exception as e:
#             messagebox.showerror("Error", f"Export failed: {str(e)}")
    
#     def export_txt(self):
#         """Export attendance to text file"""
#         items = self.tree.get_children()
#         if not items:
#             messagebox.showwarning("Warning", "No data to export!")
#             return
        
#         filename = filedialog.asksaveasfilename(
#             defaultextension=".txt",
#             filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
#             initialfile=f"attendance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
#         )
        
#         if not filename:
#             return
        
#         try:
#             with open(filename, 'w', encoding='utf-8') as file:
#                 file.write("=" * 80 + "\n")
#                 file.write("ATTENDANCE REPORT\n")
#                 file.write("=" * 80 + "\n")
#                 file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
#                 file.write(f"Total Records: {len(items)}\n")
#                 file.write("=" * 80 + "\n\n")
                
#                 file.write(f"{'StudentID':<12} {'Name':<25} {'Date':<12} {'Time':<12} {'Confidence':<12} {'Status':<10}\n")
#                 file.write("-" * 80 + "\n")
                
#                 for item in items:
#                     values = self.tree.item(item, 'values')
#                     file.write(f"{values[0]:<12} {values[1]:<25} {values[2]:<12} {values[3]:<12} {values[4]:<12} {values[5]:<10}\n")
                
#                 file.write("\n" + "=" * 80 + "\n")
            
#             messagebox.showinfo("Success", f"Report exported to:\n{filename}")
            
#         except Exception as e:
#             messagebox.showerror("Error", f"Export failed: {str(e)}")

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.withdraw()
#     app = AttendanceViewer(root)
#     root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv
import os

class AttendanceViewer:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Attendance Viewer & Reports")
        self.window.geometry("1400x850")
        self.window.configure(bg='#0a0a2e')
        self.window.state('zoomed')
        
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_ui()
        self.load_attendance_dates()
    
    def create_ui(self):
        # Main container with gradient effect
        main_container = tk.Frame(self.window, bg='#0a0a2e')
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Modern Header
        self.create_modern_header(main_container)
        
        # Enhanced Control panel
        self.create_enhanced_control_panel(main_container)
        
        # Modern Attendance table
        self.create_modern_attendance_table(main_container)
        
        # Enhanced Statistics panel
        self.create_enhanced_statistics_panel(main_container)
    
    def create_modern_header(self, parent):
        """Create a modern header with gradient-like effect"""
        header_frame = tk.Frame(parent, bg='#16213e', height=80)
        header_frame.pack(fill='x', pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Left side - Title with icon
        left_frame = tk.Frame(header_frame, bg='#16213e')
        left_frame.pack(side='left', padx=20, pady=15)
        
        title_label = tk.Label(left_frame, 
                              text="📊 ATTENDANCE VIEWER & REPORTS",
                              fg='#00ffff', bg='#16213e', 
                              font=('Arial', 22, 'bold'))
        title_label.pack()
        
        subtitle_label = tk.Label(left_frame,
                                 text="Real-time Attendance Management System",
                                 fg='#95a5a6', bg='#16213e',
                                 font=('Arial', 10))
        subtitle_label.pack()
        
        # Right side - Date and time
        right_frame = tk.Frame(header_frame, bg='#16213e')
        right_frame.pack(side='right', padx=20, pady=15)
        
        self.datetime_label = tk.Label(right_frame,
                                      text="",
                                      fg='#00ffff', bg='#16213e',
                                      font=('Arial', 12, 'bold'))
        self.datetime_label.pack()
        self.update_datetime()
    
    def update_datetime(self):
        """Update date and time display"""
        current_datetime = datetime.now().strftime("%I:%M:%S %p • %d %B %Y")
        self.datetime_label.config(text=current_datetime)
        if self.window.winfo_exists():
            self.window.after(1000, self.update_datetime)
    
    def create_enhanced_control_panel(self, parent):
        """Enhanced control panel with modern card design"""
        control_frame = tk.LabelFrame(parent, 
                                     text="🔍 Search & Filter Controls",
                                     font=('Arial', 13, 'bold'), 
                                     bg='#16213e',
                                     fg='#00ffff', 
                                     bd=3, 
                                     relief='raised')
        control_frame.pack(fill='x', pady=(0, 15))
        
        inner_frame = tk.Frame(control_frame, bg='#16213e')
        inner_frame.pack(padx=25, pady=20)
        
        # Row 1: Date selection and Search
        row1 = tk.Frame(inner_frame, bg='#16213e')
        row1.pack(fill='x', pady=(0, 15))
        
        # Date selection card
        date_card = tk.Frame(row1, bg='#1e2940', relief='groove', bd=2)
        date_card.pack(side='left', padx=(0, 20), fill='x', expand=True)
        
        tk.Label(date_card, 
                text="📅 Select Date:", 
                fg='white', bg='#1e2940',
                font=('Arial', 11, 'bold')).pack(side='left', padx=15, pady=12)
        
        style = ttk.Style()
        style.configure('Custom.TCombobox', 
                       fieldbackground='#2c3e50',
                       background='#34495e',
                       foreground='white',
                       arrowcolor='#00ffff')
        
        self.date_combo = ttk.Combobox(date_card, 
                                      width=22, 
                                      state="readonly",
                                      font=('Arial', 10),
                                      style='Custom.TCombobox')
        self.date_combo.pack(side='left', padx=10, pady=12)
        self.date_combo.bind('<<ComboboxSelected>>', self.on_date_select)
        
        # Search card
        search_card = tk.Frame(row1, bg='#1e2940', relief='groove', bd=2)
        search_card.pack(side='left', fill='x', expand=True)
        
        tk.Label(search_card, 
                text="🔎 Search Student:", 
                fg='white', bg='#1e2940',
                font=('Arial', 11, 'bold')).pack(side='left', padx=15, pady=12)
        
        self.search_entry = tk.Entry(search_card, 
                                     width=25,
                                     font=('Arial', 10),
                                     bg='#2c3e50',
                                     fg='white',
                                     insertbackground='white',
                                     relief='flat',
                                     bd=5)
        self.search_entry.pack(side='left', padx=10, pady=12)
        
        search_btn = tk.Button(search_card, 
                              text="🔍 SEARCH",
                              bg='#3498db', fg='white',
                              font=('Arial', 10, 'bold'),
                              width=12,
                              height=1,
                              relief='flat',
                              cursor='hand2',
                              activebackground='#2980b9',
                              command=self.search_attendance)
        search_btn.pack(side='left', padx=15, pady=8)
        
        # Row 2: Action buttons with modern styling
        row2 = tk.Frame(inner_frame, bg='#16213e')
        row2.pack(fill='x')
        
        button_configs = [
            ("📊 TODAY", "#2ecc71", "#27ae60", self.load_today),
            ("📅 ALL DATES", "#9b59b6", "#8e44ad", self.load_all_dates),
            ("💾 EXPORT CSV", "#f39c12", "#e67e22", self.export_csv),
            ("📄 EXPORT TXT", "#34495e", "#2c3e50", self.export_txt),
            ("🔄 REFRESH", "#16a085", "#138d75", self.refresh_data),
        ]
        
        for text, bg, active_bg, command in button_configs:
            btn = tk.Button(row2, 
                           text=text,
                           bg=bg, 
                           fg='white',
                           font=('Arial', 10, 'bold'),
                           width=15,
                           height=2,
                           relief='flat',
                           cursor='hand2',
                           activebackground=active_bg,
                           command=command)
            btn.pack(side='left', padx=8)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn, c=active_bg: b.config(bg=c))
            btn.bind('<Leave>', lambda e, b=btn, c=bg: b.config(bg=c))
    
    def create_modern_attendance_table(self, parent):
        """Create a modern table with enhanced styling"""
        table_frame = tk.LabelFrame(parent, 
                                   text="📋 Attendance Records",
                                   font=('Arial', 13, 'bold'), 
                                   bg='#16213e',
                                   fg='#00ffff', 
                                   bd=3, 
                                   relief='raised')
        table_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Table container with padding
        table_container = tk.Frame(table_frame, bg='#16213e')
        table_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Create custom style for treeview
        style = ttk.Style()
        
        # Configure treeview colors
        style.configure("Modern.Treeview",
                       background="#2c3e50",
                       foreground="white",
                       fieldbackground="#2c3e50",
                       font=('Arial', 10),
                       rowheight=30)
        
        style.configure("Modern.Treeview.Heading",
                       background="#34495e",
                       foreground="#00ffff",
                       font=('Arial', 11, 'bold'),
                       relief='flat')
        
        # Map for selected items
        style.map('Modern.Treeview',
                 background=[('selected', '#3498db')],
                 foreground=[('selected', 'white')])
        
        # Create treeview
        columns = ("StudentID", "Name", "Date", "Time", "Confidence", "Status")
        self.tree = ttk.Treeview(table_container, 
                                columns=columns, 
                                show='headings', 
                                height=15,
                                style="Modern.Treeview")
        
        # Define column widths and headings
        column_config = {
            "StudentID": (100, "🆔 Student ID"),
            "Name": (220, "👤 Name"),
            "Date": (130, "📅 Date"),
            "Time": (130, "🕐 Time"),
            "Confidence": (120, "✓ Confidence"),
            "Status": (120, "📊 Status")
        }
        
        for col, (width, heading) in column_config.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor='center')
        
        # Modern scrollbars
        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        # Add alternating row colors
        self.tree.tag_configure('oddrow', background='#2c3e50')
        self.tree.tag_configure('evenrow', background='#34495e')
    
    def create_enhanced_statistics_panel(self, parent):
        """Enhanced statistics panel with card design"""
        stats_frame = tk.LabelFrame(parent, 
                                   text="📈 Statistics Dashboard",
                                   font=('Arial', 13, 'bold'), 
                                   bg='#16213e',
                                   fg='#00ffff', 
                                   bd=3, 
                                   relief='raised')
        stats_frame.pack(fill='x')
        
        inner_frame = tk.Frame(stats_frame, bg='#16213e')
        inner_frame.pack(padx=25, pady=20)
        
        # Configure grid
        for i in range(4):
            inner_frame.columnconfigure(i, weight=1, uniform='stat')
        
        # Statistics cards
        stats_config = [
            ("📊 Total Records", "0", "#3498db", "total_label"),
            ("👥 Unique Students", "0", "#2ecc71", "students_label"),
            ("📅 Date Range", "--", "#9b59b6", "dates_label"),
            ("✓ Avg. Confidence", "--", "#f39c12", "avg_label")
        ]
        
        for idx, (title, value, color, attr_name) in enumerate(stats_config):
            # Create card
            card = tk.Frame(inner_frame, bg='#1e2940', relief='raised', bd=3)
            card.grid(row=0, column=idx, padx=12, pady=5, sticky='nsew')
            
            # Icon/Title
            title_label = tk.Label(card, 
                                  text=title,
                                  fg='#95a5a6', 
                                  bg='#1e2940',
                                  font=('Arial', 10, 'bold'))
            title_label.pack(pady=(15, 5))
            
            # Value
            value_label = tk.Label(card, 
                                  text=value,
                                  fg=color, 
                                  bg='#1e2940',
                                  font=('Arial', 18, 'bold'))
            value_label.pack(pady=(0, 15))
            
            # Store reference
            setattr(self, attr_name, value_label)
    
    # All the original methods remain the same
    def load_attendance_dates(self):
        """Load available attendance dates"""
        attendance_dir = "attendance"
        if not os.path.exists(attendance_dir):
            os.makedirs(attendance_dir)
            return
        
        dates = []
        for filename in os.listdir(attendance_dir):
            if filename.startswith("attendance_") and filename.endswith(".csv"):
                date_str = filename.replace("attendance_", "").replace(".csv", "")
                dates.append(date_str)
        
        dates.sort(reverse=True)
        self.date_combo['values'] = dates
        
        if dates:
            self.date_combo.current(0)
            self.load_attendance_by_date(dates[0])
    
    def on_date_select(self, event):
        """Handle date selection"""
        selected_date = self.date_combo.get()
        if selected_date:
            self.load_attendance_by_date(selected_date)
    
    def load_attendance_by_date(self, date):
        """Load attendance for specific date"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filename = f"attendance/attendance_{date}.csv"
        if not os.path.exists(filename):
            messagebox.showwarning("Warning", f"No attendance file found for {date}")
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                records = list(reader)
                
                for idx, row in enumerate(records):
                    # Alternate row colors
                    tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                    
                    self.tree.insert("", "end", 
                                   values=(
                                       row.get('StudentID', ''),
                                       row.get('Name', ''),
                                       row.get('Date', date),
                                       row.get('Time', ''),
                                       row.get('Confidence', ''),
                                       '✓ Present'
                                   ),
                                   tags=(tag,))
                
                self.update_statistics(records, date)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load attendance: {str(e)}")
    
    def load_today(self):
        """Load today's attendance"""
        today = datetime.now().strftime("%Y-%m-%d")
        dates = list(self.date_combo['values'])
        if today not in dates:
            dates.insert(0, today)
            self.date_combo['values'] = dates
        
        self.date_combo.set(today)
        self.load_attendance_by_date(today)
    
    def load_all_dates(self):
        """Load attendance from all dates"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        attendance_dir = "attendance"
        if not os.path.exists(attendance_dir):
            messagebox.showinfo("Info", "No attendance records found!")
            return
        
        all_records = []
        
        try:
            for filename in os.listdir(attendance_dir):
                if filename.startswith("attendance_") and filename.endswith(".csv"):
                    filepath = os.path.join(attendance_dir, filename)
                    
                    with open(filepath, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file)
                        for idx, row in enumerate(reader):
                            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                            
                            self.tree.insert("", "end", 
                                           values=(
                                               row.get('StudentID', ''),
                                               row.get('Name', ''),
                                               row.get('Date', ''),
                                               row.get('Time', ''),
                                               row.get('Confidence', ''),
                                               '✓ Present'
                                           ),
                                           tags=(tag,))
                            all_records.append(row)
            
            if all_records:
                self.update_statistics(all_records, "All Dates")
            else:
                messagebox.showinfo("Info", "No attendance records found!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load all attendance: {str(e)}")
    
    def search_attendance(self):
        """Search for specific student"""
        search_term = self.search_entry.get().strip().lower()
        
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term!")
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        attendance_dir = "attendance"
        found_count = 0
        found_records = []
        
        try:
            for filename in os.listdir(attendance_dir):
                if filename.startswith("attendance_") and filename.endswith(".csv"):
                    filepath = os.path.join(attendance_dir, filename)
                    
                    with open(filepath, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file)
                        for idx, row in enumerate(reader):
                            if (search_term in str(row.get('StudentID', '')).lower() or
                                search_term in row.get('Name', '').lower()):
                                
                                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                                
                                self.tree.insert("", "end", 
                                               values=(
                                                   row.get('StudentID', ''),
                                                   row.get('Name', ''),
                                                   row.get('Date', ''),
                                                   row.get('Time', ''),
                                                   row.get('Confidence', ''),
                                                   '✓ Present'
                                               ),
                                               tags=(tag,))
                                found_records.append(row)
                                found_count += 1
            
            if found_count == 0:
                messagebox.showinfo("Search Result", "No matching records found!")
            else:
                self.update_statistics(found_records, f"Search: {search_term}")
                messagebox.showinfo("Search Result", f"Found {found_count} record(s)!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
    
    def update_statistics(self, records, date_info):
        """Update statistics display"""
        if not records:
            self.total_label.config(text="0")
            self.students_label.config(text="0")
            self.dates_label.config(text="--")
            self.avg_label.config(text="--")
            return
        
        total = len(records)
        unique_students = len(set(row.get('StudentID', '') for row in records))
        
        confidences = []
        for row in records:
            conf_str = row.get('Confidence', '0%').replace('%', '')
            try:
                confidences.append(float(conf_str))
            except:
                pass
        
        avg_conf = sum(confidences) / len(confidences) if confidences else 0
        
        self.total_label.config(text=str(total))
        self.students_label.config(text=str(unique_students))
        self.dates_label.config(text=str(date_info))
        self.avg_label.config(text=f"{avg_conf:.1f}%")
    
    def refresh_data(self):
        """Refresh attendance data"""
        self.load_attendance_dates()
        messagebox.showinfo("Success", "Data refreshed successfully!")
    
    def export_csv(self):
        """Export attendance to CSV"""
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning("Warning", "No data to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"attendance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["StudentID", "Name", "Date", "Time", "Confidence", "Status"])
                
                for item in items:
                    writer.writerow(self.tree.item(item, 'values'))
            
            messagebox.showinfo("Success", f"Data exported to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def export_txt(self):
        """Export attendance to text file"""
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning("Warning", "No data to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"attendance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("=" * 80 + "\n")
                file.write("ATTENDANCE REPORT\n")
                file.write("=" * 80 + "\n")
                file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"Total Records: {len(items)}\n")
                file.write("=" * 80 + "\n\n")
                
                file.write(f"{'StudentID':<12} {'Name':<25} {'Date':<12} {'Time':<12} {'Confidence':<12} {'Status':<10}\n")
                file.write("-" * 80 + "\n")
                
                for item in items:
                    values = self.tree.item(item, 'values')
                    file.write(f"{values[0]:<12} {values[1]:<25} {values[2]:<12} {values[3]:<12} {values[4]:<12} {values[5]:<10}\n")
                
                file.write("\n" + "=" * 80 + "\n")
            
            messagebox.showinfo("Success", f"Report exported to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = AttendanceViewer(root)
    root.mainloop()