from rest_framework.test import APITestCase
from account.models import Account


class TestAccountModel(APITestCase):
    def test_creates_user(self):
        user = Account.objects.create_user(email='rafal19fuchs@gmail.com', username='rafalfuchs',
                                           password='Password1!')
        self.assertIsInstance(user, Account)
        self.assertEqual(user.email, 'rafal19fuchs@gmail.com')

    def test_raises_error_when_no_email_is_supplied(self):
        self.assertRaises(ValueError, Account.objects.create_user, email='', username='rafalfuchs',
                          password='Password1!')

    def test_raises_error_with_message_when_no_email_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given email must be set"):
            Account.objects.create_user(email='', username='rafalfuchs',
                                        password='Password1!')

    def test_raises_error_when_no_username_is_supplied(self):
        self.assertRaises(ValueError, Account.objects.create_user, email='rafalfuchs', username='',
                          password='Password1!')

    def test_raises_error_with_message_when_no_username_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given username must be set"):
            Account.objects.create_user(email='rafal19fuchs@gmail.com', username='',
                                        password='Password1!')

    def test_creates_super_user(self):
        user = Account.objects.create_superuser(email='rafal19fuchs@gmail.com', username='rafalfuchs',
                                                password='Password1!')

        self.assertIsInstance(user, Account)
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        user.delete()

    def test_create_user_str(self):
        user = Account.objects.create_superuser(email='rafal19fuchs@gmail.com', username='rafalfuchs',
                                                password='Password1!')
        self.assertEqual(user.__str__(), str(user.email + ", " + user.username))
        user.delete()

    def test_create_user_admin_has_perm(self):
        user = Account.objects.create_superuser(email='rafal19fuchs@gmail.com', username='rafalfuchs',
                                                password='Password1!')
        self.assertEqual(user.has_perm(perm='admin'), user.is_admin)
        user.delete()

    def test_create_user_perms_check(self):
        user = Account.objects.create_superuser(email='rafal19fuchs@gmail.com', username='rafalfuchs',
                                                password='Password1!')
        self.assertEqual(user.has_module_perms(app_label='app'), True)
        user.delete()
