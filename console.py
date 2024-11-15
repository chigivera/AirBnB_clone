#!/usr/bin/python3
"""Command interpreter for the HBNB project"""
import cmd
import shlex
import re
import ast
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""
    prompt = '(hbnb) '
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def default(self, line):
        """Handle class specific commands"""
        match = re.search(r'(\w+)\.(\w+)\((.*?)\)', line)
        if not match:
            return super().default(line)
        
        classname, method, args = match.groups()
        if classname not in self.classes:
            print("** class doesn't exist **")
            return

        # Parse arguments
        args_list = []
        if args:
            # Check if argument is a dictionary
            if args.startswith('{') and args.endswith('}'):
                try:
                    args_dict = ast.literal_eval(args)
                    if isinstance(args_dict, dict):
                        instance_id = args_dict.pop('id', None)
                        if instance_id:
                            for key, value in args_dict.items():
                                self.do_update(f"{classname} {instance_id} {key} {value}")
                        return
                except (ValueError, SyntaxError):
                    pass
            
            # Regular argument parsing
            args_list = [arg.strip('"') for arg in shlex.split(args)]

        # Handle different methods
        if method == 'all':
            self.do_all(classname)
        elif method == 'count':
            count = sum(1 for key in storage.all() if key.startswith(f"{classname}."))
            print(count)
        elif method == 'show':
            if not args_list:
                print("** instance id missing **")
                return
            self.do_show(f"{classname} {args_list[0]}")
        elif method == 'destroy':
            if not args_list:
                print("** instance id missing **")
                return
            self.do_destroy(f"{classname} {args_list[0]}")
        elif method == 'update':
            if len(args_list) < 1:
                print("** instance id missing **")
            elif len(args_list) < 2:
                print("** attribute name missing **")
            elif len(args_list) < 3:
                print("** value missing **")
            else:
                self.do_update(f"{classname} {' '.join(args_list)}")

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty line"""
        pass

    def do_create(self, arg):
        """Creates a new instance of a class"""
        if not arg:
            print("** class name missing **")
            return
        try:
            new_instance = self.classes[arg]()
            new_instance.save()
            print(new_instance.id)
        except KeyError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints string representation of an instance"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Prints string representation of all instances"""
        args = shlex.split(arg)
        obj_list = []
        if not arg:
            for obj in storage.all().values():
                obj_list.append(str(obj))
        elif args[0] in self.classes:
            for key, obj in storage.all().items():
                if key.split('.')[0] == args[0]:
                    obj_list.append(str(obj))
        else:
            print("** class doesn't exist **")
            return
        print(obj_list)

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        obj = storage.all()[key]
        try:
            value = eval(args[3])
        except (NameError, SyntaxError):
            value = args[3]
        setattr(obj, args[2], value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()