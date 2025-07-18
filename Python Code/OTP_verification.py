import re
import random
import ssl
import smtplib
from email.message import EmailMessage
import tkinter as tk
from tkinter import messagebox

# --------------- CONSTANTS --------------- 
SENDER_EMAIL = 'madaandikshant11@gmail.com' # replace with your email id
SENDER_PASSWORD = 'gtqj dyfg olnd vjth' # Replace with your 16 character app password
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

otp_value = "" # Global variable to store OTP
attempt_counter = 3

# TIMER FUNCTION FOR COUNTDOWN AFTER SENDING OTP
def start_timer(seconds=30):
    def countdown():
        nonlocal seconds
        if seconds > 0:
            mins, secs = divmod(seconds, 60)
            timer_label.config(text=f"Time left: {mins:02d}:{secs:02d}")
            seconds -= 1
            otp_frame.after(1000, countdown)
        else:
            timer_label.config(text="OTP expired.")
            verify_button.config(state=tk.DISABLED)
            otp_entry.config(state=tk.DISABLED)
    
    countdown()

# ------------------ FUNCTION TO SEND OTP TO USER -------------------
def send_otp(receiver_email):
    global otp_value
    if not is_valid_email(receiver_email):
        messagebox.showerror("Invalid Email","Please enter a valid email address")
        return
    
    otp_value = generate_otp()
    msg = EmailMessage()
    msg.set_content(f"Your otp is: {otp_value}")
    msg['Subject'] = "OTP Verification"
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        messagebox.showinfo("Success","OTP sent to your email")
        otp_frame.pack(pady=10)

        otp_entry.config(state=tk.NORMAL) # ENABLE ENTRY FIELD BACK TO NORMAL
        verify_button.config(state=tk.NORMAL) # ENABLE BUTTON BACK TO NORMAL
        start_timer(30)  # START TIMER FUNCTION

    
    except Exception as e:
        messagebox.showerror("Error",f"Failed to send OTP: {e}")


# ------------------ FUNCTION TO GENERATE OTP -------------------
def generate_otp(length=6) -> str:
    otp = str(random.randint(100000, 999999))
    return otp


# ------------------ FUNCTION TO VERIFY EMAIL -------------------
def is_valid_email(email):
    # Regular expression pattern for a valid email
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None


# --------------------- OTP VERIFICATION FUNCTION ---------------------
def verify_otp(user_otp):
    global attempt_counter
    if user_otp == otp_value:
        messagebox.showinfo("Success","OTP Verified. Access Granted")
        window.destroy()
    else:
        attempt_counter -= 1
        if attempt_counter > 0:
            messagebox.showerror("Error",f"Incorrect OTP. Attempt left {attempt_counter}")
        else:
            messagebox.showerror("Error","Maximum attempts exceeded. Access Denied")
            window.destroy()

# ******************** GUI Setup ********************
window = tk.Tk()
window.title("OTP Verification")
window.geometry("400x300")
window.resizable(False, False)

# TITLE
title_label = tk.Label(window, text="OTP Verification System", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# EMAIL ENTRY
email_label = tk.Label(window, text="Enter Email: ")
email_label.pack(pady=10)
email_entry = tk.Entry(window, width=40)
email_entry.pack(padx=5)

# SEND BUTTON
send_button = tk.Button(window, text="Send OTP", command=lambda: send_otp(email_entry.get()))
send_button.pack(padx=10)

# OTP ENTRY FRAME
otp_frame = tk.Frame(window)

# LABEL FOR OTP ENTRY BOX
otp_label = tk.Label(otp_frame, text="Enter otp: ")
otp_label.pack()
otp_entry = tk.Entry(otp_frame, width=20)
otp_entry.pack(pady=5)

# LABEL FOR THE TIMER
timer_label = tk.Label(otp_frame, text="", fg="red", font=("Arial", 10, "bold"))
timer_label.pack()

# VERIFY BUTTON
verify_button = tk.Button(otp_frame, text="Verify OTP", command=lambda: verify_otp(otp_entry.get()))
verify_button.pack()

# RUN THE APP
window.mainloop()