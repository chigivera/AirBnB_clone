#!/usr/bin/python3
"""Unit tests for console.py"""
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestHBNBCommand(unittest.TestCase):
    """Test cases for HBNBCommand class"""

    def setUp(self):
        """Set up test cases"""
        self.console = HBNBCommand()
        self.classes = {
            'BaseModel': BaseModel,
            'User': User,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Place': Place,
            'Review': Review
        }

    def test_quit(self):
        """Test quit command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("quit"))

    def test_EOF(self):
        """Test EOF command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("EOF"))

    def test_help(self):
        """Test help command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("help")
            output = f.getvalue()
            self.assertIn("Documented commands", output)

    def test_create(self):
        """Test create command"""
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(f"create {class_name}")
                output = f.getvalue().strip()
                self.assertTrue(len(output) > 0)
                # Verify the instance was created
                key = f"{class_name}.{output}"
                self.assertIn(key, storage.all())

    def test_create_missing_class(self):
        """Test create command with missing class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual("** class name missing **", f.getvalue().strip())

    def test_create_invalid_class(self):
        """Test create command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create MyModel")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_show(self):
        """Test show command"""
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                # First create an instance
                self.console.onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()
                
                # Then try to show it
                with patch('sys.stdout', new=StringIO()) as f2:
                    self.console.onecmd(f"show {class_name} {obj_id}")
                    output = f2.getvalue().strip()
                    self.assertIn(obj_id, output)
                    self.assertIn(class_name, output)

    def test_show_missing_class(self):
        """Test show command with missing class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show")
            self.assertEqual("** class name missing **", f.getvalue().strip())

    def test_show_invalid_class(self):
        """Test show command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show MyModel")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_show_missing_id(self):
        """Test show command with missing id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel")
            self.assertEqual("** instance id missing **", f.getvalue().strip())

    def test_destroy(self):
        """Test destroy command"""
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                # First create an instance
                self.console.onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()
                key = f"{class_name}.{obj_id}"
                
                # Verify it exists
                self.assertIn(key, storage.all())
                
                # Then destroy it
                self.console.onecmd(f"destroy {class_name} {obj_id}")
                
                # Verify it was destroyed
                self.assertNotIn(key, storage.all())

    def test_all(self):
        """Test all command"""
        # Test all with no class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all")
            output = f.getvalue().strip()
            self.assertIsInstance(eval(output), list)

        # Test all with valid class name
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(f"all {class_name}")
                output = f.getvalue().strip()
                self.assertIsInstance(eval(output), list)

    def test_all_invalid_class(self):
        """Test all command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all MyModel")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_update(self):
        """Test update command"""
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                # First create an instance
                self.console.onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()
                
                # Then update it
                self.console.onecmd(f'update {class_name} {obj_id} name "test_name"')
                
                # Verify the update
                key = f"{class_name}.{obj_id}"
                obj = storage.all()[key]
                self.assertEqual(obj.name, "test_name")

    def test_update_missing_class(self):
        """Test update command with missing class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update")
            self.assertEqual("** class name missing **", f.getvalue().strip())

    def test_update_invalid_class(self):
        """Test update command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update MyModel")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_update_missing_id(self):
        """Test update command with missing id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update BaseModel")
            self.assertEqual("** instance id missing **", f.getvalue().strip())

    def test_class_all(self):
        """Test <class name>.all() command"""
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(f"{class_name}.all()")
                output = f.getvalue().strip()
                self.assertIsInstance(eval(output), list)

    def test_class_count(self):
        """Test <class name>.count() command"""
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(f"{class_name}.count()")
                output = f.getvalue().strip()
                self.assertIsInstance(int(output), int)

    def test_class_show(self):
        """Test <class name>.show() command"""
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                # First create an instance
                self.console.onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()
                
                # Then try to show it using class method
                with patch('sys.stdout', new=StringIO()) as f2:
                    self.console.onecmd(f'{class_name}.show("{obj_id}")')
                    output = f2.getvalue().strip()
                    self.assertIn(obj_id, output)
                    self.assertIn(class_name, output)

    def test_class_destroy(self):
        """Test <class name>.destroy() command"""
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                # First create an instance
                self.console.onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()
                key = f"{class_name}.{obj_id}"
                
                # Verify it exists
                self.assertIn(key, storage.all())
                
                # Then destroy it using class method
                self.console.onecmd(f'{class_name}.destroy("{obj_id}")')
                
                # Verify it was destroyed
                self.assertNotIn(key, storage.all())

    def test_class_update(self):
        """Test <class name>.update() command"""
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                # First create an instance
                self.console.onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()
                
                # Then update it using class method
                self.console.onecmd(f'{class_name}.update("{obj_id}", "name", "test_name")')
                
                # Verify the update
                key = f"{class_name}.{obj_id}"
                obj = storage.all()[key]
                self.assertEqual(obj.name, "test_name")

    def test_class_update_dict(self):
        """Test <class name>.update() command with dictionary"""
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                # First create an instance
                self.console.onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()
                
                # Then update it using class method with dictionary
                self.console.onecmd(f'{class_name}.update("{obj_id}", {{"name": "test_name", "value": 42}})')
                
                # Verify the update
                key = f"{class_name}.{obj_id}"
                obj = storage.all()[key]
                self.assertEqual(obj.name, "test_name")
                self.assertEqual(obj.value, 42)


if __name__ == '__main__':
    unittest.main()