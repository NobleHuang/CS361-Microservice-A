import zmq
import hashlib
import pwinput
import json
from io import StringIO

user_data = StringIO()

def store_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user_data.write(json.dumps({'username': username, 'password': hashed_password}) + '\n')
    user_data.seek(0)

def send_file(filename, chunk_size=1024*1024):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind('tcp://*:5555')

    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            socket.send(chunk)

    socket.send(b'END')
    socket.close()
    context.term()
    
def signup(username, password):
    try:
        store_user(username, password)

        with open('users.txt', 'w') as f:
            f.write(user_data.getvalue())
        
        print('Signup successful!')
        send_file('users.txt')
        
    except:
        print('Signup Failed!')

if __name__ == '__main__':
    username = input('Enter new username: ')
    password = pwinput.pwinput(prompt='Enter new password: ')
    signup(username, password)
