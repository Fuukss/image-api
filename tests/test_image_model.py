from rest_framework.test import APITestCase
from io import StringIO
from PIL import Image
from django.core.files.base import File
from image.models import ImagePost
from account.models import Account
import shutil
from django.test import override_settings
import os

TEST_DIR = 'test_data'


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class TestAccountModel(APITestCase):

    @staticmethod
    def get_image_file(name='test.jpg', ext='img', size=(50, 50), color=(256, 0, 0)):
        file_obj = StringIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(name)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def test_create_image_str(self):
        user = Account.objects.create_user(email='rafal19fuchs@gmail.com', username='rafalfuchs',
                                           password='Password1!')

        image = ImagePost.objects.create(image=self.get_image_file(), author=user, slug='')
        self.assertEqual(image.__str__(), str(image))
        image.delete()


def tearDownModule():
    print("\nDeleting temporary files...\n")
    try:
        shutil.rmtree(TEST_DIR)
        os.remove('test.jpg')
    except OSError:
        pass
