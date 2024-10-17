import unittest
from unittest.mock import Mock
from tkinter import Tk
from PIL import Image
from lab_1 import App

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize shared objects once for all tests
        cls.root = Tk()  # Store Tk instance as class variable
        cls.app = App(cls.root)  # Store the app instance as class variable
        cls.app.build_Window()  # Build the app window once
        cls.app.get_image()

    def test_01_initialization(self):
        self.assertIsNotNone(self.app.root)
        self.assertIsNotNone(self.app.extracted_image)
        self.assertIsNotNone(self.app.modified_image)

    def test_02_get_image(self):        
        self.assertIsNotNone(self.app.extracted_image)
        self.assertEqual(self.app.remove_pic_button['state'], "normal")
        
    def test_03_invert_image_colors(self):
        self.app.placeholder_image = Image.new("RGBA", (100, 100), color="white")
        self.app.tkinter_image = None
        self.app.photo_holder = Mock()

        self.app.invert_image_colors()

        self.assertIsNotNone(self.app.tkinter_image)
        self.app.photo_holder.config.assert_called_once_with(image=self.app.tkinter_image)

    def test_04_remove_image(self):
        self.app.extracted_image = Image.new("RGBA", (100, 100), color="white")
        self.app.remove_image()

        self.assertIsNone(self.app.extracted_image)
        self.assertIsNone(self.app.modified_image)
        self.assertIsNone(self.app.tkinter_image)

if __name__ == "__main__":
    unittest.main()

