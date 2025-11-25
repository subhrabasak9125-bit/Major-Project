
import pyttsx3
import speech_recognition as sr
import threading
import datetime
import os
import csv
import json
from queue import Queue
import time
import tkinter as tk
from pathlib import Path
import re

class UltraDISHA:
    """
    Ultra Advanced DISHA - Complete Project Control
    Features:
    - Natural conversation flow with context awareness
    - Intelligent query understanding (no exact keywords needed)
    - Multi-step operations with memory
    - Advanced data analytics and insights
    - Full system control and automation
    - Learning capabilities with user preferences
    - Proactive suggestions and recommendations
    """
    
    def __init__(self, preferred_voice_index=None):
        """Initialize Ultra DISHA"""
        print(">>> Initializing Ultra Advanced DISHA...")
        
        # Core engines
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Voice setup
        self.preferred_voice_index = preferred_voice_index
        self.setup_advanced_voice()
        
        # State management
        self.is_listening = False
        self.is_active = False
        self.wake_words = ["hey disha", "disha", "ok disha", "hi disha", "hello disha", "yo disha"]
        
        # Advanced features
        self.conversation_context = []
        self.last_command = None
        self.user_preferences = {}
        self.command_history = []
        self.stats_cache = {}
        self.last_stats_update = None
        self.current_task = None
        self.waiting_for_response = False
        
        # Multi-threading
        self.command_queue = Queue()
        self.processing_lock = threading.Lock()
        
        # Project paths
        self.project_root = Path.cwd()
        self.data_dir = self.project_root / "data"
        self.student_data_dir = self.project_root / "student_data"
        self.attendance_dir = self.project_root / "attendance"
        self.trainer_dir = self.project_root / "trainer"
        
        # Load user preferences
        self.load_preferences()
        
        # Calibrate microphone
        self.calibrate_microphone()
        
        print("[OK] Ultra DISHA initialized successfully!")
        print("[+] Advanced features: Context awareness, natural conversations, full system control")
        print("[i] Intelligence Level: ULTRA - Can understand complex queries and natural language")
    
    def setup_advanced_voice(self):
        """Setup advanced voice with emotional tones - FEMALE VOICE PRIORITY"""
        voices = self.engine.getProperty('voices')
        
        print("\n[*] Available voices:")
        for idx, voice in enumerate(voices):
            gender = "FEMALE" if any(indicator in voice.name.lower() for indicator in 
                     ['zira', 'female', 'hazel', 'susan', 'samantha', 'victoria', 'woman', 'girl']) else "MALE"
            print(f"  [{idx}] {voice.name} ({gender})")
        
        female_voice_set = False
        
        # Voice selection logic
        if self.preferred_voice_index is not None:
            if 0 <= self.preferred_voice_index < len(voices):
                self.engine.setProperty('voice', voices[self.preferred_voice_index].id)
                print(f"[OK] Using user-specified voice [{self.preferred_voice_index}]: {voices[self.preferred_voice_index].name}")
                female_voice_set = True
            else:
                self.preferred_voice_index = None
        
        # PRIORITY 1: Try to find female voice by name indicators
        if not female_voice_set:
            female_indicators = ['zira', 'female', 'hazel', 'susan', 'samantha', 'victoria', 'woman', 'girl', 'kate', 'fiona']
            
            for idx, voice in enumerate(voices):
                voice_name = voice.name.lower()
                if any(indicator in voice_name for indicator in female_indicators):
                    self.engine.setProperty('voice', voice.id)
                    print(f"[OK] Auto-selected FEMALE voice [{idx}]: {voice.name}")
                    female_voice_set = True
                    break
        
        # PRIORITY 2: On Windows, voice index 1 is usually female (Zira)
        if not female_voice_set and len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
            print(f"[OK] Selected voice [1] (usually female): {voices[1].name}")
            female_voice_set = True
        
        # PRIORITY 3: Fallback to first available voice
        if not female_voice_set:
            self.engine.setProperty('voice', voices[0].id)
            print(f"[!] Using default voice [0]: {voices[0].name}")
        
        # Advanced voice settings for more feminine/pleasant sound
        self.engine.setProperty('rate', 180)  # Slightly slower for clearer, more feminine sound
        self.engine.setProperty('volume', 0.95)
        
        print(f"[+] Voice configured: Rate=180 (feminine), Volume=0.95")
        print(f"[i] TIP: To manually select a voice, pass preferred_voice_index parameter\n")
        print(f"    Example: UltraDISHA(preferred_voice_index=1)  # Usually Zira on Windows\n")
    
    def calibrate_microphone(self):
        """Advanced microphone calibration"""
        print("[*] Calibrating microphone for optimal performance...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
                self.recognizer.energy_threshold = 4000
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = 0.8
            print("[OK] Microphone calibrated successfully!")
        except Exception as e:
            print(f"[!] Microphone calibration warning: {e}")
    
    def speak(self, text, emotion="neutral"):
        """
        Advanced speech with emotional tones
        Emotions: neutral, happy, excited, concerned, professional, friendly
        """
        print(f"DISHA [{emotion}]: {text}")
        
        try:
            # Adjust voice for emotion (optimized for female voice)
            rate = 180  # Base rate for feminine voice
            if emotion == "excited":
                rate = 195  # Slightly faster when excited
            elif emotion == "concerned":
                rate = 165  # Slower when concerned
            elif emotion == "professional":
                rate = 175  # Measured professional tone
            elif emotion == "friendly":
                rate = 185  # Warm friendly tone
            
            self.engine.setProperty('rate', rate)
            
            # Speak
            self.engine.stop()
            self.engine.say(text)
            self.engine.runAndWait()
            
            # Reset to base feminine rate
            self.engine.setProperty('rate', 180)
            
            time.sleep(0.2)
        except Exception as e:
            print(f"Speech error: {e}")
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """Advanced listening with better recognition"""
        try:
            with self.microphone as source:
                print("[*] Listening...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            try:
                text = self.recognizer.recognize_google(audio).lower()
                print(f"[>] You said: {text}")
                self.conversation_context.append({
                    'type': 'user',
                    'text': text,
                    'timestamp': datetime.datetime.now()
                })
                return text
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                self.speak("I'm having trouble connecting to the speech service. Please check your internet.", "concerned")
                return None
                
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"Listening error: {e}")
            return None
    
    def load_preferences(self):
        """Load user preferences"""
        pref_file = self.project_root / "disha_preferences.json"
        if pref_file.exists():
            try:
                with open(pref_file, 'r') as f:
                    self.user_preferences = json.load(f)
                print("[OK] User preferences loaded")
            except:
                pass
    
    def save_preferences(self):
        """Save user preferences"""
        pref_file = self.project_root / "disha_preferences.json"
        try:
            with open(pref_file, 'w') as f:
                json.dump(self.user_preferences, f, indent=2)
        except:
            pass
    
    def greet(self):
        """Personalized greeting"""
        hour = datetime.datetime.now().hour
        
        if hour < 12:
            greeting = "Good morning"
        elif hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        name = self.user_preferences.get('user_name', '')
        name_part = f", {name}" if name else ""
        
        # Check if first time user
        if not name:
            self.speak(
                f"{greeting}! I am DISHA Ultra, your ultra-advanced AI assistant with complete control over your Face Recognition Attendance System. "
                f"I understand natural language, remember context, and can perform complex operations. "
                f"By the way, what should I call you? You can tell me anytime by saying 'my name is' or 'call me' followed by your name.",
                "friendly"
            )
        else:
            self.speak(
                f"{greeting}{name_part}! Great to see you again! I'm DISHA Ultra, ready to assist. "
                f"I remember our previous conversations and your preferences. "
                f"Just tell me what you need - I can understand natural language, no exact commands required!",
                "happy"
            )
    
    def get_statistics(self):
        """Get comprehensive statistics with caching"""
        now = time.time()
        if (self.last_stats_update is None or 
            now - self.last_stats_update > 5):
            
            try:
                from statistics_module import RealTimeStatistics
                stats_module = RealTimeStatistics()
                self.stats_cache = stats_module.get_all_statistics()
                self.last_stats_update = now
            except:
                # Manual calculation fallback
                self.stats_cache = self.calculate_manual_statistics()
        
        return self.stats_cache
    
    def calculate_manual_statistics(self):
        """Calculate statistics manually from files"""
        stats = {
            'total_students': 0,
            'present_today': 0,
            'photos_collected': 0,
            'models_trained': 0,
            'total_records': 0
        }
        
        try:
            # Count students
            csv_path = self.student_data_dir / "students.csv"
            if csv_path.exists():
                with open(csv_path, 'r') as f:
                    reader = csv.DictReader(f)
                    stats['total_students'] = sum(1 for _ in reader)
            
            # Count photos
            if self.data_dir.exists():
                for student_dir in self.data_dir.iterdir():
                    if student_dir.is_dir():
                        stats['photos_collected'] += sum(1 for _ in student_dir.glob('*.jpg'))
            
            # Check model
            model_path = self.trainer_dir / "trainer.yml"
            if model_path.exists():
                stats['models_trained'] = 1
            
            # Count today's attendance
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            attendance_file = self.attendance_dir / f"attendance_{today}.csv"
            if attendance_file.exists():
                with open(attendance_file, 'r') as f:
                    reader = csv.DictReader(f)
                    stats['present_today'] = sum(1 for _ in reader)
        except Exception as e:
            print(f"Stats calculation error: {e}")
        
        return stats
    
    def get_student_list(self):
        """Get detailed student list"""
        try:
            csv_path = self.student_data_dir / "students.csv"
            if csv_path.exists():
                with open(csv_path, 'r') as f:
                    reader = csv.DictReader(f)
                    return list(reader)
            return []
        except:
            return []
    
    def get_attendance_data(self, date=None):
        """Get attendance for specific date"""
        try:
            if date is None:
                date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            attendance_file = self.attendance_dir / f"attendance_{date}.csv"
            if attendance_file.exists():
                with open(attendance_file, 'r') as f:
                    reader = csv.DictReader(f)
                    return list(reader)
            return []
        except:
            return []
    
    def analyze_attendance_trends(self):
        """Analyze attendance trends over past week"""
        try:
            if not self.attendance_dir.exists():
                return None
            
            files = sorted(self.attendance_dir.glob("attendance_*.csv"))
            if len(files) < 2:
                return None
            
            recent_files = files[-7:]  # Last 7 days
            daily_counts = []
            
            for file in recent_files:
                try:
                    with open(file, 'r') as f:
                        reader = csv.DictReader(f)
                        count = sum(1 for _ in reader)
                        daily_counts.append(count)
                except:
                    continue
            
            if not daily_counts:
                return None
            
            avg = sum(daily_counts) / len(daily_counts)
            latest = daily_counts[-1]
            trend = "increasing" if latest > avg * 1.1 else "decreasing" if latest < avg * 0.9 else "stable"
            
            return {
                'average': avg,
                'latest': latest,
                'trend': trend,
                'days_analyzed': len(daily_counts),
                'daily_counts': daily_counts
            }
        except:
            return None
    
    def get_student_by_name(self, name_query):
        """Find student by partial name match"""
        students = self.get_student_list()
        name_query = name_query.lower()
        
        # Exact match first
        for s in students:
            if s.get('Name', '').lower() == name_query:
                return s
        
        # Partial match
        matches = [s for s in students if name_query in s.get('Name', '').lower()]
        return matches[0] if matches else None
    
    def understand_intent(self, command):
        """
        Advanced intent recognition using pattern matching
        This allows natural language understanding without exact keywords
        """
        command = command.lower()
        
        # Greeting intents
        if any(word in command for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'how are you', "what's up", 'yo']):
            return 'greeting'
        
        # Student count intents
        if any(phrase in command for phrase in ['how many student', 'total student', 'number of student', 'count student', 'student count']):
            return 'student_count'
        
        # Student list intents
        if any(phrase in command for phrase in ['list student', 'show student', 'who are the student', 'tell me about student', 'student names']):
            return 'student_list'
        
        # Find specific student
        if any(phrase in command for phrase in ['find student', 'search student', 'look for student', 'locate student', 'who is']):
            return 'find_student'
        
        # Attendance today
        if any(phrase in command for phrase in ['attendance today', 'who is present', 'present today', 'attendance now', 'current attendance', "today's attendance"]):
            return 'attendance_today'
        
        # Absent students
        if any(phrase in command for phrase in ['who is absent', 'absent today', 'missing student', 'not present']):
            return 'absent_students'
        
        # Attendance trends
        if any(phrase in command for phrase in ['attendance trend', 'attendance pattern', 'attendance over time', 'past attendance', 'weekly attendance']):
            return 'attendance_trends'
        
        # System status
        if any(phrase in command for phrase in ['system status', 'status report', 'overall status', 'how is everything', 'system health', 'check system']):
            return 'system_status'
        
        # Photo/training status
        if any(phrase in command for phrase in ['photo', 'image', 'sample', 'picture']):
            return 'photo_info'
        
        # Model training status
        if any(phrase in command for phrase in ['model', 'training', 'trained', 'ready to recognize']):
            return 'model_info'
        
        # Open module
        if 'open' in command:
            return 'open_module'
        
        # Close module
        if 'close' in command:
            return 'close_module'
        
        # Time/Date
        if 'time' in command and ('what' in command or 'current' in command):
            return 'time_query'
        if 'date' in command or ('what' in command and 'today' in command):
            return 'date_query'
        
        # Help
        if any(word in command for word in ['help', 'what can you do', 'your capabilities', 'assist me', 'guide me']):
            return 'help'
        
        # Name learning
        if any(phrase in command for phrase in ['my name is', 'call me', 'i am', "i'm"]):
            return 'learn_name'
        
        # Exit
        if any(word in command for word in ['exit', 'goodbye', 'bye', 'quit', 'deactivate', 'stop', 'close disha']):
            return 'exit'
        
        # Refresh
        if any(word in command for word in ['refresh', 'update', 'reload']):
            return 'refresh'
        
        return 'unknown'
    
    def process_advanced_command(self, command):
        """
        Ultra-advanced command processing with natural language understanding
        No exact keywords needed - DISHA understands context and intent
        """
        
        # Store in history
        self.command_history.append({
            'command': command,
            'timestamp': datetime.datetime.now()
        })
        
        # Get conversation context
        context = self.get_conversation_context()
        
        # Understand intent
        intent = self.understand_intent(command)
        
        # Process based on intent
        if intent == 'greeting':
            responses = [
                "Hello! I'm functioning perfectly and ready to help you!",
                "Hi there! All systems are operational. What can I do for you?",
                "Hey! Great to hear from you. How can I assist?",
                "Hello! I'm here and ready to help with your attendance system!"
            ]
            import random
            self.speak(random.choice(responses), "friendly")
            return None
        
        elif intent == 'student_count':
            self.speak("Let me check the student database")
            stats = self.get_statistics()
            total = stats['total_students']
            
            if total > 0:
                self.speak(f"You have {total} students registered in the system", "professional")
                
                # Proactive suggestion
                if total < 5:
                    self.speak("That's a small class. Would you like me to help you add more students?", "friendly")
                elif total > 50:
                    self.speak("That's quite a large class! The face recognition system can handle it easily.", "happy")
            else:
                self.speak("The database is currently empty. Shall I guide you through adding students?", "friendly")
            return None
        
        elif intent == 'student_list':
            self.speak("Retrieving the complete student list")
            students = self.get_student_list()
            
            if students:
                if len(students) <= 10:
                    names = [s.get('Name', 'Unknown') for s in students]
                    self.speak(f"Here are all the registered students: {', '.join(names)}", "professional")
                else:
                    self.speak(f"You have {len(students)} students. Let me give you the first five: " + 
                             ', '.join([s.get('Name', 'Unknown') for s in students[:5]]) +
                             ". Would you like me to continue with more names?", "professional")
            else:
                self.speak("No students are currently registered. Shall I open the Student Management module for you?", "friendly")
            return None
        
        elif intent == 'find_student':
            # Extract name from command
            patterns = [r'find student (?:named |called )?(.+)', 
                       r'search (?:for )?student (?:named |called )?(.+)',
                       r'who is (.+)']
            
            name = None
            for pattern in patterns:
                match = re.search(pattern, command)
                if match:
                    name = match.group(1).strip()
                    break
            
            if name:
                self.speak(f"Searching for {name}")
                student = self.get_student_by_name(name)
                
                if student:
                    info = f"Found {student.get('Name')}! "
                    if student.get('ID'):
                        info += f"Student ID: {student.get('ID')}. "
                    if student.get('Major'):
                        info += f"Major: {student.get('Major')}. "
                    if student.get('Year'):
                        info += f"Year: {student.get('Year')}. "
                    
                    self.speak(info, "professional")
                    
                    # Check if they're present today
                    attendance = self.get_attendance_data()
                    is_present = any(a.get('ID') == student.get('ID') for a in attendance)
                    if is_present:
                        self.speak(f"{student.get('Name')} is present today!", "happy")
                    else:
                        self.speak(f"{student.get('Name')} is not marked present today", "neutral")
                else:
                    self.speak(f"I couldn't find any student matching '{name}'. Would you like me to show the complete student list?", "concerned")
            else:
                self.speak("Please tell me the student's name. Say 'find student' followed by the name", "professional")
            return None
        
        elif intent == 'attendance_today':
            self.speak("Checking today's attendance records")
            stats = self.get_statistics()
            present = stats['present_today']
            total = stats['total_students']
            
            if total > 0:
                percentage = (present / total) * 100
                
                # Emotional response based on attendance
                if percentage >= 90:
                    emotion = "excited"
                    comment = "Excellent attendance!"
                elif percentage >= 70:
                    emotion = "happy"
                    comment = "Good attendance."
                else:
                    emotion = "concerned"
                    comment = "Attendance is lower than usual."
                
                self.speak(f"{present} out of {total} students are present today. That's {percentage:.1f} percent. {comment}", emotion)
                
                # Provide trend analysis
                trends = self.analyze_attendance_trends()
                if trends:
                    trend_desc = f"The trend over the past week is {trends['trend']} with an average of {trends['average']:.0f} students per day."
                    self.speak(trend_desc, "professional")
            else:
                self.speak(f"{present} students are marked present today", "professional")
            return None
        
        elif intent == 'absent_students':
            self.speak("Calculating absent students")
            stats = self.get_statistics()
            present = stats['present_today']
            total = stats['total_students']
            absent = total - present
            
            if absent > 0:
                self.speak(f"{absent} students are absent today out of {total} total", "concerned")
                
                # List absent if small number
                if absent <= 10:
                    students = self.get_student_list()
                    attendance = self.get_attendance_data()
                    present_ids = [a.get('ID') for a in attendance]
                    
                    absent_students = [s for s in students if s.get('ID') not in present_ids]
                    
                    if absent_students:
                        names = [s.get('Name', 'Unknown') for s in absent_students]
                        self.speak(f"The absent students are: {', '.join(names)}", "professional")
            else:
                self.speak("Fantastic! Perfect attendance today - all students are present!", "excited")
            return None
        
        elif intent == 'attendance_trends':
            self.speak("Analyzing attendance trends")
            trends = self.analyze_attendance_trends()
            
            if trends:
                self.speak(
                    f"I analyzed the past {trends['days_analyzed']} days. "
                    f"The average attendance is {trends['average']:.1f} students. "
                    f"The trend is {trends['trend']}. "
                    f"Today we have {trends['latest']} students present.",
                    "professional"
                )
                
                # Provide recommendation
                if trends['trend'] == "decreasing":
                    self.speak("I notice attendance is declining. You might want to check if there are any issues.", "concerned")
                elif trends['trend'] == "increasing":
                    self.speak("Great news! Attendance is improving!", "happy")
            else:
                self.speak("I don't have enough historical data yet to analyze trends. Please use the system for a few more days.", "professional")
            return None
        
        elif intent == 'system_status':
            self.speak("Running comprehensive system diagnostics")
            time.sleep(0.3)
            
            stats = self.get_statistics()
            issues = []
            warnings = []
            
            # Check data
            if stats['total_students'] == 0:
                issues.append("No students registered")
            elif stats['total_students'] < 5:
                warnings.append("Very few students registered")
            
            if stats['photos_collected'] == 0:
                issues.append("No photo samples collected")
            elif stats['photos_collected'] < stats['total_students'] * 100:
                warnings.append("Insufficient photo samples for optimal recognition")
            
            if stats['models_trained'] == 0:
                issues.append("Face recognition model not trained")
            
            # Report
            report = f"System Status Report: {stats['total_students']} students, {stats['present_today']} present today, {stats['photos_collected']} photo samples. "
            
            if stats['models_trained'] > 0:
                report += "Face recognition model is trained and operational. "
            
            # Add trends
            trends = self.analyze_attendance_trends()
            if trends:
                report += f"Attendance trend is {trends['trend']}. "
            
            self.speak(report, "professional")
            
            if issues:
                self.speak(f"I found {len(issues)} critical issues: " + ", ".join(issues), "concerned")
            elif warnings:
                self.speak(f"I have {len(warnings)} recommendations: " + ", ".join(warnings), "professional")
            else:
                self.speak("All systems are functioning perfectly! No issues detected.", "happy")
            
            return None
        
        elif intent == 'photo_info':
            self.speak("Checking photo sample status")
            stats = self.get_statistics()
            photos = stats['photos_collected']
            students = stats['total_students']
            
            if photos > 0:
                avg_per_student = photos / students if students > 0 else 0
                self.speak(f"The system has {photos} photo samples collected, averaging {avg_per_student:.0f} per student. ", "professional")
                
                if avg_per_student < 100:
                    self.speak("I recommend capturing at least 100 samples per student for optimal accuracy.", "professional")
                else:
                    self.speak("Great! You have sufficient samples for excellent recognition accuracy.", "happy")
            else:
                self.speak("No photo samples have been collected yet. Would you like me to open the Photo Capture module?", "friendly")
            return None
        
        elif intent == 'model_info':
            self.speak("Checking face recognition model status")
            stats = self.get_statistics()
            
            if stats['models_trained'] > 0:
                self.speak("The face recognition model has been successfully trained and is ready for use. You can start marking attendance with face recognition!", "happy")
            else:
                self.speak("The model has not been trained yet. You need to capture photo samples first, then train the model before using face recognition. Shall I guide you through the process?", "professional")
            return None
        
        elif intent == 'open_module':
            module_map = {
                'student': 'student_management',
                'face': 'face_recognition',
                'recognition': 'face_recognition',
                'attendance': 'attendance',
                'train': 'train_data',
                'photo': 'photos',
                'help': 'help_desk',
                'developer': 'developer',
                'setting': 'settings'
            }
            
            for keyword, module in module_map.items():
                if keyword in command:
                    module_name = module.replace('_', ' ').title()
                    self.speak(f"Opening {module_name} for you now", "professional")
                    return ('open_module', module)
            
            self.speak("Which module would you like me to open? I can open student management, face recognition, attendance, training, photos, help desk, developer info, or settings.", "friendly")
            return None
        
        elif intent == 'close_module':
            if 'all' in command:
                self.speak("Closing all open modules for you", "professional")
                return ('close_all_modules', None)
            else:
                self.speak("Closing the module", "professional")
                return ('close_module', 'current')
        
        elif intent == 'time_query':
            self.speak("Let me check the time")
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            day = datetime.datetime.now().strftime("%A")
            self.speak(f"It's {current_time} on {day}", "professional")
            return None
        
        elif intent == 'date_query':
            self.speak("Let me check today's date")
            date = datetime.datetime.now().strftime("%B %d, %Y")
            day = datetime.datetime.now().strftime("%A")
            self.speak(f"Today is {day}, {date}", "professional")
            return None
        
        elif intent == 'help':
            self.speak(
                "I'm your ultra-advanced AI assistant with complete control over the attendance system. "
                "I understand natural language, so just talk to me naturally! "
                "I can manage students, check attendance, analyze trends, control all modules, "
                "answer questions, remember your preferences, and much more. "
                "I'm always learning and getting better at understanding you. "
                "Try asking me anything - no need for exact commands!",
                "friendly"
            )
            return None
        
        elif intent == 'learn_name':
            patterns = [r"my name is (.+)", r"call me (.+)", r"i am (.+)", r"i'm (.+)"]
            name = None
            
            for pattern in patterns:
                match = re.search(pattern, command)
                if match:
                    name = match.group(1).strip()
                    break
            
            if name:
                self.user_preferences['user_name'] = name
                self.save_preferences()
                self.speak(f"Nice to meet you, {name}! I'll remember that from now on. You can change it anytime.", "happy")
            return None
        
        elif intent == 'refresh':
            self.speak("Refreshing all system data")
            self.last_stats_update = None
            self.get_statistics()
            self.speak("All data has been refreshed successfully!", "professional")
            return ('refresh_stats', None)
        
        elif intent == 'exit':
            name = self.user_preferences.get('user_name', '')
            name_part = f", {name}" if name else ""
            self.speak(f"Goodbye{name_part}! It was great working with you. I'll be here whenever you need me. Have a wonderful day!", "happy")
            return ('exit', None)
        
        else:
            # Unknown intent - be helpful
            self.speak(
                "I'm not quite sure what you meant, but I'm here to help! "
                "Try asking me about students, attendance, system status, or tell me to open a specific module. "
                "I understand natural language, so just speak naturally.",
                "friendly"
            )
            return None
    
    def get_conversation_context(self):
        """Get recent conversation context"""
        recent = self.conversation_context[-5:] if len(self.conversation_context) >= 5 else self.conversation_context
        return recent
    
    def continuous_listen(self, callback=None):
        """Continuous listening with advanced processing"""
        self.is_active = True
        self.speak("DISHA Ultra is now active with full system access. I understand natural language - just talk to me!", "excited")
        
        while self.is_active:
            text = self.listen(timeout=10)
            
            if text:
                wake_detected = False
                command = text
                
                # Check for wake word
                for wake_word in self.wake_words:
                    if wake_word in text:
                        wake_detected = True
                        command = text.split(wake_word, 1)[-1].strip()
                        break
                
                if wake_detected:
                    if command:
                        result = self.process_advanced_command(command)
                        
                        if callback and result:
                            callback(result)
                        
                        if result and result[0] == 'exit':
                            self.is_active = False
                            break
                    else:
                        self.speak("Yes? I'm listening", "friendly")
                        
                        command = self.listen(timeout=7)
                        if command:
                            result = self.process_advanced_command(command)
                            
                            if callback and result:
                                callback(result)
                            
                            if result and result[0] == 'exit':
                                self.is_active = False
                                break
    
    def stop(self):
        """Stop DISHA"""
        self.is_active = False
        name = self.user_preferences.get('user_name', '')
        name_part = f", {name}" if name else ""
        self.speak(f"DISHA Ultra deactivated. See you soon{name_part}!", "professional")


