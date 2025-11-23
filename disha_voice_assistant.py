

import pyttsx3
import speech_recognition as sr
import threading
import datetime
import os
import csv
from queue import Queue
import time
import tkinter as tk

class DISHA:
    """
    DISHA - Digital Intelligent System for Human Assistance
    Enhanced version with proper speech-first behavior
    """
    
    def __init__(self):
        # Initialize text-to-speech (OFFLINE - INSTANT)
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Assistant state
        self.is_listening = False
        self.is_active = False
        self.wake_words = ["hey disha", "disha", "ok disha", "hi disha"]
        
        # Command queue for threaded processing
        self.command_queue = Queue()
        
        # Statistics cache (for quick responses)
        self.stats_cache = {}
        self.last_stats_update = None
        
        # Adjust for ambient noise
        print("DISHA: Calibrating microphone...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.energy_threshold = 4000
                self.recognizer.dynamic_energy_threshold = True
            print("DISHA: Microphone calibrated successfully!")
        except Exception as e:
            print(f"DISHA: Microphone calibration warning: {e}")
        
        print("DISHA: Initialization complete!")
    
    def setup_voice(self):
        """Configure DISHA's voice"""
        voices = self.engine.getProperty('voices')
        
        # Try to set female voice (usually index 1)
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        else:
            self.engine.setProperty('voice', voices[0].id)
        
        # Set speech rate
        self.engine.setProperty('rate', 175)
        
        # Set volume
        self.engine.setProperty('volume', 0.9)
    
    def speak(self, text, wait=True):
        """Make DISHA speak - ALWAYS COMPLETES BEFORE CONTINUING"""
        print(f"DISHA: {text}")
        
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")
    
    def listen(self, timeout=5, phrase_time_limit=5):
        """Listen for voice command"""
        try:
            with self.microphone as source:
                print("DISHA: Listening...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            # Recognize speech
            try:
                text = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                self.speak("I couldn't connect to the speech service. Please check your internet.")
                return None
                
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"Error listening: {e}")
            return None
    
    def greet(self):
        """Greet the user based on time"""
        hour = datetime.datetime.now().hour
        
        if hour < 12:
            greeting = "Good morning"
        elif hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        self.speak(f"{greeting}! I am DISHA, your Digital Intelligent System for Human Assistance. "
                  f"I can open and close modules, answer questions, and help you manage the system. "
                  f"Say 'Hey DISHA' followed by your command. How may I help you?")
    
    def get_statistics(self):
        """Get system statistics (cached for speed)"""
        now = time.time()
        if (self.last_stats_update is None or 
            now - self.last_stats_update > 10):
            
            try:
                from statistics_module import RealTimeStatistics
                stats_module = RealTimeStatistics()
                self.stats_cache = stats_module.get_all_statistics()
                self.last_stats_update = now
            except:
                self.stats_cache = {
                    'total_students': 0,
                    'present_today': 0,
                    'photos_collected': 0,
                    'models_trained': 0
                }
        
        return self.stats_cache
    
    def get_student_list(self):
        """Get list of students from CSV"""
        try:
            csv_path = "student_data/students.csv"
            if os.path.exists(csv_path):
                with open(csv_path, 'r') as f:
                    reader = csv.DictReader(f)
                    students = list(reader)
                    return students
            return []
        except:
            return []
    
    def get_today_attendance(self):
        """Get today's attendance"""
        try:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            attendance_file = f"attendance/attendance_{today}.csv"
            
            if os.path.exists(attendance_file):
                with open(attendance_file, 'r') as f:
                    reader = csv.DictReader(f)
                    attendance = list(reader)
                    return attendance
            return []
        except:
            return []
    
    def process_command(self, command):
        """
        Process voice command
        CRITICAL: Speaks FIRST, then returns action to perform
        """
        
        # === GREETINGS ===
        if any(word in command for word in ['hello', 'hi', 'hey there']):
            self.speak("Hello! How can I assist you today?")
            return None
        
        # === TIME & DATE ===
        elif 'time' in command and 'what' in command:
            self.speak("Let me check the time for you")
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}")
            return None
        
        elif 'date' in command and ('what' in command or 'today' in command):
            self.speak("Let me check today's date")
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            day = datetime.datetime.now().strftime("%A")
            self.speak(f"Today is {day}, {current_date}")
            return None
        
        # === STUDENT STATISTICS ===
        elif 'how many students' in command or 'total students' in command or 'number of students' in command:
            self.speak("Let me check the student count for you")
            stats = self.get_statistics()
            total = stats['total_students']
            if total > 0:
                self.speak(f"There are {total} students registered in the system")
            else:
                self.speak("No students are currently registered. You can add students using the Student Management module")
            return None
        
        elif 'list students' in command or 'show students' in command or 'who are the students' in command:
            self.speak("Retrieving student list")
            students = self.get_student_list()
            if students:
                if len(students) <= 5:
                    names = [s.get('Name', 'Unknown') for s in students]
                    self.speak(f"The registered students are: {', '.join(names)}")
                else:
                    self.speak(f"There are {len(students)} students registered. The first few are: " + 
                             ', '.join([s.get('Name', 'Unknown') for s in students[:3]]))
            else:
                self.speak("No students are currently registered")
            return None
        
        # === ATTENDANCE ===
        elif 'present today' in command or 'attendance today' in command or 'who is present' in command:
            self.speak("Checking today's attendance")
            stats = self.get_statistics()
            present = stats['present_today']
            total = stats['total_students']
            
            if total > 0:
                percentage = (present / total) * 100
                self.speak(f"{present} out of {total} students are present today. That's {percentage:.1f} percent attendance")
                
                # Get attendance details
                attendance = self.get_today_attendance()
                if attendance and len(attendance) <= 5:
                    names = [a.get('Name', 'Unknown') for a in attendance]
                    self.speak(f"Present students: {', '.join(names)}")
            else:
                self.speak(f"{present} students are present today")
            return None
        
        elif 'attendance percentage' in command or 'attendance rate' in command:
            self.speak("Calculating attendance percentage")
            stats = self.get_statistics()
            present = stats['present_today']
            total = stats['total_students']
            
            if total > 0:
                percentage = (present / total) * 100
                self.speak(f"Today's attendance rate is {percentage:.1f} percent. "
                          f"{present} present out of {total} total students")
            else:
                self.speak("No students are registered yet")
            return None
        
        # === PHOTOS & TRAINING ===
        elif 'photos' in command or 'images' in command or 'photo samples' in command:
            self.speak("Checking photo samples")
            stats = self.get_statistics()
            photos = stats['photos_collected']
            self.speak(f"There are {photos} photo samples collected in the system. "
                      f"You need at least 100 samples per student for good accuracy")
            return None
        
        elif 'model trained' in command or 'is model trained' in command or 'training status' in command:
            self.speak("Checking model training status")
            stats = self.get_statistics()
            if stats['models_trained'] > 0:
                self.speak("Yes, the face recognition model has been trained and is ready to use. "
                          "You can now start the face recognition module")
            else:
                self.speak("The model has not been trained yet. Please capture photo samples and train the model first")
            return None
        
        elif 'how to train' in command or 'train the model' in command:
            self.speak("To train the model, first capture at least 100 photo samples per student, "
                      "then go to the Train Data module and click the Train button")
            return None
        
        # === SYSTEM STATUS ===
        elif 'system status' in command or 'status report' in command or 'overall status' in command:
            self.speak("Generating system status report")
            stats = self.get_statistics()
            self.speak(f"System status report: {stats['total_students']} students registered, "
                      f"{stats['present_today']} present today, "
                      f"{stats['photos_collected']} photo samples collected, "
                      f"and model is {'trained and ready' if stats['models_trained'] else 'not trained yet'}")
            return None
        
        # === OPEN MODULES ===
        elif 'open student management' in command or ('open' in command and 'student' in command):
            self.speak("Opening Student Management System now")
            return ('open_module', 'student_management')
        
        elif 'open face recognition' in command or ('open' in command and 'face' in command and 'recognition' in command):
            stats = self.get_statistics()
            if stats['models_trained'] > 0:
                self.speak("Opening Face Recognition Module now")
                return ('open_module', 'face_recognition')
            else:
                self.speak("The model is not trained yet. Please train the model first before using face recognition")
                return None
        
        elif 'open attendance' in command or ('open' in command and 'attendance' in command):
            self.speak("Opening Attendance Viewer now")
            return ('open_module', 'attendance')
        
        elif 'open training' in command or ('open' in command and 'train' in command):
            self.speak("Opening Training Module now")
            return ('open_module', 'train_data')
        
        elif 'open photo' in command or ('open' in command and 'photo' in command):
            self.speak("Opening Photo Capture Module now")
            return ('open_module', 'photos')
        
        elif 'open help' in command or ('open' in command and 'help' in command):
            self.speak("Opening Help Desk now")
            return ('open_module', 'help_desk')
        
        elif 'open developer' in command or ('open' in command and 'developer' in command):
            self.speak("Opening Developer Information now")
            return ('open_module', 'developer')
        
        elif 'open settings' in command or ('open' in command and 'settings' in command):
            self.speak("Opening Settings now")
            return ('open_module', 'settings')
        
        # === CLOSE MODULES ===
        elif 'close student management' in command or ('close' in command and 'student' in command):
            self.speak("Closing Student Management System now")
            return ('close_module', 'student_management')
        
        elif 'close face recognition' in command or ('close' in command and 'face' in command and 'recognition' in command):
            self.speak("Closing Face Recognition Module now")
            return ('close_module', 'face_recognition')
        
        elif 'close attendance' in command or ('close' in command and 'attendance' in command):
            self.speak("Closing Attendance Viewer now")
            return ('close_module', 'attendance')
        
        elif 'close training' in command or ('close' in command and 'train' in command):
            self.speak("Closing Training Module now")
            return ('close_module', 'train_data')
        
        elif 'close photo' in command or ('close' in command and 'photo' in command):
            self.speak("Closing Photo Capture Module now")
            return ('close_module', 'photos')
        
        elif 'close all' in command or 'close everything' in command:
            self.speak("Closing all open modules now")
            return ('close_all_modules', None)
        
        # === HELP & INFORMATION ===
        elif 'help' in command or 'what can you do' in command or 'your capabilities' in command:
            self.speak("I can help you with many things! I can open and close any system module, "
                      "check statistics like student count and attendance, "
                      "tell you the time and date, provide system status, "
                      "answer questions about the attendance system, and much more. "
                      "Just ask me anything or tell me to open or close a specific module!")
            return None
        
        elif 'how does it work' in command or 'how to use' in command or 'workflow' in command:
            self.speak("The workflow is simple: First, add students in Student Management. "
                      "Then, capture photo samples for each student. "
                      "Next, train the model in Train Data module. "
                      "Finally, use Face Recognition to mark attendance automatically. "
                      "Would you like me to open any module?")
            return None
        
        elif 'features' in command or 'what features' in command:
            self.speak("Key features include: Automatic face detection and recognition, "
                      "real-time attendance marking, ID card verification, "
                      "liveness detection for security, comprehensive student management, "
                      "and me, your voice assistant!")
            return None
        
        # === WHO/WHAT QUESTIONS ===
        elif 'who created you' in command or 'who made you' in command or 'your creator' in command:
            self.speak("I was created by SMIT students as part of the Face Recognition Attendance System project")
            return None
        
        elif 'what is your name' in command or 'your name' in command:
            self.speak("My name is DISHA. It stands for Digital Intelligent System for Human Assistance")
            return None
        
        # === REFRESH/UPDATE ===
        elif 'refresh' in command or 'update statistics' in command or 'reload data' in command:
            self.speak("Refreshing system statistics now")
            self.last_stats_update = None
            stats = self.get_statistics()
            self.speak("Statistics refreshed successfully")
            return ('refresh_stats', None)
        
        # === EXIT/STOP ===
        elif 'exit' in command or 'stop listening' in command or 'goodbye' in command or 'bye' in command or 'deactivate' in command:
            self.speak("Goodbye! Have a great day! Say 'Hey DISHA' anytime you need me.")
            return ('exit', None)
        
        # === UNKNOWN COMMAND ===
        else:
            self.speak("I'm not sure I understood that. You can ask me about statistics, "
                      "system status, or tell me to open or close any module. "
                      "Say 'help' for more options")
            return None
    
    def continuous_listen(self, callback=None):
        """Continuously listen for wake word and commands"""
        self.is_active = True
        self.speak("DISHA is now active and ready. Say 'Hey DISHA' followed by your command")
        
        while self.is_active:
            # Listen for wake word
            text = self.listen(timeout=10)
            
            if text:
                # Check for wake word
                wake_detected = False
                for wake_word in self.wake_words:
                    if wake_word in text:
                        wake_detected = True
                        # Extract command after wake word
                        command = text.split(wake_word, 1)[-1].strip()
                        break
                
                if wake_detected:
                    if command:
                        # Process the command immediately
                        result = self.process_command(command)
                        
                        # Call callback if provided
                        if callback and result:
                            callback(result)
                        
                        # Check for exit
                        if result and result[0] == 'exit':
                            self.is_active = False
                            break
                    else:
                        # No command after wake word, listen again
                        self.speak("Yes? I'm listening")
                        
                        # Listen for command
                        command = self.listen(timeout=5)
                        
                        if command:
                            result = self.process_command(command)
                            
                            # Call callback if provided
                            if callback and result:
                                callback(result)
                            
                            # Check for exit
                            if result and result[0] == 'exit':
                                self.is_active = False
                                break
    
    def stop(self):
        """Stop DISHA"""
        self.is_active = False
        self.speak("DISHA deactivated")


