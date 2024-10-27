import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import os
import json
import time
import threading
import webbrowser

API_KEY_FILE = "apikey.json"

def load_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as file:
            data = json.load(file)
            return data.get("apikey")
    return None

def save_api_key(apikey):
    with open(API_KEY_FILE, "w") as file:
        json.dump({"apikey": apikey}, file)

def prompt_for_api_key():
    api_window = tk.Toplevel(root)
    api_window.title("Enter API Key")
    api_window.configure(bg="#2a2d36")

    tk.Label(api_window, text="Enter API Key:", bg="#2a2d36", fg="white", font=("Helvetica", 12)).pack(pady=10)
    api_entry = ttk.Entry(api_window, width=40, font=("Helvetica", 12))
    api_entry.pack(pady=5)

    def save_and_close():
        apikey = api_entry.get()
        if apikey:
            save_api_key(apikey)
            api_key_label.config(text=f"Current API Key: {apikey}")
            api_window.destroy()
            messagebox.showinfo("Success", "API Key saved!")
        else:
            messagebox.showerror("Error", "API Key cannot be empty.")

    ttk.Button(api_window, text="Save API Key", command=save_and_close, style="Accent.TButton").pack(pady=15)

def send_sms():
    apikey = load_api_key()
    if not apikey:
        messagebox.showerror("Error", "API Key not found. Please enter the API Key first.")
        return

    url = "https://sms.anbuinfosec.xyz/api/sms"
    mobile = mobile_entry.get()
    msg = message_entry.get()

    params = {
        "apikey": apikey,
        "mobile": mobile,
        "msg": msg
    }

    def request_sms():
        processing_label.config(text="Sending...", fg="orange")
        try:
            response = requests.get(url, params=params)
            response_data = response.json()
            
            if response.status_code == 200 and response_data.get("success", False):
                info_message = (
                    f"Message sent successfully!\n\n"
                    f"Mobile: {response_data['mobile']}\n"
                    f"Message: {response_data['msg']}\n"
                    f"New Balance: {response_data['newBalance']}\n"
                    f"IP: {response_data['ip']}"
                )
                messagebox.showinfo("Success", info_message)
            else:
                error_message = response_data.get("message", "Unknown error occurred.")
                messagebox.showwarning("Failed", f"Error: {error_message}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            processing_label.config(text="")

    threading.Thread(target=request_sms).start()

def change_api_key():
    prompt_for_api_key()

def open_website():
    webbrowser.open("https://anbuinfosec.xyz")

def fade_in(window, delay=10, step=0.1):
    alpha = 0.0
    while alpha < 1.0:
        window.attributes("-alpha", alpha)
        alpha += step
        window.update()
        time.sleep(delay / 1000)

root = tk.Tk()
root.title("ANON SMS")
root.geometry("450x500")
root.configure(bg="#181c24")
root.resizable(False, False)

root.attributes("-alpha", 0.0)
fade_in(root)

style = ttk.Style()
style.configure("TLabel", background="#181c24", font=("Helvetica", 10), foreground="white")
style.configure("TButton", font=("Helvetica", 10), padding=5, relief="flat")
style.configure("Accent.TButton", font=("Helvetica", 12), padding=6, background="#4CAF50", foreground="white")
style.map("Accent.TButton", background=[("active", "#45A049")])

header_frame = tk.Frame(root, bg="#20232a", height=60)
header_frame.pack(fill="x")
header = tk.Label(header_frame, text="ANON SMS", bg="#20232a", fg="white", font=("Helvetica", 16, "bold"))
header.pack(pady=15)

apikey = load_api_key()
api_key_label = tk.Label(root, text=f"Current API Key: {apikey if apikey else 'Not Set'}", bg="#181c24", fg="white", font=("Helvetica", 10))
api_key_label.pack(pady=15)

content_frame = tk.Frame(root, bg="#181c24")
content_frame.pack(pady=10)

mobile_label = ttk.Label(content_frame, text="Mobile Number:", font=("Helvetica", 11))
mobile_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
mobile_entry = ttk.Entry(content_frame, width=30, font=("Helvetica", 11))
mobile_entry.grid(row=0, column=1, padx=10, pady=5)

message_label = ttk.Label(content_frame, text="Message:", font=("Helvetica", 11))
message_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
message_entry = ttk.Entry(content_frame, width=30, font=("Helvetica", 11))
message_entry.grid(row=1, column=1, padx=10, pady=5)

button_frame = tk.Frame(root, bg="#181c24")
button_frame.pack(pady=20)

send_button = ttk.Button(button_frame, text="Send SMS", command=send_sms, style="Accent.TButton")
send_button.grid(row=0, column=0, padx=10, pady=10)

change_key_button = ttk.Button(button_frame, text="Change API Key", command=change_api_key, style="Accent.TButton")
change_key_button.grid(row=0, column=1, padx=10, pady=10)

processing_label = tk.Label(root, text="", bg="#181c24", fg="yellow", font=("Helvetica", 10, "italic"))
processing_label.pack(pady=10)

footer_frame = tk.Frame(root, bg="#20232a", height=40)
footer_frame.pack(fill="x")
footer = tk.Label(footer_frame, text="Powered by ANONSMS", bg="#20232a", fg="white", font=("Helvetica", 8), cursor="hand2")
footer.pack(pady=10)
footer.bind("<Button-1>", lambda e: open_website())

root.mainloop()
