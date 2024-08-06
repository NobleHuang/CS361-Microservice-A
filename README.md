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
```

#### Login
**Example Call:**
```cmd
>>> python Signup-ZeroMQ.py
Enter username: test
Enter password: 1234
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
