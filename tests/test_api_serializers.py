import shutil
from django.test import override_settings
import os
from api.serializers import ImageSerializer, ImagePostCreateSerializer
from rest_framework.test import APITestCase
from io import StringIO
from PIL import Image
from django.core.files.base import File
from image.models import ImagePost
from account.models import Account

TEST_DIR = 'test_data'


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class TestImageSerializer(APITestCase):
    @staticmethod
    def get_image_file(name='te?st.jpg', ext='img', size=(50, 50), color=(256, 0, 0)):
        file_obj = StringIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(name)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        self.serializer_data = {
            'username': 'testname',
            'image': 'http://localhost:8000/media/image/testname/test.jpg'
        }
        user = Account.objects.create_user(email='testname@gmail.com', username='testname',
                                           password='Password1!')
        self.image = ImagePost.objects.create(image=self.get_image_file(), author=user)
        self.serializer = ImageSerializer(instance=self.image)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'image', 'username'})

    def test_remove_question_mark_from_url(self):
        data = self.serializer.data
        self.assertFalse("?" in set(data.values()))


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class TestImagePostSerializer(APITestCase):
    @staticmethod
    def get_image_file(name='test.jpg', ext='img', size=(50, 50), color=(256, 0, 0)):
        file_obj = StringIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(name)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        self.serializer_data = {
            'image': '/media/image/testname/test.jpg',
            'slug': 'testname-testjpg',
            'author': 1
        }
        user = Account.objects.create_user(email='testname@gmail.com', username='testname',
                                           password='Password1!')
        self.image = ImagePost.objects.create(image=self.get_image_file(), author=user, slug='')
        self.serializer = ImagePostCreateSerializer(instance=self.image)
        user.delete()

    def test_save_image_post(self):
        data = self.serializer.data
        self.assertQuerysetEqual(set(self.serializer_data.values()), set(data.values()), transform=lambda x: x)


def tearDownModule():
    print("\nDeleting temporary files...\n")
    try:
        shutil.rmtree(TEST_DIR)
        os.remove('te?st.jpg')
    except OSError:
        pass
