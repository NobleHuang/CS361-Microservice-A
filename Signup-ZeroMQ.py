# Make it high-res, even in Windows 10 or above
#from ctypes import windll as ctypes_windll
#ctypes_windll.shcore.SetProcessDpiAwareness(1)

import tkinter as tk
from tkinter import messagebox
import hashlib
import zmq
import os

# Function to center the window both vertically and horizontally
def center_window(window, width, height):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the position of the window to center it on the screen
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the geometry of the window to center it on the screen
    window.geometry(f'{width}x{height}+{x}+{y}')
    
# Function to hash a password using SHA-512
def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()

# Function to save the new user data
def save_user_data(username, password):
    hashed_password = hash_password(password)
    file_path = os.path.join(os.getenv('LOCALAPPDATA'), 'LoginApp', 'UserData.txt')
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    try:
        with open(file_path, 'a') as file:
            file.write(f'{username.lower()},{hashed_password}\n')
        return True
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')
        return False

context = None
socket = None

def setup_zmq():
    global context, socket
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.connect('tcp://localhost:5555')  # Connect to the ZeroMQ server

def send_user_data(username, password):
    global socket
    hashed_password = hash_password(password)
    data = f'{username.lower()},{hashed_password}'
    socket.send_string(data)
    print(f"Signup Data: {data}")
    print('User data sent successfully')
    return True

def signup():
    username = entry_username.get()
    password = entry_password.get()
    
    if username and password:
        setup_zmq()  # Ensure the ZeroMQ connection is set up
        if send_user_data(username, password):
            messagebox.showinfo('Signup Info', 'Signup successful!')
        else:
            messagebox.showerror('Signup Info', 'Signup failed.')
    else:
        messagebox.showwarning('Signup Info', 'Username and password cannot be empty.')

# Create the main window
root = tk.Tk()
root.title('Signup Form')
root.configure(bg='#FFFFFF')

width, height = 480, 240
center_window(root, width, height)

# Window Header
windowHeader = tk.Label(root, text='Signup Here', bg='#FFFFFF', font='Arial 20 bold')
windowHeader.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

# Username label and entry
label_username = tk.Label(root, text='Username:', bg='#FFFFFF', font='Arial 12')
label_username.grid(row=1, column=0, padx=10, pady=10)
entry_username = tk.Entry(root, bg='#FFFFFF')
entry_username.grid(row=1, column=1, padx=10, pady=10)

# Password label and entry
label_password = tk.Label(root, text='Password:', bg='#FFFFFF', font='Arial 12')
label_password.grid(row=2, column=0, padx=10, pady=10)
entry_password = tk.Entry(root, show='*', bg='#FFFFFF')
entry_password.grid(row=2, column=1, padx=10, pady=10)

# Signup button
button_signup = tk.Button(root, text='Signup', command=signup, bg='#FFFFFF')
button_signup.grid(row=3, column=0, columnspan=2, pady=10)

# Run the main event loop
root.mainloop()
