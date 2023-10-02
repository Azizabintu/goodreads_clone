from django.contrib.auth import get_user
from django.urls import reverse
from users.models import CustomUser
from django.test import TestCase


# Create your tests here.
class RegisterTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username':'mustafa',
                'first_name':'Uktam',
                'last_name':'Babajanov',
                'email':'babajanov@mail.ru',
                'password':'123'
            }
        )

        user=CustomUser.objects.get(username='mustafa')
        self.assertEqual(user.first_name,'Uktam')
        self.assertEqual(user.last_name,'Babajanov')
        self.assertEqual(user.email,'babajanov@mail.ru')
        self.assertNotEqual(user.password,'123')
        self.assertTrue(user.check_password('123'))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'first_name': 'Uktam1',
                'last_name': 'Babajanov1',
                'email': 'babajanov1@mail.ru',
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count,0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'mustafa',
                'first_name': 'Uktam',
                'last_name': 'Babajanov',
                'email': 'babajanov',
                'password': '123'
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username': 'mustafa',
                'first_name': 'Uktam',
                'last_name': 'Babajanov',
                'email': 'babajanov@mail.ru',
                'password': '123'
            }
        )

        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'mustafa',
                'first_name': 'Uktam2',
                'last_name': 'Babajanov2',
                'email': 'babajanov2',
                'password': '1232'
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, "form", "username", "A user with that username already exists.")

class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username='aziza')
        self.db_user.set_password('12345')
        self.db_user.save()

    def test_login_success(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username":'aziza',
                'password':'12345'

            }
        )
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username":'wrong_username',
                'password':'12345'

            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data={
                "username": 'aziza',
                'password': 'wrong_password'

            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login()
        self.client.get(reverse('users:logout'))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.url,'/users/login/'+'?next=/users/profile/')
        self.assertEqual(response.status_code, 302)


    def test_profile_detail(self):
        db_user = CustomUser.objects.create(
            username='aziza',first_name='Aziza',last_name='Babashova',
            email='aziza.babashova@mail.ru')
        db_user.set_password('12345')
        db_user.save()

        self.client.login(username='aziza',password='12345')


        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, db_user.username)
        self.assertContains(response, db_user.first_name)
        self.assertContains(response, db_user.last_name)
        self.assertContains(response, db_user.email)

    def test_profile_update(self):
        db_user = CustomUser.objects.create(
            username='aziza',first_name='Aziza',last_name='Babashova',
            email='aziza.babashova@mail.ru')
        db_user.set_password('12345')
        db_user.save()

        self.client.login(username='aziza',password='12345')

        response = self.client.post(
            reverse("users:profile_edit"),
            data={
                "username": 'aziza1',
                "first_name": 'Azizaaaaa',
                "last_name":"Babashova",
                'email': 'aziza1.babashova@mail.ru'
            }

        )

        user=CustomUser.objects.get(pk=db_user.pk)
        #db_user.refresh_from_db()

        self.assertEqual(user.username,'aziza1')
        self.assertEqual(user.first_name,'Azizaaaaa')
        self.assertEqual(user.email,'aziza1.babashova@mail.ru')
        self.assertEqual(response.url,reverse("users:profile"))