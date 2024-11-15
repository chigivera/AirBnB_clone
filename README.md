# AirBnB Clone Project

## Description
This project is a simplified clone of AirBnB that implements a command-line interface for managing AirBnB objects. It's the first step towards building a full web application.

## Command Interpreter
The command interpreter provides a command-line interface to interact with the object storage system.

### How to Start
```bash
./console.py
```

### How to Use
The command interpreter supports the following commands:
* create: Creates a new instance of a class
* show: Shows the string representation of an instance
* destroy: Deletes an instance
* all: Shows all instances or all instances of a specific class
* update: Updates an instance's attributes

### Examples
```
(hbnb) create BaseModel
49faff9a-6318-451f-87b6-910505c55907
(hbnb) show BaseModel 49faff9a-6318-451f-87b6-910505c55907
[BaseModel] (49faff9a-6318-451f-87b6-910505c55907) {'id': '49faff9a-6318-451f-87b6-910505c55907', 'created_at': datetime.datetime(2023, 7, 14, 3, 10, 25, 903293), 'updated_at': datetime.datetime(2023, 7, 14, 3, 10, 25, 903300)}
(hbnb) update BaseModel 49faff9a-6318-451f-87b6-910505c55907 name "My First Model"
(hbnb) show BaseModel 49faff9a-6318-451f-87b6-910505c55907
[BaseModel] (49faff9a-6318-451f-87b6-910505c55907) {'id': '49faff9a-6318-451f-87b6-910505c55907', 'created_at': datetime.datetime(2023, 7, 14, 3, 10, 25, 903293), 'updated_at': datetime.datetime(2023, 7, 14, 3, 10, 25, 903300), 'name': 'My First Model'}