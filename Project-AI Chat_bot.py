import sys
import datetime

# =============================================================================
# PROJECT: College Enquiry Chatbot (Rule-Based)
# TEAM SIZE: 5 Members
# DESCRIPTION: A simple AI bot to answer student questions about college.
# =============================================================================

def greet_user():
    """Gets the current time and returns a greeting."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good Morning"
    elif 12 <= hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

# =============================================================================
# MODULE 1: ADMISSIONS (Friend 1)
# Handles questions about dates, cutoffs, documents, and process.
# =============================================================================
def get_admission_info(text):
    if "cutoff" in text:
        return "For AI & DS, last year's cutoff was 70 percentile in CET."
    elif "date" in text or "start" in text:
        return "Admission forms will be available from June 15th on the website."
    elif "document" in text:
        return "Required Documents: 10th/12th Marksheet, LC, Aadhar, and Caste Certificate (if applicable)."
    elif "branch" in text or "seat" in text:
        return "We have 120 seats for AI & DS and 120 seats for other all branches but 180 for Computer Engineering."
    elif "donation" in text or "management" in text:
        return "Please visit the Principal's office for management quota enquiries."
    else:
        return None

# =============================================================================
# MODULE 2: FEES & SCHOLARSHIPS (Friend 2)
# Handles questions about costs, scholarships, and payment modes.
# =============================================================================
# =============================================================================
# MODULE 2: FEES & SCHOLARSHIPS (FIXED VERSION)
# =============================================================================
def get_fee_info(text):
    # 1. Check for specific items (Hostel, Bus) FIRST
    if "hostel" in text:
        return "Hostel Fee: 25,000 INR (Lodging) + 25,000 INR (Mess) per year."
    
    # 2. Check for Scholarships/Categories
    # We use 'text.split()' to find exact words so 'cost' or 'hostel' don't trigger 'st'
    words = text.split() 
    
    if "scholarship" in text or "ebc" in text:
        return "EBC Scholarship is available for income below 8 Lakhs. You get 50% tuition fee waiver."
    elif "obc" in text:
        return "For OBC category, the fee is approx 47,000 INR per year."
    elif "sc" in words or "st" in words: # Only triggers if "st" is a separate word
        return "For SC/ST candidates, tuition fee is 100% waived. You only pay development fees."
    
    # 3. Check for general Fee/Cost LAST
    elif "fee" in text or "cost" in text:
        return "Open Category Total Fee: 84,000 INR per year."
    else:
        return None

# =============================================================================
# MODULE 3: ACADEMICS & EXAMS (Friend 3)
# Handles questions about syllabus, teachers, and exam patterns.
# =============================================================================
def get_academic_info(text):
    if "subject" in text or "syllabus" in text:
        return "First Year Subjects: Problem solving programming, Engg Mathematics-I, Apllied Physics and Chemistry, Software Engineering, and ED+LL+BCS."
    elif "exam" in text:
        return "In-Sem exams (40 marks) [MCQ-based]. End-Sem exams (60 marks) are in Jan."
    elif "attendance" in text:
        return "75% attendance is strictly mandatory to sit for exams."
    elif "kt" in text or "fail" in text:
        return "If you fail, you can attempt the backlog exam in the next semester."
    elif "timing" in text or "hour" in text:
        return "College timings are 8:00 AM to 3:00 PM, Monday to Friday."
    else:
        return None

# =============================================================================
# MODULE 4: FACILITIES & HOSTEL (Friend 4)
# Handles questions about wifi, library, canteen, gym, etc.
# =============================================================================
def get_facility_info(text):
    if "library" in text:
        return "The Central Library is open 24/7 during exam periods. Normal timings: 8 AM - 11 PM."
    elif "wifi" in text or "internet" in text:
        return "Free Campus Wi-Fi is available. Register your laptop MAC address at the IT cell."
    elif "mess" in text or "canteen" in text:
        return "We have 2 canteens. A full thali costs 60 INR. Snacks are available all day."
    elif "gym" in text or "sport" in text:
        return "There is a gym in the College basement and a cricket ground behind the main building."
    elif "bus" in text or "transport" in text:
        return "College buses run many routes covering the whole Nashik city. Pass cost: ~30,000 INR/year."
    else:
        return None

# =============================================================================
# MODULE 5: MAIN CONTROLLER (Friend 5 / Team Lead)
# Controls the flow, handles greetings, and combines all modules.
# =============================================================================
def start_chat():
    print("**************************************************")
    print(f"🤖  {greet_user()}! Welcome to the Matoshri College Enquiry Chatbot.")
    print("    I can answer questions about:")
    print("    1. Admissions & Cutoffs")
    print("    2. Fees & Scholarships")
    print("    3. Exams & Syllabus")
    print("    4. Hostel & Facilities")
    print("\n    (Type 'exit' or 'bye' to stop chatting)")
    print("**************************************************")

    while True:
        try:
            # 1. Take Input
            user_input = input("\nYou: ").strip()

            # 2. Check for empty input
            if not user_input:
                continue

            # 3. Clean Input (Lowercase for easy matching)
            cleaned_input = user_input.lower()

            # 4. Exit Logic
            if cleaned_input in ["exit", "bye", "quit", "stop"]:
                print("Bot: Thank you for visiting. Best of luck for your future!")
                break
            
            # 5. Small Talk Logic
            if cleaned_input in ["hello", "hi", "hey"]:
                print("Bot: Hello there! Ask me anything about the college.")
                continue
            elif "thank" in cleaned_input:
                print("Bot: You are welcome!")
                continue
            elif "who are you" in cleaned_input:
                print("Bot: I am a Matoshri College Chatbot created by First Year AI & DS students.")
                continue

            # 6. Check Modules one by one
            # If a module finds an answer, print it and 'continue' to next loop iteration
            
            response = get_admission_info(cleaned_input)
            if response:
                print(f"Bot: {response}")
                continue

            response = get_fee_info(cleaned_input)
            if response:
                print(f"Bot: {response}")
                continue

            response = get_academic_info(cleaned_input)
            if response:
                print(f"Bot: {response}")
                continue
            
            response = get_facility_info(cleaned_input)
            if response:
                print(f"Bot: {response}")
                continue

            # 7. Fallback (If no keyword matches)
            print("Bot: I'm sorry, I didn't understand that. Please ask for 'Fees', 'Hostel', 'Exam', or 'Admission'.")

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nBot: Exiting...")
            sys.exit()

# Start the program
if __name__ == "__main__":
    start_chat()