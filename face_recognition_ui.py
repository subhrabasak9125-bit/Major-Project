
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import threading
import time

try:
    import customtkinter as ctk
except ImportError:
    raise ImportError("Install: pip install customtkinter")

from PIL import Image, ImageTk
import cv2
import json

# Chart libraries
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import matplotlib.animation as animation
    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False
    print("Install matplotlib for charts: pip install matplotlib")

# Import modules
try:
    from statistics_module import RealTimeStatistics
    STATS_AVAILABLE = True
except ImportError:
    STATS_AVAILABLE = False

try:
    from disha_ultra_internet import UltraDISHAWithInternet
    DISHA_AVAILABLE = True
except ImportError:
    DISHA_AVAILABLE = False
    print("DISHA Ultra will be created")

# Configuration
VIDEO_PATH = "WhatsApp Video 2025-11-17 at 23.41.36_2c9c66ab.mp4"


class UltraAdvancedDashboard:
    """Ultimate Advanced Dashboard with Full Visualizations"""
    
    def __init__(self, root=None):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = root or ctk.CTk()
        self.root.title("🚀 SMIT Ultra-Advanced Face Recognition System")
        self.root.geometry("1920x1080")
        
        try:
            self.root.state("zoomed")
        except:
            pass
        
        # Initialize state
        self._init_state()
        self._init_video()
        
        # Build ultra UI
        self.build_ultra_dashboard()
        
        # Start all updates
        self._start_all_updates()
    
    def _init_state(self):
        """Initialize application state"""
        self.running = True
        self.stats_module = RealTimeStatistics() if STATS_AVAILABLE else None
        self.disha = None
        self.disha_active = False
        
        # Chart data storage
        self.chart_data = {
            'attendance_history': [],
            'hourly_data': [],
            'department_data': {},
            'weekly_trends': []
        }
        
        # Animation states
        self.animation_state = 0
        self.notification_queue = []
        
        # Live data cache
        self.live_data_cache = {}
        self.last_cache_update = None
    
    def _init_video(self):
        """Initialize video background"""
        self.cap = None
        self.video_enabled = False
        
        if os.path.exists(VIDEO_PATH):
            try:
                self.cap = cv2.VideoCapture(VIDEO_PATH)
                self.video_enabled = True
            except:
                pass
    
    def build_ultra_dashboard(self):
        """Build the ultimate dashboard UI"""
        
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#000000")
        self.main_frame.pack(fill="both", expand=True)
        
        # Video background
        if self.video_enabled:
            self.video_canvas = tk.Canvas(self.main_frame, bg="#000000",
                                         highlightthickness=0)
            self.video_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Glassmorphic overlay
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=("#05050F", "#05050F")

        )
        self.content_frame.place(relx=0.005, rely=0.005, relwidth=0.99, relheight=0.99)
        
        # Build all sections
        self.build_top_bar()
        self.build_main_dashboard()
        self.build_floating_controls()
        self.build_notifications()
    
    def build_top_bar(self):
        """Build animated top bar with system info"""
        top_bar = ctk.CTkFrame(self.content_frame, height=80, 
                              fg_color=("gray10", "gray10"), corner_radius=15)
        top_bar.pack(fill="x", padx=10, pady=10)
        top_bar.pack_propagate(False)
        
        # Left: Animated logo and title
        left_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        left_frame.pack(side="left", padx=20)
        
        self.title_label = ctk.CTkLabel(
            left_frame,
            text="🚀 SMIT ULTRA-ADVANCED AI SYSTEM",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#00d9ff"
        )
        self.title_label.pack(anchor="w", pady=(8, 0))
        
        subtitle = ctk.CTkLabel(
            left_frame,
            text="Real-Time Biometric Intelligence • AI-Powered Analytics • Internet-Enabled Assistant",
            font=ctk.CTkFont(size=11),
            text_color="gray60"
        )
        subtitle.pack(anchor="w")
        
        # Center: Live stats ticker
        center_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        center_frame.pack(side="left", expand=True, padx=30)
        
        self.ticker_label = ctk.CTkLabel(
            center_frame,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#00ff00"
        )
        self.ticker_label.pack()
        
        # Right: Clock and controls
        right_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        right_frame.pack(side="right", padx=20)
        
        self.clock_label = ctk.CTkLabel(
            right_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00d9ff"
        )
        self.clock_label.pack(pady=(5, 0))
        
        # System status
        self.system_status = ctk.CTkLabel(
            right_frame,
            text="● SYSTEM ONLINE",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#00ff00"
        )
        self.system_status.pack()
    
    def build_main_dashboard(self):
        """Build main dashboard with charts and stats"""
        
        # Main content area
        main_content = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Left panel: Stats and charts (70%)
        left_panel = ctk.CTkFrame(main_content, fg_color="transparent")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Stats cards row
        self.build_stats_cards(left_panel)
        
        # Charts grid
        self.build_charts_grid(left_panel)
        
        # Right panel: Controls and activity (30%)
        right_panel = ctk.CTkFrame(main_content, fg_color="transparent")
        right_panel.pack(side="right", fill="both", padx=(5, 0))
        
        self.build_control_panel(right_panel)
        self.build_activity_feed(right_panel)
    
    def build_stats_cards(self, parent):
        """Build animated statistics cards"""
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent", height=140)
        cards_frame.pack(fill="x", pady=(0, 10))
        cards_frame.pack_propagate(False)
        
        # Get real stats
        if self.stats_module:
            stats_data = self.stats_module.get_all_statistics()
        else:
            stats_data = {
                'total_students': 0,
                'present_today': 0,
                'photos_collected': 0,
                'models_trained': 0
            }
        
        stats = [
            ("👥 STUDENTS", stats_data['total_students'], "#3498db", "📚 Enrolled"),
            ("✅ PRESENT", stats_data['present_today'], "#2ecc71", "🎯 Today"),
            ("📸 SAMPLES", stats_data['photos_collected'], "#9b59b6", "🔬 Collected"),
            ("🧠 AI MODEL", stats_data['models_trained'], "#f39c12", "⚡ Trained")
        ]
        
        self.stat_cards = []
        
        for i in range(4):
            cards_frame.columnconfigure(i, weight=1)
        
        for i, (label, value, color, subtitle) in enumerate(stats):
            # 3D card container
            card_container = ctk.CTkFrame(cards_frame, fg_color="transparent")
            card_container.grid(row=0, column=i, padx=8, sticky="nsew")
            
            # Shadow layers for 3D effect
            shadow3 = ctk.CTkFrame(card_container, fg_color="#000000", 
                                  corner_radius=20)
            shadow3.place(relx=0.04, rely=0.04, relwidth=0.96, relheight=0.96)
            
            shadow2 = ctk.CTkFrame(card_container, fg_color="#0a0a0a",
                                  corner_radius=20)
            shadow2.place(relx=0.03, rely=0.03, relwidth=0.97, relheight=0.97)
            
            shadow1 = ctk.CTkFrame(card_container, fg_color="#141414",
                                  corner_radius=20)
            shadow1.place(relx=0.02, rely=0.02, relwidth=0.98, relheight=0.98)
            
            # Main card with gradient
            card = ctk.CTkFrame(
                card_container,
                fg_color=("gray12", "gray12"),
                corner_radius=20,
                border_width=3,
                border_color=color
            )
            card.place(relx=0, rely=0, relwidth=1, relheight=1)
            
            # Glow effect on hover
            card.bind("<Enter>", lambda e, c=card, col=color: 
                     c.configure(border_color=self.brighten_color(col), border_width=4))
            card.bind("<Leave>", lambda e, c=card, col=color:
                     c.configure(border_color=col, border_width=3))
            
            # Label
            tk.Label(card, text=label, fg=color, bg="#1a1a1a",
                    font=("Arial", 11, "bold")).pack(pady=(15, 5))
            
            # Value with pulsing effect
            value_label = tk.Label(card, text=str(value), fg="white",
                                  bg="#1a1a1a", font=("Arial", 36, "bold"))
            value_label.pack(pady=(0, 5))
            
            # Subtitle
            tk.Label(card, text=subtitle, fg="gray60", bg="#1a1a1a",
                    font=("Arial", 9)).pack(pady=(0, 15))
            
            self.stat_cards.append(value_label)
    
    def build_charts_grid(self, parent):
        """Build interactive charts grid"""
        charts_frame = ctk.CTkFrame(parent, fg_color="transparent")
        charts_frame.pack(fill="both", expand=True)
        
        # Configure grid
        charts_frame.rowconfigure(0, weight=1)
        charts_frame.rowconfigure(1, weight=1)
        charts_frame.columnconfigure(0, weight=1)
        charts_frame.columnconfigure(1, weight=1)
        
        if CHARTS_AVAILABLE:
            # Chart 1: Attendance Trends (Top Left)
            self.create_attendance_trend_chart(charts_frame, 0, 0)
            
            # Chart 2: Department Distribution (Top Right)
            self.create_department_pie_chart(charts_frame, 0, 1)
            
            # Chart 3: Weekly Performance (Bottom Left)
            self.create_weekly_bar_chart(charts_frame, 1, 0)
            
            # Chart 4: Real-Time Activity (Bottom Right)
            self.create_realtime_line_chart(charts_frame, 1, 1)
        else:
            # Fallback: Text-based stats
            for i in range(2):
                for j in range(2):
                    placeholder = ctk.CTkFrame(charts_frame, 
                                              fg_color=("gray12", "gray12"),
                                              corner_radius=15)
                    placeholder.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                    
                    ctk.CTkLabel(placeholder, 
                                text="📊 Install matplotlib\nfor live charts",
                                font=ctk.CTkFont(size=16),
                                text_color="gray50").pack(expand=True)
    
    def create_attendance_trend_chart(self, parent, row, col):
        """Create animated attendance trend line chart"""
        chart_frame = ctk.CTkFrame(parent, fg_color=("gray12", "gray12"),
                                   corner_radius=15)
        chart_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # Title
        ctk.CTkLabel(chart_frame, text="📈 Attendance Trends (Last 7 Days)",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#00d9ff").pack(pady=(10, 5))
        
        # Matplotlib figure
        fig = Figure(figsize=(5, 3), facecolor='#1a1a1a')
        ax = fig.add_subplot(111, facecolor='#1a1a1a')
        
        # Sample data
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        attendance = self.stats_module.get_last_7_days_attendance()

        
        ax.plot(days, attendance, color='#00d9ff', linewidth=2, marker='o',
               markersize=6, markerfacecolor='#00ff00')
        ax.fill_between(days, attendance, alpha=0.3, color='#00d9ff')
        
        ax.set_ylabel('Students', color='white', fontsize=10)
        ax.tick_params(colors='white', labelsize=8)
        ax.grid(True, alpha=0.2, color='gray')
        ax.spines['bottom'].set_color('gray')
        ax.spines['top'].set_color('gray')
        ax.spines['left'].set_color('gray')
        ax.spines['right'].set_color('gray')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def create_department_pie_chart(self, parent, row, col):
        """Create department distribution pie chart"""
        chart_frame = ctk.CTkFrame(parent, fg_color=("gray12", "gray12"),
                                   corner_radius=15)
        chart_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(chart_frame, text="🎓 Department Distribution",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#00d9ff").pack(pady=(10, 5))
        
        fig = Figure(figsize=(5, 3), facecolor='#1a1a1a')
        ax = fig.add_subplot(111, facecolor='#1a1a1a')
        
        dept_data = self.stats_module.get_department_distribution()
        departments = list(dept_data.keys())
        sizes = list(dept_data.values())

        colors = ['#3498db', '#2ecc71', '#9b59b6', '#f39c12', '#e74c3c']
        
        ax.pie(sizes, labels=departments, colors=colors, autopct='%1.1f%%',
              startangle=90, textprops={'color': 'white', 'fontsize': 9})
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def create_weekly_bar_chart(self, parent, row, col):
        """Create weekly performance bar chart"""
        chart_frame = ctk.CTkFrame(parent, fg_color=("gray12", "gray12"),
                                   corner_radius=15)
        chart_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(chart_frame, text="📊 Weekly Performance",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#00d9ff").pack(pady=(10, 5))
        
        fig = Figure(figsize=(5, 3), facecolor='#1a1a1a')
        ax = fig.add_subplot(111, facecolor='#1a1a1a')
        
        weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
        present = self.stats_module.get_weekly_performance()
        absent = [12, 8, 15, 10]
        
        x = range(len(weeks))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], present, width, label='Present',
              color='#2ecc71')
        ax.bar([i + width/2 for i in x], absent, width, label='Absent',
              color='#e74c3c')
        
        ax.set_ylabel('Students', color='white', fontsize=10)
        ax.set_xticks(x)
        ax.set_xticklabels(weeks)
        ax.tick_params(colors='white', labelsize=8)
        ax.legend(facecolor='#1a1a1a', labelcolor='white', fontsize=8)
        ax.grid(True, alpha=0.2, color='gray', axis='y')
        
        for spine in ax.spines.values():
            spine.set_color('gray')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def create_realtime_line_chart(self, parent, row, col):
        """Create real-time activity line chart"""
        chart_frame = ctk.CTkFrame(parent, fg_color=("gray12", "gray12"),
                                   corner_radius=15)
        chart_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(chart_frame, text="⚡ Real-Time Activity",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#00d9ff").pack(pady=(10, 5))
        
        fig = Figure(figsize=(5, 3), facecolor='#1a1a1a')
        ax = fig.add_subplot(111, facecolor='#1a1a1a')
        
        raw = self.stats_module.get_realtime_activity_counts()
        activity = list(range(1, len(raw) + 1))
        times = raw

        
        ax.plot(times, activity, color='#f39c12', linewidth=2, marker='s',
               markersize=6, markerfacecolor='#ff0000')
        ax.fill_between(times, activity, alpha=0.3, color='#f39c12')
        
        ax.set_ylabel('Check-ins', color='white', fontsize=10)
        ax.tick_params(colors='white', labelsize=8)
        ax.grid(True, alpha=0.2, color='gray')
        
        for spine in ax.spines.values():
            spine.set_color('gray')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def build_control_panel(self, parent):
        """Build control panel with module buttons"""
        control_frame = ctk.CTkFrame(parent, fg_color=("gray10", "gray10"),
                                     corner_radius=15)
        control_frame.pack(fill="both", expand=True, pady=(0, 10))

    # Title
        ctk.CTkLabel(control_frame, text="🎮 SYSTEM CONTROLS",
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color="#00d9ff").pack(pady=(15, 10))

    # Scrollable frame for buttons - match parent background
        scroll_frame = ctk.CTkScrollableFrame(
            control_frame,
            fg_color=("gray10", "gray10")  # Match control_frame background
        )
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # Make internal components completely invisible
        try:
        # Make scrollable frame background match parent
            scroll_frame._scrollable_frame.configure(fg_color=("gray10", "gray10"))
        
        # Make canvas completely transparent initially
            scroll_frame._canvas.configure(bg="gray10", highlightthickness=0)
        
        # Remove any borders
            scroll_frame.configure(border_width=0)
        
        except Exception as e:
            print("Scroll background configuration failed:", e)

    # Function to handle scroll appearance
        def handle_scroll_visibility(*args):
            try:
            # Get scroll position
                y1, y2 = scroll_frame._canvas.yview()
            
            # If we can scroll (content is larger than visible area)
                if y1 > 0.0 or y2 < 1.0:
                # Show very subtle background only when scrolling is possible
                    scroll_frame._canvas.configure(bg="#0a0a0a")
                else:
                # Completely transparent when no scrolling needed
                    scroll_frame._canvas.configure(bg="")
            except:
                pass

    # Apply scroll detection
        try:
        # Bind to scroll events
            scroll_frame._canvas.bind("<Configure>", handle_scroll_visibility)
            scroll_frame._scrollable_frame.bind("<Configure>", handle_scroll_visibility)
        
        # Also check after a short delay when UI is fully loaded
            self.root.after(500, handle_scroll_visibility)
        
        except Exception as e:
            print("Scroll binding failed:", e)

        modules = [
            ("👥 Students", self.open_students, "#3498db"),
            ("🔐 Face Recognition", self.open_recognition, "#2ecc71"),
            ("📊 Attendance", self.open_attendance, "#9b59b6"),
            ("🧠 Train AI", self.open_training, "#e74c3c"),
            ("📸 Capture Photos", self.open_photos, "#1abc9c"),
            ("❓ Help", self.open_help, "#e67e22"),
            ("💻 Developer", self.open_developer, "#34495e"),
            ("🚪 Exit", self.exit_app, "#c0392b")
        ]
    
        for text, cmd, color in modules:
            btn = ctk.CTkButton(
                scroll_frame,
                text=text,
                command=cmd,
                fg_color=color,
                hover_color=self.brighten_color(color),
                height=45,
                font=ctk.CTkFont(size=13, weight="bold"),
                corner_radius=10,
                border_width=2,
                border_color=self.brighten_color(color)
            )
            btn.pack(fill="x", pady=5)
    
    # Final check after all buttons are added
        self.root.after(1000, handle_scroll_visibility) 
            
    

    
    def build_activity_feed(self, parent):
        """Build live activity feed"""
        activity_frame = ctk.CTkFrame(parent, fg_color=("gray10", "gray10"),
                                      corner_radius=15)
        activity_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(activity_frame, text="🔴 LIVE ACTIVITY FEED",
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color="#00d9ff").pack(pady=(15, 10))
        
        # Scrollable activity list
        self.activity_scroll = ctk.CTkScrollableFrame(activity_frame,
                                                      fg_color="transparent")
        self.activity_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.update_activity_feed()
    
    def build_floating_controls(self):
        """Build floating DISHA and quick action buttons"""
        
        # DISHA floating button (bottom right)
        disha_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        disha_container.place(relx=0.96, rely=0.92, anchor="center")
        
        # Outer glow
        glow = ctk.CTkFrame(disha_container, width=130, height=130,
                           corner_radius=65, fg_color="#7b2ff7")
        glow.pack()
        
        # Main DISHA button
        self.disha_btn = ctk.CTkButton(
            disha_container,
            text="🎤\nDISHA\nULTRA",
            width=120,
            height=120,
            corner_radius=60,
            fg_color=("#9b59b6", "#8e44ad"),
            hover_color="#7d3c98",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.toggle_disha,
            border_width=4,
            border_color="#bb87dd"
        )
        self.disha_btn.place(relx=0.5, rely=0.5, anchor="center")
        
        # Status indicator
        self.disha_status = ctk.CTkLabel(
            disha_container,
            text="●",
            font=ctk.CTkFont(size=24),
            text_color="#ff4444"
        )
        self.disha_status.place(relx=0.82, rely=0.18, anchor="center")
        
        # Quick actions (top right)
        actions_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        actions_frame.place(relx=0.98, rely=0.08, anchor="e")
        
        quick_actions = [
            ("🔄", self.refresh_all, "#2ecc71"),
            ("⚙️", self.open_settings, "#3498db"),
            ("📊", self.open_analytics, "#f39c12")
        ]
        
        for icon, cmd, color in quick_actions:
            btn = ctk.CTkButton(
                actions_frame,
                text=icon,
                width=50,
                height=50,
                corner_radius=25,
                fg_color=color,
                hover_color=self.brighten_color(color),
                font=ctk.CTkFont(size=20),
                command=cmd
            )
            btn.pack(pady=5)
    
    def build_notifications(self):
        """Build notification system"""
        self.notification_frame = ctk.CTkFrame(self.content_frame,
                                              fg_color="transparent")
        self.notification_frame.place(relx=1, rely=0.15, anchor="ne")
    
    def show_notification(self, message, type="info"):
        """Show animated notification"""
        colors = {
            "info": "#3498db",
            "success": "#2ecc71",
            "warning": "#f39c12",
            "error": "#e74c3c"
        }
        
        notif = ctk.CTkFrame(
            self.notification_frame,
            fg_color=("gray10", "gray10"),
            corner_radius=12,
            border_width=2,
            border_color=colors.get(type, "#3498db")
        )
        notif.pack(pady=5, padx=10, anchor="e")
        
        label = ctk.CTkLabel(
            notif,
            text=message,
            font=ctk.CTkFont(size=11),
            text_color="white"
        )
        label.pack(padx=15, pady=10)
        
        # Auto-dismiss
        self.root.after(3000, notif.destroy)
    
    # Utility methods
    def brighten_color(self, hex_color):
        """Brighten a hex color"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r, g, b = min(255, int(r * 1.3)), min(255, int(g * 1.3)), min(255, int(b * 1.3))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    # Update methods
    def update_clock(self):
        """Update clock display"""
        now = datetime.now().strftime("%I:%M:%S %p • %d %B %Y")
        try:
            self.clock_label.configure(text=now)
        except:
            pass
        if self.running:
            self.root.after(1000, self.update_clock)
    
    def update_ticker(self):
        """Update live stats ticker"""
        if self.stats_module:
            stats = self.stats_module.get_all_statistics()
            ticker_text = f"📊 {stats['total_students']} Students | ✅ {stats['present_today']} Present | 📸 {stats['photos_collected']} Samples | 🧠 AI: {'Trained' if stats['models_trained'] > 0 else 'Not Trained'}"
        else:
            ticker_text = "📊 Real-Time Statistics Loading..."
        
        try:
            self.ticker_label.configure(text=ticker_text)
        except:
            pass
        
        if self.running:
            self.root.after(5000, self.update_ticker)
    
    def update_activity_feed(self):
        """Update live activity feed"""
        # Clear old activities
        for widget in self.activity_scroll.winfo_children():
            widget.destroy()
        
        if self.stats_module:
            activities = self.stats_module.get_recent_activity(10)
            
            for activity in reversed(activities):
                activity_card = ctk.CTkFrame(
                    self.activity_scroll,
                    fg_color=("gray14", "gray14"),
                    corner_radius=8,
                    height=50
                )
                activity_card.pack(fill="x", pady=3)
                activity_card.pack_propagate(False)
                
                icon = ctk.CTkLabel(activity_card, text="✅",
                                   font=ctk.CTkFont(size=18))
                icon.pack(side="left", padx=10)
                
                info_frame = ctk.CTkFrame(activity_card, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True, padx=5)
                
                name_label = ctk.CTkLabel(
                    info_frame,
                    text=activity['name'],
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color="white",
                    anchor="w"
                )
                name_label.pack(fill="x")
                
                time_label = ctk.CTkLabel(
                    info_frame,
                    text=f"🕐 {activity['time']}",
                    font=ctk.CTkFont(size=9),
                    text_color="gray60",
                    anchor="w"
                )
                time_label.pack(fill="x")
        
        if self.running:
            self.root.after(5000, self.update_activity_feed)
    
    def update_video(self):
        """Update video background"""
        if not self.running or not self.cap:
            return
        
        ret, frame = self.cap.read()
        if not ret:
            try:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
            except:
                return
        
        if ret:
            try:
                w = self.root.winfo_width() or 1920
                h = self.root.winfo_height() or 1080
                frame = cv2.resize(frame, (w, h))
                frame = cv2.GaussianBlur(frame, (25, 25), 0)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                img = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(img)
                
                self.video_canvas.delete("video")
                self.video_canvas.create_image(0, 0, anchor="nw",
                                              image=photo, tags="video")
                self.video_canvas.image = photo
            except:
                pass
        
        if self.running:
            self.root.after(33, self.update_video)
    
    def _start_all_updates(self):
        """Start all update processes"""
        self.update_clock()
        self.update_ticker()
        if self.video_enabled:
            self.update_video()
        self.update_charts()
        
        # Periodic updates
        def periodic_updates():
            while self.running:
                time.sleep(10)
                if self.running:
                    self.root.after(0, self.update_activity_feed)
        
        threading.Thread(target=periodic_updates, daemon=True).start()
    
    
    def update_charts(self):
        """Redraw charts every 10 seconds"""
        try:
        # Rebuild only chart area without rebuilding full UI
            left_panel = self.content_frame.winfo_children()[1].winfo_children()[0]
            self.build_charts_grid(left_panel)
        except:
            pass

        if self.running:
            self.root.after(10000, self.update_charts)

    # DISHA Integration
    def toggle_disha(self):
        """Toggle DISHA Ultra"""
        if not DISHA_AVAILABLE:
            messagebox.showinfo("DISHA Ultra",
                "DISHA Ultra with Internet will be created.\n\n"
                "Required:\n"
                "pip install pyttsx3 SpeechRecognition pyaudio requests beautifulsoup4")
            return
        
        if not self.disha_active:
            try:
                self.disha = UltraDISHAWithInternet(self.root)
                self.disha.start()
                self.disha_active = True
                
                self.disha_btn.configure(fg_color="#27ae60")
                self.disha_status.configure(text_color="#00ff00")
                
                self.show_notification("🎤 DISHA Ultra Activated!", "success")
                
                info = ("✨ DISHA ULTRA WITH INTERNET ACTIVATED!\n\n"
                       "🌐 Full Internet Access Enabled\n"
                       "🎯 Complete Project Control\n\n"
                       "Try:\n"
                       "• 'Hey DISHA, search for AI news'\n"
                       "• 'DISHA, what's the weather today?'\n"
                       "• 'Hey DISHA, open student management'\n"
                       "• 'DISHA, how many students are present?'")
                
                messagebox.showinfo("DISHA Ultra Active", info)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start: {str(e)}")
                self.disha_active = False
        else:
            try:
                if self.disha:
                    self.disha.stop()
                    self.disha = None
                self.disha_active = False
                
                self.disha_btn.configure(fg_color="#9b59b6")
                self.disha_status.configure(text_color="#ff4444")
                
                self.show_notification("DISHA Ultra Deactivated", "info")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to stop: {str(e)}")
    
    # Module launchers
    def open_students(self):
        try:
            from student_management import UpdatedStudentManagement
            UpdatedStudentManagement(self.root)
            self.show_notification("Student Management Opened", "success")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def open_recognition(self):
        try:
            from face_recognition_module import FaceRecognitionModule
            FaceRecognitionModule(self.root)
            self.show_notification("Face Recognition Started", "success")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def open_attendance(self):
        try:
            from attendance_viewer import AttendanceViewer
            AttendanceViewer(self.root)
            self.show_notification("Attendance Viewer Opened", "success")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def open_training(self):
        try:
            from train_data_module import TrainDataModule
            TrainDataModule(self.root)
            self.show_notification("Training Module Opened", "success")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def open_photos(self):
        try:
            from photo_capture_module import PhotoCaptureModule
            PhotoCaptureModule(self.root, student_id=999, student_name="Test")
            self.show_notification("Photo Capture Opened", "success")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def open_help(self):
        help_text = """
🚀 ULTRA-ADVANCED FACE RECOGNITION SYSTEM

🌟 FEATURES:
✅ Real-time charts and graphs
✅ Live activity monitoring
✅ AI-powered analytics
✅ Internet-enabled DISHA assistant
✅ Complete project control

📊 DASHBOARD:
• Live statistics cards
• Attendance trends chart
• Department distribution
• Weekly performance bars
• Real-time activity graph

🎤 DISHA ULTRA:
• Natural language understanding
• Internet search capabilities
• Full system control
• Context-aware responses

💡 USAGE:
1. Monitor real-time stats on dashboard
2. Use DISHA for voice commands
3. Access all modules from control panel
4. View live charts for insights

🔗 QUICK ACTIONS:
• 🔄 Refresh: Update all data
• ⚙️ Settings: Configure system
• 📊 Analytics: View detailed reports

📚 SUPPORT:
Developed by SMIT Students
Version: Ultra Advanced 5.0
        """
        
        win = ctk.CTkToplevel(self.root)
        win.title("Help & Information")
        win.geometry("800x700")
        
        text = ctk.CTkTextbox(win, font=ctk.CTkFont(size=12))
        text.pack(fill="both", expand=True, padx=20, pady=20)
        text.insert("1.0", help_text)
        text.configure(state="disabled")
        
        ctk.CTkButton(win, text="Close", command=win.destroy,
                     height=45).pack(pady=(0, 20))
    
    def open_developer(self):
        dev_text = """
🎓 SMIT ULTRA-ADVANCED FACE RECOGNITION SYSTEM

👨‍💻 Developed By: SMIT Students

📚 PROJECT: Advanced Biometric AI System
⚡ VERSION: 5.0 - Ultra Advanced Edition

🛠️ TECHNOLOGIES:
  • Python 3.8+
  • CustomTkinter (Ultra UI)
  • Matplotlib (Live Charts)
  • OpenCV (Face Recognition)
  • LBPH Algorithm
  • Real-time Processing
  • Voice Assistant Integration
  • Internet-Enabled AI

🌟 ULTRA FEATURES:
  ✅ Real-time animated dashboards
  ✅ Live charts and graphs
  ✅ Internet-enabled DISHA Ultra
  ✅ 3D card effects
  ✅ Glassmorphic design
  ✅ Live activity feeds
  ✅ Comprehensive analytics
  ✅ Voice-controlled operations
  ✅ Web search integration
  ✅ Natural language processing

📊 CAPABILITIES:
  • Real-time statistics monitoring
  • Animated trend visualization
  • Department distribution analysis
  • Weekly performance tracking
  • Live activity streaming
  • Voice-activated controls
  • Internet-powered responses
  • Complete system automation

🎯 Innovation Level: ULTRA ADVANCED
📅 Year: 2024-2025

© SMIT - All Rights Reserved
Ultra-Advanced AI System
        """
        
        win = ctk.CTkToplevel(self.root)
        win.title("Developer Information")
        win.geometry("800<br/>700")
        
        text = ctk.CTkTextbox(win, font=ctk.CTkFont(size=12))
        text.pack(fill="both", expand=True, padx=20, pady=20)
        text.insert("1.0", dev_text)
        text.configure(state="disabled")
        
        ctk.CTkButton(win, text="Close", command=win.destroy,
                     height=45).pack(pady=(0, 20))
    
    def refresh_all(self):
        """Refresh all data"""
        self.update_ticker()
        self.update_activity_feed()
        self.show_notification("🔄 All Data Refreshed", "success")
    
    def open_settings(self):
        from settings_window import SettingsWindow
        SettingsWindow(self.root)
        self.show_notification("⚙️ Settings Opened", "info")

    
    def open_analytics(self):
        from advanced_analytics import AdvancedAnalytics
        AdvancedAnalytics(self.root, self.stats_module)
        self.show_notification("📊 Advanced Analytics Opened", "success")

    
    def exit_app(self):
        """Exit application"""
        if messagebox.askyesno("Exit", "Exit Ultra System?"):
            self.running = False
            if self.disha:
                try:
                    self.disha.stop()
                except:
                    pass
            if self.cap:
                try:
                    self.cap.release()
                except:
                    pass
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
        

if __name__ == "__main__":
    app = UltraAdvancedDashboard()
    app.run()
