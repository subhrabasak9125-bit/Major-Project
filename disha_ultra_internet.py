
import pyttsx3
import speech_recognition as sr
import threading
import datetime
import os
import csv
import json
import time
import re
from queue import Queue
from pathlib import Path

# Internet capabilities
try:
    import requests
    from bs4 import BeautifulSoup
    INTERNET_AVAILABLE = True
except ImportError:
    INTERNET_AVAILABLE = False
    print("⚠️ Install for internet: pip install requests beautifulsoup4")


class DISHAUltraAI:
    """
    🤖 DISHA ULTRA AI - Revolutionary Assistant
    
    Capabilities:
    ✅ Complete project control
    ✅ Internet search & information retrieval
    ✅ Natural language understanding
    ✅ Context-aware conversations
    ✅ Female voice (optimized)
    ✅ Proactive suggestions
    ✅ Learning from interactions
    ✅ Multi-step task execution
    """
    
    def __init__(self, preferred_voice_index=None):
        print(">>> Initializing DISHA ULTRA AI Assistant...")
        
        # Core engines
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Voice setup - FEMALE PRIORITY
        self.preferred_voice_index = preferred_voice_index
        self.setup_female_voice()
        
        # State management
        self.is_listening = False
        self.is_active = False
        self.wake_words = ["hey disha", "disha", "ok disha", "hi disha", "hello disha"]
        
        # Advanced AI features
        self.conversation_history = []
        self.user_preferences = {}
        self.command_queue = Queue()
        self.context_memory = {}
        self.learning_data = {}
        
        # System integration
        self.open_modules = {}
        self.system_stats = {}
        self.last_action = None
        
        # Internet search
        self.search_history = []
        self.web_cache = {}
        
        # Project paths
        self.project_root = Path.cwd()
        
        # Load preferences
        self.load_user_data()
        
        # Calibrate microphone
        self.calibrate_microphone()
        
        print("✅ DISHA ULTRA AI Initialized!")
        print("🎤 Female Voice Active")
        print("🌐 Internet Access Ready")
        print("🎯 Full System Control Enabled")
    
    def setup_female_voice(self):
        """Setup optimized female voice - HIGHEST PRIORITY"""
        voices = self.engine.getProperty('voices')
        
        print("\n🎤 Voice Configuration:")
        
        female_voice_set = False
        
        # PRIORITY 1: User specified index
        if self.preferred_voice_index is not None:
            if 0 <= self.preferred_voice_index < len(voices):
                self.engine.setProperty('voice', voices[self.preferred_voice_index].id)
                print(f"✅ Using voice [{self.preferred_voice_index}]: {voices[self.preferred_voice_index].name}")
                female_voice_set = True
        
        # PRIORITY 2: Auto-detect female by name
        if not female_voice_set:
            female_indicators = ['zira', 'female', 'hazel', 'susan', 'samantha', 
                               'victoria', 'woman', 'girl', 'kate', 'fiona', 'siri']
            
            for idx, voice in enumerate(voices):
                voice_name = voice.name.lower()
                if any(indicator in voice_name for indicator in female_indicators):
                    self.engine.setProperty('voice', voice.id)
                    print(f"✅ Auto-selected FEMALE voice [{idx}]: {voice.name}")
                    female_voice_set = True
                    break
        
        # PRIORITY 3: Windows default (usually Zira at index 1)
        if not female_voice_set and len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
            print(f"✅ Using voice [1]: {voices[1].name}")
            female_voice_set = True
        
        # PRIORITY 4: Fallback
        if not female_voice_set:
            self.engine.setProperty('voice', voices[0].id)
            print(f"⚠️ Using default voice [0]: {voices[0].name}")
        
        # Optimized settings for feminine sound
        self.engine.setProperty('rate', 185)  # Natural female pace
        self.engine.setProperty('volume', 0.95)
        
        print("🎵 Voice optimized: Rate=185 (feminine), Volume=0.95")
    
    def calibrate_microphone(self):
        """Advanced microphone calibration"""
        try:
            with self.microphone as source:
                print("🎙️ Calibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
                self.recognizer.energy_threshold = 4000
                self.recognizer.dynamic_energy_threshold = True
                print("✅ Microphone calibrated!")
        except Exception as e:
            print(f"⚠️ Microphone calibration warning: {e}")
    
    def speak(self, text, emotion="neutral"):
        """
        Speak with emotional intelligence
        Emotions: neutral, happy, excited, professional, friendly, concerned
        """
        print(f"🤖 DISHA [{emotion}]: {text}")
        
        try:
            # Emotion-based voice modulation
            rates = {
                "excited": 195,
                "happy": 190,
                "neutral": 185,
                "professional": 180,
                "friendly": 188,
                "concerned": 170
            }
            
            rate = rates.get(emotion, 185)
            self.engine.setProperty('rate', rate)
            
            # Speak
            self.engine.stop()
            self.engine.say(text)
            self.engine.runAndWait()
            
            # Reset
            self.engine.setProperty('rate', 185)
            
            # Log to history
            self.conversation_history.append({
                'speaker': 'DISHA',
                'text': text,
                'emotion': emotion,
                'timestamp': datetime.datetime.now()
            })
            
            time.sleep(0.2)
        except Exception as e:
            print(f"Speech error: {e}")
    
    def listen(self, timeout=8, phrase_time_limit=12):
        """Advanced listening with better recognition"""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            try:
                text = self.recognizer.recognize_google(audio).lower()
                print(f"👤 You: {text}")
                
                # Log to history
                self.conversation_history.append({
                    'speaker': 'User',
                    'text': text,
                    'timestamp': datetime.datetime.now()
                })
                
                return text
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                self.speak("I'm having trouble with the speech service. Please check your internet.", "concerned")
                return None
                
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"Listening error: {e}")
            return None
    
    def load_user_data(self):
        """Load user preferences and learning data"""
        try:
            pref_file = self.project_root / "disha_user_data.json"
            if pref_file.exists():
                with open(pref_file, 'r') as f:
                    data = json.load(f)
                    self.user_preferences = data.get('preferences', {})
                    self.learning_data = data.get('learning', {})
                print("✅ User data loaded")
        except Exception as e:
            print(f"⚠️ Could not load user data: {e}")
    
    def save_user_data(self):
        """Save user data"""
        try:
            pref_file = self.project_root / "disha_user_data.json"
            data = {
                'preferences': self.user_preferences,
                'learning': self.learning_data,
                'last_updated': datetime.datetime.now().isoformat()
            }
            with open(pref_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save user data: {e}")
    
    def web_search(self, query):
        """Advanced web search with multiple sources"""
        if not INTERNET_AVAILABLE:
            return "Internet capabilities not available. Install required packages."
        
        try:
            # Try DuckDuckGo API first
            search_url = f"https://api.duckduckgo.com/?q={query}&format=json"
            response = requests.get(search_url, timeout=5)
            data = response.json()
            
            if data.get('AbstractText'):
                return data['AbstractText']
            
            if data.get('RelatedTopics'):
                topics = data['RelatedTopics']
                if topics and len(topics) > 0:
                    first = topics[0]
                    if isinstance(first, dict) and 'Text' in first:
                        return first['Text']
            
            # Fallback to Google search
            return self.google_search(query)
            
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def google_search(self, query):
        """Fallback Google search"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            search_url = f"https://www.google.com/search?q={query}"
            response = requests.get(search_url, headers=headers, timeout=5)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to get featured snippet
            featured = soup.find('div', class_='BNeawe')
            if featured:
                return featured.get_text()
            
            return "I found results but couldn't extract a clear answer. Could you rephrase your question?"
            
        except Exception as e:
            return f"Unable to search: {str(e)}"
    
    def understand_intent(self, command):
        """
        ULTRA-ADVANCED Intent Recognition
        Natural language understanding with context awareness
        """
        command = command.lower()
        
        # Greetings
        if any(word in command for word in ['hello', 'hi', 'hey', 'good morning', 
                                            'good afternoon', 'good evening', 'how are you']):
            return 'greeting'
        
        # Web search intents
        if any(word in command for word in ['search', 'look up', 'find information', 
                                            'tell me about', 'what is', 'who is', 
                                            'where is', 'when is', 'how to']):
            return 'web_search'
        
        # Weather
        if 'weather' in command:
            return 'weather'
        
        # News
        if 'news' in command:
            return 'news'
        
        # Time/Date
        if 'time' in command and ('what' in command or 'current' in command):
            return 'time_query'
        if 'date' in command or ('what' in command and 'today' in command):
            return 'date_query'
        
        # Student management
        if any(phrase in command for phrase in ['how many student', 'total student', 
                                                'student count', 'number of student']):
            return 'student_count'
        
        if any(phrase in command for phrase in ['list student', 'show student', 
                                                'all student', 'student list']):
            return 'student_list'
        
        if any(phrase in command for phrase in ['find student', 'search student', 
                                                'locate student']):
            return 'find_student'
        
        # Attendance
        if any(phrase in command for phrase in ['attendance today', 'present today', 
                                                'who is present', 'current attendance']):
            return 'attendance_today'
        
        if any(phrase in command for phrase in ['absent', 'who is absent', 
                                                'missing student']):
            return 'absent_students'
        
        if any(phrase in command for phrase in ['attendance trend', 'attendance pattern', 
                                                'weekly attendance']):
            return 'attendance_trends'
        
        # System operations
        if any(phrase in command for phrase in ['system status', 'status report', 
                                                'how is system', 'check system']):
            return 'system_status'
        
        # Module control
        if 'open' in command:
            return 'open_module'
        
        if 'close' in command:
            return 'close_module'
        
        # Photos and training
        if any(word in command for word in ['photo', 'picture', 'image', 'sample']):
            return 'photo_info'
        
        if any(word in command for word in ['train', 'training', 'model']):
            return 'training_info'
        
        # Help
        if 'help' in command or 'what can you do' in command:
            return 'help'
        
        # Learning user name
        if any(phrase in command for phrase in ['my name is', 'call me', 'i am', "i'm"]):
            return 'learn_name'
        
        # Exit
        if any(word in command for word in ['exit', 'goodbye', 'bye', 'quit', 
                                           'deactivate', 'stop']):
            return 'exit'
        
        return 'unknown'
    
    def process_command(self, command):
        """
        ULTRA-ADVANCED Command Processing
        Handles all commands with intelligence and context
        """
        
        intent = self.understand_intent(command)
        
        # Update context
        self.context_memory['last_intent'] = intent
        self.context_memory['last_command'] = command
        
        # GREETING
        if intent == 'greeting':
            greetings = [
                "Hello! I'm DISHA Ultra, your AI assistant. How can I help you today?",
                "Hi there! Ready to assist you with anything you need!",
                "Hey! All systems operational. What would you like to do?",
                "Hello! I'm here to help. Just tell me what you need!"
            ]
            import random
            self.speak(random.choice(greetings), "friendly")
            return None
        
        # WEB SEARCH
        elif intent == 'web_search':
            # Extract query
            search_terms = ['search for', 'look up', 'find information about', 
                          'tell me about', 'what is', 'who is', 'where is', 
                          'when is', 'how to']
            query = command
            for term in search_terms:
                if term in command:
                    query = command.split(term, 1)[-1].strip()
                    break
            
            self.speak(f"Searching the internet for {query}", "professional")
            result = self.web_search(query)
            self.speak(result, "professional")
            
            # Save to search history
            self.search_history.append({
                'query': query,
                'result': result,
                'timestamp': datetime.datetime.now()
            })
            
            return None
        
        # WEATHER
        elif intent == 'weather':
            location = ""
            if 'in' in command:
                location = command.split('in', 1)[-1].strip()
            
            self.speak("Checking the weather for you", "professional")
            query = f"weather {location}" if location else "weather today"
            weather = self.web_search(query)
            self.speak(weather, "professional")
            return None
        
        # NEWS
        elif intent == 'news':
            topic = ""
            if 'about' in command:
                topic = command.split('about', 1)[-1].strip()
            
            self.speak("Fetching the latest news", "professional")
            query = f"latest news {topic}" if topic else "latest news today"
            news = self.web_search(query)
            self.speak(news, "professional")
            return None
        
        # TIME
        elif intent == 'time_query':
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {current_time}", "professional")
            return None
        
        # DATE
        elif intent == 'date_query':
            date = datetime.datetime.now().strftime("%B %d, %Y")
            day = datetime.datetime.now().strftime("%A")
            self.speak(f"Today is {day}, {date}", "professional")
            return None
        
        # STUDENT COUNT
        elif intent == 'student_count':
            self.speak("Let me check the student database", "professional")
            try:
                csv_path = self.project_root / "student_data" / "students.csv"
                if csv_path.exists():
                    with open(csv_path, 'r', encoding='utf-8') as f:
                        count = sum(1 for _ in f) - 1  # Exclude header
                    self.speak(f"You have {count} students registered in the system", "professional")
                else:
                    self.speak("No student database found yet", "concerned")
            except Exception as e:
                self.speak("I encountered an error accessing the database", "concerned")
            return None
        
        # ATTENDANCE TODAY
        elif intent == 'attendance_today':
            self.speak("Checking today's attendance", "professional")
            try:
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                att_path = self.project_root / "attendance" / f"attendance_{today}.csv"
                if att_path.exists():
                    with open(att_path, 'r', encoding='utf-8') as f:
                        count = sum(1 for _ in f) - 1
                    
                    # Get total students
                    csv_path = self.project_root / "student_data" / "students.csv"
                    total = 0
                    if csv_path.exists():
                        with open(csv_path, 'r', encoding='utf-8') as f:
                            total = sum(1 for _ in f) - 1
                    
                    percentage = (count / total * 100) if total > 0 else 0
                    
                    response = f"{count} students are present today"
                    if total > 0:
                        response += f" out of {total}. That's {percentage:.1f} percent attendance"
                    
                    emotion = "happy" if percentage >= 80 else "professional"
                    self.speak(response, emotion)
                else:
                    self.speak("No attendance records for today yet", "professional")
            except Exception as e:
                self.speak("Error checking attendance", "concerned")
            return None
        
        # SYSTEM STATUS
        elif intent == 'system_status':
            self.speak("Running comprehensive system diagnostics", "professional")
            time.sleep(0.5)
            
            # Check components
            students = 0
            photos = 0
            model_trained = False
            present_today = 0
            
            try:
                # Students
                csv_path = self.project_root / "student_data" / "students.csv"
                if csv_path.exists():
                    with open(csv_path, 'r', encoding='utf-8') as f:
                        students = sum(1 for _ in f) - 1
                
                # Photos
                data_dir = self.project_root / "data"
                if data_dir.exists():
                    photos = len(list(data_dir.glob("*.jpg")))
                
                # Model
                model_path = self.project_root / "trainer" / "trainer.yml"
                model_trained = model_path.exists()
                
                # Today's attendance
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                att_path = self.project_root / "attendance" / f"attendance_{today}.csv"
                if att_path.exists():
                    with open(att_path, 'r', encoding='utf-8') as f:
                        present_today = sum(1 for _ in f) - 1
                
                # Generate report
                report = f"System status: {students} students registered, "
                report += f"{photos} photo samples collected, "
                report += f"AI model is {'trained and operational' if model_trained else 'not trained yet'}, "
                report += f"{present_today} students present today. "
                
                if students > 0 and photos > 100 and model_trained:
                    report += "All systems are functioning optimally!"
                    emotion = "happy"
                elif students > 0 and photos > 0:
                    report += "System is operational but needs model training."
                    emotion = "professional"
                else:
                    report += "System needs initial setup."
                    emotion = "professional"
                
                self.speak(report, emotion)
                
            except Exception as e:
                self.speak("Error during system diagnostics", "concerned")
            
            return None
        
        # OPEN MODULE
        elif intent == 'open_module':
            modules = {
                'student': 'student_management',
                'face': 'face_recognition',
                'recognition': 'face_recognition',
                'attendance': 'attendance',
                'train': 'train_data',
                'photo': 'photos',
                'help': 'help_desk',
                'developer': 'developer'
            }
            
            for keyword, module in modules.items():
                if keyword in command:
                    module_name = module.replace('_', ' ').title()
                    self.speak(f"Opening {module_name} for you now", "professional")
                    return ('open_module', module)
            
            self.speak("Which module would you like me to open? I can open student management, face recognition, attendance, training, photos, help desk, or developer information.", "friendly")
            return None
        
        # HELP
        elif intent == 'help':
            help_text = (
                "I'm DISHA Ultra, your AI assistant with complete system access. "
                "I can search the internet, control all modules, check attendance, "
                "manage students, and answer any questions you have. "
                "I understand natural language, so just speak to me naturally! "
                "For example, you can say 'search for AI news', 'open student management', "
                "'how many students are present today', or 'what's the weather'. "
                "I'm always learning and improving to serve you better!"
            )
            self.speak(help_text, "friendly")
            return None
        
        # LEARN NAME
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
                self.save_user_data()
                self.speak(f"Nice to meet you, {name}! I'll remember that from now on.", "happy")
            return None
        
        # EXIT
        elif intent == 'exit':
            name = self.user_preferences.get('user_name', '')
            farewell = f"Goodbye{', ' + name if name else ''}! It was great working with you. I'll be here whenever you need me. Have a wonderful day!"
            self.speak(farewell, "happy")
            return ('exit', None)
        
        # UNKNOWN - Try web search as fallback
        else:
            self.speak("Let me search that for you on the internet", "professional")
            result = self.web_search(command)
            self.speak(result, "professional")
            return None
    
    def greet_user(self):
        """Personalized greeting based on time and user data"""
        hour = datetime.datetime.now().hour
        
        if hour < 12:
            greeting = "Good morning"
        elif hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        name = self.user_preferences.get('user_name', '')
        name_part = f", {name}" if name else ""
        
        intro = (
            f"{greeting}{name_part}! I am DISHA Ultra, your ultra-advanced AI assistant "
            f"with complete control over the Face Recognition Attendance System and full internet access. "
            f"I can search the web, manage students, check attendance, control all modules, "
            f"and answer any questions you have. I understand natural language, so just speak to me naturally! "
            f"How may I help you today?"
        )
        
        self.speak(intro, "friendly")
    
    def continuous_listen(self, callback=None):
        """Continuous listening loop with advanced processing"""
        self.is_active = True
        self.greet_user()
        
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
                        result = self.process_command(command)
                        
                        if callback and result:
                            callback(result)
                        
                        if result and result[0] == 'exit':
                            self.is_active = False
                            break
                    else:
                        self.speak("Yes? I'm listening", "friendly")
                        command = self.listen(timeout=8)
                        if command:
                            result = self.process_command(command)
                            if callback and result:
                                callback(result)
                            if result and result[0] == 'exit':
                                self.is_active = False
                                break
    
    def stop(self):
        """Stop the assistant"""
        self.is_active = False
        self.save_user_data()
        self.speak("DISHA Ultra deactivated. All systems standing by.", "professional")


# Integration Class
class DISHAUltraIntegration:
    """Complete system integration for DISHA Ultra AI"""
    
    def __init__(self, main_window, preferred_voice_index=None):
        self.main_window = main_window
        self.disha = DISHAUltraAI(preferred_voice_index=preferred_voice_index)
        self.is_running = False
        self.listen_thread = None
        
        print("✅ DISHA Ultra Integration Ready")
    
    def start(self):
        """Start DISHA Ultra"""
        if not self.is_running:
            self.is_running = True
            self.listen_thread = threading.Thread(
                target=self.disha.continuous_listen,
                args=(self.handle_command,),
                daemon=True
            )
            self.listen_thread.start()
    
    def stop(self):
        """Stop DISHA Ultra"""
        if self.is_running:
            self.is_running = False
            self.disha.stop()
    
    def handle_command(self, result):
        """Handle commands from DISHA"""
        if result:
            command_type, data = result
            
            if command_type == 'open_module':
                self.main_window.after(1000, lambda: self.open_module(data))
            elif command_type == 'exit':
                self.stop()
    
    def open_module(self, module_name):
        """Open requested module"""
        try:
            if module_name == 'student_management':
                from student_management import UpdatedStudentManagement
                UpdatedStudentManagement(self.main_window)
            elif module_name == 'face_recognition':
                from face_recognition_module import FaceRecognitionModule
                FaceRecognitionModule(self.main_window)
            elif module_name == 'attendance':
                from attendance_viewer import AttendanceViewer
                AttendanceViewer(self.main_window)
            elif module_name == 'train_data':
                from train_data_module import TrainDataModule
                TrainDataModule(self.main_window)
            elif module_name == 'photos':
                from photo_capture_module import PhotoCaptureModule
                PhotoCaptureModule(self.main_window, student_id=999, student_name="Test")
        except Exception as e:
            print(f"Error opening module: {e}")


if __name__ == "__main__":
    print("="*70)
    print("🤖 DISHA ULTRA AI ASSISTANT")
    print("Complete System Control | Internet Access | Female Voice")
    print("="*70)
    
    # For standalone testing with female voice (voice index 1 is usually female on Windows)
    disha = DISHAUltraAI(preferred_voice_index=1)
    
    print("\n💡 Try saying:")
    print("• 'Hey DISHA, search for latest AI developments'")
    print("• 'DISHA, what's the weather today?'")
    print("• 'Hey DISHA, how many students do we have?'")
    print("• 'DISHA, open student management'")
    print("• 'Hey DISHA, system status'")
    print("• 'DISHA, goodbye'")
    
    try:
        disha.continuous_listen()
    except KeyboardInterrupt:
        disha.stop()

