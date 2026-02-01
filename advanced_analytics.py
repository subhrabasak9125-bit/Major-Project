import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class AdvancedAnalytics:
    def __init__(self, root, stats):
        self.root = root
        self.stats = stats

        self.win = ctk.CTkToplevel(root)
        self.win.title("📊 Advanced Analytics")
        self.win.geometry("1050x700")
        self.win.grab_set()

        self.build_ui()

    def build_ui(self):
        title = ctk.CTkLabel(self.win, text="📊 ADVANCED ANALYTICS",
                             font=ctk.CTkFont(size=22, weight="bold"),
                             text_color="#00d9ff")
        title.pack(pady=15)

        # Main container
        frame = ctk.CTkFrame(self.win, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=10)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # Chart 1 — Heatmap (Weekly × Hour)
        self.create_heatmap(frame, 0, 0)

        # Chart 2 — Department Strength Bar Chart
        self.create_department_chart(frame, 0, 1)

        # Chart 3 — Monthly Attendance Trend
        self.create_monthly_trend(frame, 1, 0)

        # Chart 4 — Peak Hour Activity
        self.create_peak_hour(frame, 1, 1)

    # ---------------- CHART 1 ----------------
    def create_heatmap(self, parent, row, col):
        card = ctk.CTkFrame(parent, fg_color=("gray12", "gray12"), corner_radius=12)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(card, text="🔥 Weekly Attendance Heatmap",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#00d9ff").pack(pady=10)

        fig = Figure(figsize=(5,3), facecolor="#1a1a1a")
        ax = fig.add_subplot(111)

        import numpy as np
        heat = np.random.randint(20, 100, size=(7, 8))  # Fake heatmap (can be replaced with real)

        ax.imshow(heat, cmap="plasma")
        ax.set_xticks([])
        ax.set_yticks([])
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    # ---------------- CHART 2 ----------------
    def create_department_chart(self, parent, row, col):
        card = ctk.CTkFrame(parent, fg_color=("gray12", "gray12"), corner_radius=12)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(card, text="🏫 Department Strength",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#00d9ff").pack(pady=10)

        fig = Figure(figsize=(5,3), facecolor="#1a1a1a")
        ax = fig.add_subplot(111)

        dept_data = self.stats.get_department_distribution()
        x = list(dept_data.keys())
        y = list(dept_data.values())

        ax.bar(x, y, color="#3498db")
        ax.set_facecolor("#1a1a1a")
        ax.tick_params(colors="white")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------------- CHART 3 ----------------
    def create_monthly_trend(self, parent, row, col):
        card = ctk.CTkFrame(parent, fg_color=("gray12", "gray12"), corner_radius=12)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(card, text="📅 Monthly Attendance Trend",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#00d9ff").pack(pady=10)

        fig = Figure(figsize=(5,3), facecolor="#1a1a1a")
        ax = fig.add_subplot(111)

        import numpy as np
        days = list(range(1, 31))
        trend = np.random.randint(50, 120, size=30)

        ax.plot(days, trend, color="#2ecc71")
        ax.set_facecolor("#1a1a1a")
        ax.tick_params(colors="white")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------------- CHART 4 ----------------
    def create_peak_hour(self, parent, row, col):
        card = ctk.CTkFrame(parent, fg_color=("gray12", "gray12"), corner_radius=12)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(card, text="⏳ Peak Hour Activity",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#e67e22").pack(pady=10)

        fig = Figure(figsize=(5,3), facecolor="#1a1a1a")
        ax = fig.add_subplot(111)

        hours = ["8AM","9AM","10AM","11AM","12PM","1PM","2PM"]
        counts = [12, 33, 55, 78, 99, 54, 20]

        ax.plot(hours, counts, color="#f39c12", marker="o")
        ax.set_facecolor("#1a1a1a")
        ax.tick_params(colors="white")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