# Enhanced Integration Class
class UltraDISHAIntegration:
    """
    Ultra DISHA Integration with complete project control
    Seamlessly integrates with the main UI
    """
    
    def __init__(self, main_window, preferred_voice_index=None):
        self.main_window = main_window
        self.disha = UltraDISHA(preferred_voice_index=preferred_voice_index)
        self.is_running = False
        self.listen_thread = None
        
        self.open_windows = {
            'student_management': None,
            'face_recognition': None,
            'attendance': None,
            'train_data': None,
            'photos': None
        }
        
        self.setup_status_display()
    
    def setup_status_display(self):
        """Setup status display"""
        self.status_label = None
        if hasattr(self.main_window, 'content_frame'):
            try:
                import customtkinter as ctk
                self.status_label = ctk.CTkLabel(
                    self.main_window.content_frame,
                    text="",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#00ff00",
                    fg_color=("gray20", "gray20"),
                    corner_radius=8
                )
                self.status_label.place(relx=0.5, rely=0.95, anchor="center")
                self.status_label.place_forget()
            except:
                pass
    
    def start(self):
        """Start Ultra DISHA"""
        if not self.is_running:
            self.is_running = True
            self.disha.greet()
            
            self.listen_thread = threading.Thread(
                target=self.disha.continuous_listen,
                args=(self.handle_command,),
                daemon=True
            )
            self.listen_thread.start()
    
    def stop(self):
        """Stop DISHA"""
        if self.is_running:
            self.is_running = False
            self.disha.stop()
    
    def handle_command(self, result):
        """Handle commands from DISHA with smooth execution"""
        command_type, data = result
        
        # Show processing indicator
        self.show_status("[*] DISHA is processing your request...")
        
        # 1 second delay for speech completion
        if command_type == 'open_module':
            self.main_window.after(1000, lambda: self._execute_open(data))
        
        elif command_type == 'close_module':
            self.main_window.after(1000, lambda: self._execute_close(data))
        
        elif command_type == 'close_all_modules':
            self.main_window.after(1000, self._execute_close_all)
        
        elif command_type == 'refresh_stats':
            self.main_window.after(1000, self._execute_refresh)
        
        elif command_type == 'exit':
            self.stop()
    
    def _execute_open(self, data):
        """Execute module opening"""
        self.open_module(data)
        self.hide_status()
    
    def _execute_close(self, data):
        """Execute module closing"""
        self.close_module(data)
        self.hide_status()
    
    def _execute_close_all(self):
        """Execute close all"""
        self.close_all_modules()
        self.hide_status()
    
    def _execute_refresh(self):
        """Execute refresh"""
        try:
            if hasattr(self.main_window, 'update_statistics'):
                self.main_window.update_statistics()
            elif hasattr(self.main_window, 'refresh_statistics_manual'):
                self.main_window.refresh_statistics_manual()
        except:
            pass
        self.hide_status()
    
    def show_status(self, text):
        """Show status message"""
        if self.status_label:
            try:
                self.status_label.configure(text=text)
                self.status_label.place(relx=0.5, rely=0.95, anchor="center")
            except:
                pass
    
    def hide_status(self):
        """Hide status message"""
        if self.status_label:
            try:
                self.main_window.after(1500, lambda: self.status_label.place_forget())
            except:
                pass
    
    def open_module(self, module_name):
        """Open the requested module"""
        try:
            if module_name == 'student_management':
                from student_management import UpdatedStudentManagement
                window = UpdatedStudentManagement(self.main_window)
                if hasattr(window, 'window'):
                    self.open_windows['student_management'] = window.window
            
            elif module_name == 'face_recognition':
                from face_recognition_module import FaceRecognitionModule
                window = FaceRecognitionModule(self.main_window)
                if hasattr(window, 'window'):
                    self.open_windows['face_recognition'] = window.window
            
            elif module_name == 'attendance':
                from attendance_viewer import AttendanceViewer
                window = AttendanceViewer(self.main_window)
                if hasattr(window, 'window'):
                    self.open_windows['attendance'] = window.window
            
            elif module_name == 'train_data':
                from train_data_module import TrainDataModule
                window = TrainDataModule(self.main_window)
                if hasattr(window, 'window'):
                    self.open_windows['train_data'] = window.window
            
            elif module_name == 'photos':
                from photo_capture_module import PhotoCaptureModule
                window = PhotoCaptureModule(self.main_window, student_id=999, student_name="Test Student")
                if hasattr(window, 'window'):
                    self.open_windows['photos'] = window.window
            
            elif module_name == 'help_desk':
                if hasattr(self.main_window, 'help_desk'):
                    self.main_window.help_desk()
            
            elif module_name == 'developer':
                if hasattr(self.main_window, 'developer'):
                    self.main_window.developer()
            
            elif module_name == 'settings':
                if hasattr(self.main_window, 'settings'):
                    self.main_window.settings()
                    
        except Exception as e:
            self.disha.speak(f"Error opening module: {str(e)}", "concerned")
    
    def close_module(self, module_name):
        """Close specific module"""
        try:
            if module_name in self.open_windows:
                window = self.open_windows[module_name]
                
                if window and self._is_window_open(window):
                    window.destroy()
                    self.open_windows[module_name] = None
                    
        except Exception as e:
            self.disha.speak(f"Error closing module: {str(e)}", "concerned")
    
    def close_all_modules(self):
        """Close all open module windows"""
        try:
            for module_name in self.open_windows:
                window = self.open_windows[module_name]
                if window and self._is_window_open(window):
                    try:
                        window.destroy()
                    except:
                        pass
                self.open_windows[module_name] = None
                
        except Exception as e:
            self.disha.speak(f"Error closing modules: {str(e)}", "concerned")
    
    def _is_window_open(self, window):
        """Check if window is still open"""
        try:
            return window.winfo_exists()
        except:
            return False
    
    def speak(self, text):
        """Make DISHA speak"""
        self.disha.speak(text)


# Standalone test
if __name__ == "__main__":
    print("="*70)
    print("DISHA ULTRA - Digital Intelligent System for Human Assistance")
    print("ULTRA HIGH LEVEL ADVANCED VERSION")
    print("="*70)
    print()
    
    disha = UltraDISHA()
    disha.greet()
    
    print("\n[i] Natural Language Examples:")
    print("- 'Hey DISHA, how many students do we have?'")
    print("- 'Yo DISHA, who's absent today?'")
    print("- 'Hey DISHA, what's the attendance trend?'")
    print("- 'Hi DISHA, find student John'")
    print("- 'Hey DISHA, open student management'")
    print("- 'DISHA, how's the system doing?'")
    print("- 'Hey DISHA, my name is Alex'")
    print("- 'OK DISHA, goodbye'")
    print()
    print("[+] Just speak naturally - DISHA understands context!")
    print()
    
    try:
        disha.continuous_listen()
    except KeyboardInterrupt:
        print("\n\nStopping DISHA Ultra...")
        disha.stop()
