import customtkinter as ctk  # The modern UI library
import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import os
import sqlite3
import pyttsx3
import threading
import time

# --- CONFIGURATION ---
DB_NAME = 'library.db'
TRAINER_PATH = 'trainer/trainer.yml'
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Set the Theme (Dark Mode)
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue") 

class LibraryApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Neural Library System v2.0")
        self.window.geometry("1100x700")

        # Initialize Voice Engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150) # Speed of speech
        self.last_spoken_time = 0 # To prevent spamming voice

        # Load AI Models
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        if os.path.exists(TRAINER_PATH):
            self.recognizer.read(TRAINER_PATH)
        else:
            messagebox.showerror("Error", "Trainer file not found!")
            return

        self.face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

        # UI Layout
        self.create_futuristic_widgets()

        # Camera Setup
        self.cap = cv2.VideoCapture(0)
        self.current_person_id = -1
        self.update_webcam()

    def speak(self, text):
        """Runs voice in a separate thread so video doesn't freeze"""
        def _speech():
            self.engine.say(text)
            self.engine.runAndWait()
        
        # Only speak if 5 seconds have passed since last speech
        if time.time() - self.last_spoken_time > 5:
            self.last_spoken_time = time.time()
            threading.Thread(target=_speech).start()

    def create_futuristic_widgets(self):
        # 1. Main Grid Layout
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        # --- LEFT SIDEBAR (Controls) ---
        self.sidebar = ctk.CTkFrame(self.window, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Logo / Title
        self.logo_label = ctk.CTkLabel(self.sidebar, text="NEURAL\nLIBRARY", font=ctk.CTkFont(size=25, weight="bold"))
        self.logo_label.pack(pady=30)

        # Status Panel
        self.lbl_status = ctk.CTkLabel(self.sidebar, text="SYSTEM STATUS:\nSCANNING", font=ctk.CTkFont(size=14), text_color="cyan")
        self.lbl_status.pack(pady=20)

        # Buttons (Hidden by default)
        self.btn_issue = ctk.CTkButton(self.sidebar, text="[+] ISSUE BOOK", fg_color="#2ecc71", hover_color="#27ae60", command=self.issue_book_window)
        self.btn_return = ctk.CTkButton(self.sidebar, text="[-] RETURN BOOK", fg_color="#e74c3c", hover_color="#c0392b", command=self.return_book_action)

        # --- RIGHT MAIN AREA ---
        self.main_area = ctk.CTkFrame(self.window, corner_radius=10, fg_color="#1a1a1a")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Video Frame
        self.video_label = tk.Label(self.main_area, bg="black", bd=0)
        self.video_label.pack(pady=20)

        # User Info Panel (Below Video)
        self.info_frame = ctk.CTkFrame(self.main_area, height=150, fg_color="transparent")
        self.info_frame.pack(fill="x", padx=20)

        self.lbl_name = ctk.CTkLabel(self.info_frame, text="USER: UNKNOWN", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_name.pack(anchor="w")

        self.lbl_role = ctk.CTkLabel(self.info_frame, text="ACCESS LEVEL: RESTRICTED", font=ctk.CTkFont(size=14), text_color="red")
        self.lbl_role.pack(anchor="w")

        # Book List (Modern Textbox instead of Listbox)
        self.book_display = ctk.CTkTextbox(self.info_frame, height=100, font=("Consolas", 14))
        self.book_display.pack(fill="x", pady=10)
        self.book_display.insert("0.0", ">> WAITING FOR BIOMETRIC DATA...")
        self.book_display.configure(state="disabled")

    def draw_hud(self, img, x, y, w, h, name, conf):
        """Draws a cool Sci-Fi box around the face"""
        color = (0, 255, 255) if name != "Unknown" else (0, 0, 255) # Yellow/Cyan vs Red
        
        # Corners instead of a full box
        l = 30 # length of corner line
        t = 2  # thickness
        
        # Top Left
        cv2.line(img, (x, y), (x + l, y), color, t)
        cv2.line(img, (x, y), (x, y + l), color, t)
        # Top Right
        cv2.line(img, (x + w, y), (x + w - l, y), color, t)
        cv2.line(img, (x + w, y), (x + w, y + l), color, t)
        # Bottom Left
        cv2.line(img, (x, y + h), (x + l, y + h), color, t)
        cv2.line(img, (x, y + h), (x, y + h - l), color, t)
        # Bottom Right
        cv2.line(img, (x + w, y + h), (x + w - l, y + h), color, t)
        cv2.line(img, (x + w, y + h), (x + w, y + h - l), color, t)

        # Scan Line (Moving effect)
        scan_line_y = y + int((time.time() * 100) % h)
        cv2.line(img, (x, scan_line_y), (x+w, scan_line_y), (0, 255, 0), 1)

        # Text Overlay
        cv2.putText(img, f"TARGET: {name.upper()}", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
        cv2.putText(img, f"CONFIDENCE: {conf}%", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    def update_webcam(self):
        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.2, 5)

            detected_id = -1
            
            for (x, y, w, h) in faces:
                id, distance = self.recognizer.predict(gray[y:y+h, x:x+w])
                
                confidence = round(100 - distance)
                
                if distance < 60: 
                    detected_id = id
                    # Get name immediately for HUD
                    user = self.get_user_from_db(id)
                    name = user[0] if user else "Unknown"
                    self.draw_hud(frame, x, y, w, h, name, confidence)
                else:
                    self.draw_hud(frame, x, y, w, h, "Unknown", confidence)

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

            if detected_id != self.current_person_id and detected_id != -1:
                self.handle_new_person(detected_id)

        self.window.after(15, self.update_webcam)

    def handle_new_person(self, user_id):
        self.current_person_id = user_id
        user_info = self.get_user_from_db(user_id)
        
        if user_info:
            name, role = user_info
            
            # Update UI
            self.lbl_name.configure(text=f"USER: {name.upper()}")
            self.lbl_status.configure(text="STATUS: VERIFIED", text_color="#2ecc71")
            
            if role == "Librarian":
                self.lbl_role.configure(text="ACCESS LEVEL: ADMIN (UNLOCKED)", text_color="#2ecc71")
                self.btn_issue.pack(pady=10, padx=20, fill="x")
                self.btn_return.pack(pady=10, padx=20, fill="x")
                self.speak(f"Welcome Admin {name}. System unlocked.")
            else:
                self.lbl_role.configure(text="ACCESS LEVEL: STUDENT", text_color="cyan")
                self.btn_issue.pack_forget()
                self.btn_return.pack_forget()
                self.speak(f"Welcome student {name}.")

            # Update Books
            self.refresh_book_list(user_id)
        else:
            self.speak("User not found.")

    def refresh_book_list(self, user_id):
        books = self.get_books_from_db(user_id)
        self.book_display.configure(state="normal")
        self.book_display.delete("0.0", "end")
        
        if books:
            self.book_display.insert("0.0", ">> CURRENTLY BORROWED:\n\n")
            for book in books:
                self.book_display.insert("end", f"[O] {book}\n")
        else:
             self.book_display.insert("0.0", ">> NO ACTIVE LOANS DETECTED.")
             
        self.book_display.configure(state="disabled")

    # --- DATABASE HELPERS ---
    def get_user_from_db(self, user_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name, role FROM students WHERE id=?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def get_books_from_db(self, user_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM books WHERE borrowed_by_id=?", (user_id,))
        results = cursor.fetchall()
        conn.close()
        return [r[0] for r in results]

    def issue_book_window(self):
        # Using standard Tkinter for popups as CTK popups are complex
        dialog = ctk.CTkInputDialog(text="Enter Book Title:", title="Issue Book")
        book_title = dialog.get_input()
        
        # For Student ID, we need another dialog or use the current student
        # For simplicity, let's assume we are issuing to YOURSELF (Student ID 1) for testing
        # Or add another input dialog
        if book_title:
             self.save_book_db(book_title, 1) # Hardcoded to ID 1 for quick testing

    def save_book_db(self, title, student_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, borrowed_by_id) VALUES (?, ?, ?)", (title, 'Unknown', student_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Book Issued!")
        if self.current_person_id == student_id:
            self.refresh_book_list(student_id)

    def return_book_action(self):
        # Basic return logic - deletes the last book for demo purposes
        # Since textboxes aren't clickable like listboxes, we simplified this
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE borrowed_by_id=?", (self.current_person_id,))
        conn.commit()
        conn.close()
        self.speak("All books returned.")
        self.refresh_book_list(self.current_person_id)

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    root = ctk.CTk()
    app = LibraryApp(root)
    root.mainloop()