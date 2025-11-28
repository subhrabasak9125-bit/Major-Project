import customtkinter as ctk
import json
import os

class SettingsWindow:
    def __init__(self, root):
        self.root = root
        self.config_path = "settings.json"

        self.win = ctk.CTkToplevel(root)
        self.win.title("⚙️ System Settings")
        self.win.geometry("650x550")
        self.win.grab_set()

        self.load_settings()
        self.build_ui()

    def load_settings(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                self.settings = json.load(f)
        else:
            self.settings = {
                "appearance": "dark",
                "auto_refresh": True,
                "refresh_interval": 10,
                "enable_voice": True
            }

    def save_settings(self):
        with open(self.config_path, "w") as f:
            json.dump(self.settings, f, indent=4)

    def build_ui(self):
        title = ctk.CTkLabel(self.win, text="⚙️ SYSTEM SETTINGS",
                             font=ctk.CTkFont(size=22, weight="bold"),
                             text_color="#00d9ff")
        title.pack(pady=15)

        container = ctk.CTkFrame(self.win)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Theme
        ctk.CTkLabel(container, text="Appearance Mode:",
                     font=ctk.CTkFont(size=14)).pack(anchor="w", pady=5)
        self.theme_box = ctk.CTkOptionMenu(
            container,
            values=["light", "dark"],
            command=self.update_theme
        )
        self.theme_box.set(self.settings["appearance"])
        self.theme_box.pack(fill="x", pady=5)

        # Auto refresh
        self.refresh_switch = ctk.CTkSwitch(
            container,
            text="Enable Auto Refresh",
            command=self.toggle_refresh
        )
        self.refresh_switch.select() if self.settings["auto_refresh"] else self.refresh_switch.deselect()
        self.refresh_switch.pack(pady=10)

        # Refresh interval
        ctk.CTkLabel(container, text="Refresh Interval (seconds):",
                     font=ctk.CTkFont(size=14)).pack(anchor="w")
        self.interval_entry = ctk.CTkEntry(container)
        self.interval_entry.insert(0, str(self.settings["refresh_interval"]))
        self.interval_entry.pack(fill="x", pady=5)

        # Save button
        ctk.CTkButton(container, text="Save Settings",
                      fg_color="#2ecc71",
                      command=self.save_settings).pack(pady=20)

    def update_theme(self, mode):
        self.settings["appearance"] = mode
        ctk.set_appearance_mode(mode)

    def toggle_refresh(self):
        self.settings["auto_refresh"] = self.refresh_switch.get() == 1
