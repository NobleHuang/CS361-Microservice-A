# User Authentication Microservice
This microservice comprises everything about User Authentication Microservice equipped with ZeroMQ for communication between components. The microservice enables user signup and login activities.

## Communication Contract

### Requesting Data
To request data from the microservice, you are required to use the `Signup` and `Login` components using ZeroMQ. Below are the steps and example calls.

#### Signup
**Example Call:**
```cmd
>>> python Signup-ZeroMQ.py
Enter new username: test
Enter new password: 1234
Signup successful!
```

#### Login
**Example Call:**
```cmd
>>> python Signup-ZeroMQ.py
Enter username: test
Enter password: 1234
Login successful!
```

#### Receiving Data
To receive data from the microservice, the Signup and Login components will send responses back to the client. The responses will contain the status and message.

#### Signup
**Example Response:**
```
Signup successful!
```

#### Login
**Example Response:**
```
Login successful!
```

## UML Sequence Diagrams
![CS 361 Microservice A](https://raw.githubusercontent.com/NobleHuang/CS361-Microservice-A/main/UML-seq-diagram.jpg)

## Files
Signup-ZeroMQ.py: Handles user signup.
Login-ZeroMQ.py: Handles user login.

### Signup-ZeroMQ.py
```python
import zmq
import hashlib
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

if __name__ == '__main__':
    try:
        username = input('Enter new username: ')
        password = input('Enter new password: ')
        store_user(username, password)

        with open('users.txt', 'w') as f:
            f.write(user_data.getvalue())
        
        print('Signup successful!')
        send_file('users.txt')
        
    except:
        print('Signup Failed!')
```

### Login-ZeroMQ.py
```python
import zmq
import hashlib
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
    socket.connect('tcp://*:5555')

    with open(filename, 'wb') as file:
        while True:
            chunk = socket.recv()
            if chunk == b'END':
                break
            file.write(chunk)

    socket.close()
    context.term()

if __name__ == '__main__':
    receive_file('users.txt')
    load_users('users.txt')

    username = input('Enter username: ')
    password = input('Enter password: ')

    if check_user(username, password):
        print('Login successful!')
    else:
        print('Login failed!')
```