# Integration with main UI
class DISHAIntegration:
    """
    Integrate DISHA with the Face Recognition UI
    FIXED: Proper window tracking and closing
    """
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.disha = DISHA()
        self.is_running = False
        self.listen_thread = None
        
        # Track open module windows using Toplevel references
        self.open_windows = {
            'student_management': None,
            'face_recognition': None,
            'attendance': None,
            'train_data': None,
            'photos': None
        }
    
    def start(self):
        """Start DISHA in background thread"""
        if not self.is_running:
            self.is_running = True
            self.disha.greet()
            
            # Start listening in background
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
        """Handle commands from DISHA"""
        command_type, data = result
        
        if command_type == 'open_module':
            # Schedule module opening in main thread
            self.main_window.after(100, lambda: self.open_module(data))
        
        elif command_type == 'close_module':
            # Schedule module closing in main thread
            self.main_window.after(100, lambda: self.close_module(data))
        
        elif command_type == 'close_all_modules':
            # Close all open modules
            self.main_window.after(100, self.close_all_modules)
        
        elif command_type == 'refresh_stats':
            # Refresh statistics in main UI
            try:
                if hasattr(self.main_window, 'update_statistics'):
                    self.main_window.after(100, self.main_window.update_statistics)
                elif hasattr(self.main_window, 'refresh_statistics_manual'):
                    self.main_window.after(100, self.main_window.refresh_statistics_manual)
            except:
                pass
        
        elif command_type == 'exit':
            self.stop()
    
    def open_module(self, module_name):
        """Open the requested module - SPEECH ALREADY DONE"""
        try:
            # Import and open the module
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
            # Speak error in separate thread to avoid blocking
            threading.Thread(target=self.disha.speak, 
                           args=(f"Error opening module: {str(e)}",), 
                           daemon=True).start()
    
    def close_module(self, module_name):
        """Close specific module - SPEECH ALREADY DONE"""
        try:
            if module_name in self.open_windows:
                window = self.open_windows[module_name]
                
                if window and self._is_window_open(window):
                    window.destroy()
                    self.open_windows[module_name] = None
                    
                    # Confirm closure
                    threading.Thread(target=self.disha.speak, 
                                   args=("Module closed successfully",), 
                                   daemon=True).start()
                else:
                    # Window not open
                    threading.Thread(target=self.disha.speak, 
                                   args=("This module is not currently open",), 
                                   daemon=True).start()
                    
        except Exception as e:
            threading.Thread(target=self.disha.speak, 
                           args=(f"Error closing module: {str(e)}",), 
                           daemon=True).start()
    
    def close_all_modules(self):
        """Close all open module windows - SPEECH ALREADY DONE"""
        try:
            closed_count = 0
            for module_name in self.open_windows:
                window = self.open_windows[module_name]
                if window and self._is_window_open(window):
                    try:
                        window.destroy()
                        closed_count += 1
                    except:
                        pass
                self.open_windows[module_name] = None
            
            if closed_count > 0:
                threading.Thread(target=self.disha.speak, 
                               args=(f"Closed {closed_count} window{'s' if closed_count > 1 else ''}",), 
                               daemon=True).start()
            else:
                threading.Thread(target=self.disha.speak, 
                               args=("No open modules to close",), 
                               daemon=True).start()
                
        except Exception as e:
            threading.Thread(target=self.disha.speak, 
                           args=(f"Error closing modules: {str(e)}",), 
                           daemon=True).start()
    
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
    print("="*60)
    print("DISHA - Digital Intelligent System for Human Assistance")
    print("COMPLETE REWRITE - All Issues Fixed")
    print("="*60)
    print()
    
    # Test DISHA
    disha = DISHA()
    disha.greet()
    
    print("\nAvailable commands:")
    print("\n📊 STATISTICS:")
    print("- 'Hey DISHA, how many students are registered?'")
    print("- 'Hey DISHA, who is present today?'")
    print("- 'Hey DISHA, system status'")
    print("\n🚀 OPEN MODULES:")
    print("- 'Hey DISHA, open student management'")
    print("- 'Hey DISHA, open face recognition'")
    print("- 'Hey DISHA, open attendance'")
    print("\n❌ CLOSE MODULES:")
    print("- 'Hey DISHA, close student management'")
    print("- 'Hey DISHA, close face recognition'")
    print("- 'Hey DISHA, close all modules'")
    print("\n❓ QUESTIONS:")
    print("- 'Hey DISHA, what time is it?'")
    print("- 'Hey DISHA, help'")
    print("- 'Hey DISHA, goodbye'")
    print()
    
    try:
        disha.continuous_listen()
    except KeyboardInterrupt:
        print("\nStopping DISHA...")

        disha.stop()
