import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from twilio.rest import Client
import os

# Twilio credentials (replace with yours)
account_sid = 'YOUR_TWILIO_SID'
auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
twilio_number = 'YOUR_TWILIO_PHONE_NUMBER'

client = Client(account_sid, auth_token)

def make_call(name, phone, language, gender, service):
    # Choose voice and language
    if language == 'English':
        twilio_lang = 'en-US'
    elif language == 'Hindi':
        twilio_lang = 'hi-IN'
    elif language == 'Telugu':
        twilio_lang = 'te-IN'
    else:
        twilio_lang = 'en-US'

    voice = 'Polly.Joanna' if gender == 'Male' else 'Polly.Matthew'  # Reverse gender voice

    message = f"Hello {name}, this is a feedback call for your recent {service} service. How was your experience?"

    twiml = f"""
        <Response>
            <Say language="{twilio_lang}" voice="{voice}">{message}</Say>
        </Response>
    """

    try:
        call = client.calls.create(
            twiml=twiml,
            to=phone,
            from_=twilio_number
        )
        return "Success"
    except Exception as e:
        print(f"Call failed for {name}: {e}")
        return "Failed"

def start_calls():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    df = pd.read_csv(file_path)

    success_data = []
    failed_data = []

    for _, row in df.iterrows():
        name = row['Name']
        phone = row['Phone']
        language = row['Language']
        gender = row['Gender']
        service = row['Service']

        result = make_call(name, phone, language, gender, service)
        if result == "Success":
            success_data.append(row)
        else:
            failed_data.append(row)

    if success_data:
        pd.DataFrame(success_data).to_csv("call_success.csv", index=False)
    if failed_data:
        pd.DataFrame(failed_data).to_csv("call_failed.csv", index=False)

    messagebox.showinfo("Done", "Calls completed.\nCheck call_success.csv and call_failed.csv")

# GUI setup
root = tk.Tk()
root.title("AI Call Center Agent")
root.geometry("400x200")

label = tk.Label(root, text="Click to start feedback calls", font=("Arial", 14))
label.pack(pady=20)

btn = tk.Button(root, text="Start Calls", command=start_calls, font=("Arial", 12), bg="blue", fg="white")
btn.pack(pady=10)

root.mainloop()
