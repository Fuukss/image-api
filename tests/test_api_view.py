from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APITestCase
from io import BytesIO
from PIL import Image
from django.core.files.base import File
from account.models import Account
from plan.model import Plan


class TestApiCreateImageView(APITestCase):

    @staticmethod
    def get_image_file(name, size, ext='png', color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

        self.plan_basic = Plan.objects.create(plan_name='Basic')
        self.plan_premium = Plan.objects.create(plan_name='Premium')
        self.plan_enterprise = Plan.objects.create(plan_name='Enterprise')
        self.plan_other = Plan.objects.create(plan_name='Other', thumbnail_width=50, thumbnail_height=50)
        self.plan_other_original_file = Plan.objects.create(plan_name='OtherOriginal', thumbnail_width=50,
                                                            thumbnail_height=50, original_file=1)

        self.user_basic = Account.objects.create(username='basicname', email='basicemail@gmail.com',
                                                 password='Password1!',
                                                 account_tier=self.plan_basic)
        self.user_premium = Account.objects.create(username='premiumname', email='premiumemail@gmail.com',
                                                   password='Password1!',
                                                   account_tier=self.plan_premium)
        self.user_enterprise = Account.objects.create(username='enterprisename', email='enterpriseemail@gmail.com',
                                                      password='Password1!',
                                                      account_tier=self.plan_enterprise)
        self.user_other = Account.objects.create(username='othername', email='otheremail@gmail.com',
                                                 password='Password1!',
                                                 account_tier=self.plan_other)
        self.user_other_original = Account.objects.create(username='otheroriginalname',
                                                          email='otheroriginalemail@gmail.com',
                                                          password='Password1!',
                                                          account_tier=self.plan_other_original_file)
        self.user_basic.save()
        self.user_premium.save()
        self.user_enterprise.save()
        self.user_other.save()
        self.user_other_original.save()
        self.image = self.get_image_file(name='test.jpg', size=(50, 50))

    def test_api_create_image_unauthorization(self):
        response = self.client.post('/api/image/create')
        self.assertEqual(response.status_code, 401)

    def test_api_create_image_basic_account(self):
        token = Token.objects.get(user__username='basicname')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = self.image
        response = client.post('/api/image/create', {"image": data, "slug": ''}, format='multipart')
        assert response.status_code == 201

    def test_api_create_image_premium_account(self):
        token = Token.objects.get(user__username='premiumname')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = self.image
        response = client.post('/api/image/create', {"image": data, "slug": ''}, format='multipart')
        assert response.status_code == 201

    def test_api_create_image_enterprise_account(self):
        token = Token.objects.get(user__username='enterprisename')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = self.image
        response = client.post('/api/image/create', {"image": data, "slug": ''}, format='multipart')
        assert response.status_code == 201

    def test_api_create_image_other_account(self):
        token = Token.objects.get(user__username='othername')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = self.image
        response = client.post('/api/image/create', {"image": data, "slug": ''}, format='multipart')
        assert response.status_code == 201

    def test_api_create_image_other_original_link_account(self):
        token = Token.objects.get(user__username='otheroriginalname')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = self.image
        response = client.post('/api/image/create', {"image": data, "slug": ''}, format='multipart')
        assert response.status_code == 201

    def test_api_create_image_serializer_error(self):
        token = Token.objects.get(user__username='basicname')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = self.image
        response = client.post('/api/image/create', {"image": data}, format='multipart')
        print(response)
        assert response.status_code == 400

    def test_api_image_list_view(self):
        token = Token.objects.get(user__username='basicname')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('/api/image/list', format='multipart')
        assert response.status_code == 200

