from rest_framework.test import APITestCase
from io import BytesIO
from PIL import Image
from django.core.files.base import File
from image.validators import image_size, validate_file_extension
from rest_framework.exceptions import ValidationError
import shutil
from django.test import override_settings
import os

TEST_DIR = 'test_data'


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class TestImageValidatorSize(APITestCase):

    @staticmethod
    def get_image_file(name, size, ext='png', color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def test_image_size(self):
        image = self.get_image_file(size=(50, 50), name='test.png')

        self.assertEqual(image_size(image), image)

    def test_raises_error_when_image_is_too_large(self):
        image = self.get_image_file(size=(20000, 30000), name='test.png')
        self.assertRaises(ValidationError, image_size, image)


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class TestImageValidatorExtension(APITestCase):
    @staticmethod
    def get_image_file(name, size, ext='png', color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def test_image_extension_png(self):
        image = self.get_image_file(size=(50, 50), name='test.png')

        self.assertEqual(validate_file_extension(image), image)

    def test_image_extension_diff(self):
        image = self.get_image_file(size=(50, 50), name='test.jpeg')

        self.assertRaises(ValidationError, validate_file_extension, image)


def tearDownModule():
    print("\nDeleting temporary files...\n")
    try:
        shutil.rmtree(TEST_DIR)
        os.remove('test.jpg')
    except OSError:
        pass
