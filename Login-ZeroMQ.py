import tkinter as tk
from tkinter import messagebox
import hashlib
import zmq
import os
from ctypes import windll as ctypes_windll

# Make it high-res, even in Windows 10 or above
ctypes_windll.shcore.SetProcessDpiAwareness(1)

# Function to center the window both vertically and horizontally
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

# Function to hash a password using SHA-512
def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()

# Global variables for ZeroMQ context and socket
context = None
socket = None

def setup_zmq():
    global context, socket
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

def authenticate(username, password):
    global socket
    hashed_password = hash_password(password)
    request = f"{username.lower()},{hashed_password}"
    print(f"Login Data: {request}")
    socket.send_string(request)

def check_for_response():
    try:
        response = socket.recv_string(zmq.DONTWAIT)
        print(f"Received response: {response}")
        if response == "Authenticated":
            messagebox.showinfo('Login Info', 'Login successful!')
        else:
            messagebox.showerror('Login Info', 'Invalid username or password.')
    except zmq.Again:
        pass
    finally:
        root.after(100, check_for_response)  # Schedule next check

def login():
    username = entryUsername.get()
    password = entryPassword.get()
    setup_zmq()  # Setup ZeroMQ connection for this login attempt
    authenticate(username, password)
    check_for_response()  # Start polling for response

# Create the main window
root = tk.Tk()
root.title('Login Form')
root.configure(bg='#FFFFFF')

width, height = 480, 240
center_window(root, width, height)

# Window Header
windowHeader = tk.Label(root, text='Login Here', bg='#FFFFFF', font='Arial 20 bold')
windowHeader.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

# Username label and entry
labelUsername = tk.Label(root, text='Username:', bg='#FFFFFF', font='Arial 12')
labelUsername.grid(row=1, column=0, padx=10, pady=10)
entryUsername = tk.Entry(root, bg='#FFFFFF', font='Arial 12')
entryUsername.grid(row=1, column=1, padx=10, pady=10)

# Password label and entry
labelPassword = tk.Label(root, text='Password:', bg='#FFFFFF', font='Arial 12')
labelPassword.grid(row=2, column=0, padx=10, pady=10)
entryPassword = tk.Entry(root, show='*', bg='#FFFFFF', font='Arial 12')
entryPassword.grid(row=2, column=1, padx=10, pady=10)

# Login button
buttonLogin = tk.Button(root, text='Login', command=login, bg='#FFFFFF', font='Arial 12')
buttonLogin.grid(row=3, column=0, columnspan=2, pady=10)

# Run the main event loop
root.mainloop()