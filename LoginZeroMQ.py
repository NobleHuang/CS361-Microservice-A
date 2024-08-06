import zmq
import hashlib
import pwinput
import json
from io import StringIO

user_data = StringIO()

def load_users(filename):
    with open(filename, 'r') as file:
        user_data.write(file.read())
    user_data.seek(0)

def check_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    for line in user_data:
        user = json.loads(line)
        if user['username'] == username and user['password'] == hashed_password:
            return True
    return False

def receive_file(filename):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect('tcp://localhost:5555')

    with open(filename, 'wb') as file:
        while True:
            chunk = socket.recv()
            if chunk == b'END':
                break
            file.write(chunk)

    socket.close()
    context.term()
    
def login(username, password):
    receive_file('users.txt')
    load_users('users.txt')

    username = input('Enter username: ')
    password = pwinput.pwinput(prompt='Enter password: ')

    if check_user(username, password):
        print('Login successful!')
    else:
        print('Login failed!')

if __name__ == '__main__':
    username = input('Enter new username: ')
    password = pwinput.pwinput(prompt='Enter new password: ')
    login(username, password)
