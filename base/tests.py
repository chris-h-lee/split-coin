from django.test import TestCase
from .models import Create, Profile
from datetime import date
from django.contrib.auth.models import User

# Create your tests here.

# Tests based off tutorials from https://docs.djangoproject.com/en/3.1/topics/testing/overview/
# Test cases for creating "Create" model

class CreateTestCase(TestCase):
    def setUp(self):
        Create.objects.create(Description="Hi", Name="User", Event="Volunteer")

    def test_created_successfully(self):
        self.assertEqual("Hi", str(Create.objects.get(Name="User")))

    def test_name_matches(self):
        self.assertEqual("User", Create.objects.get(Name="User").get_author())

    def test_event_matches(self):
        self.assertEqual("Volunteer", Create.objects.get(Name="User").get_type())


class CreateTestCase2(TestCase):
    def setUp(self):
        Create.objects.create(Description="Hi")
        Create.objects.create(Description="Bye")

    def test_num_queries(self):
        with self.assertNumQueries(2):
            Create.objects.create(Description="Donate")
            Create.objects.create(Description="Volunteer")


class CreateTestCase3(TestCase):
    def setUp(self):
        Create.objects.create(Event="Volunteer")

    def test_volunteer_filter(self):
        self.assertEqual("Volunteer", Create.objects.all().filter(Event="Volunteer").get(pk=1).get_type())


class CreateTestCase4(TestCase):
    def setUp(self):
        Create.objects.create(Event="Donation")

    def test_donation_filter(self):
        self.assertEqual("Donation", Create.objects.all().filter(Event="Donation").get(pk=1).get_type())


class CreateTestCase5(TestCase):
    def setUp(self):
        Create.objects.create(Date=date.today(), Event="Volunteer")

    def test_check_date(self):
        self.assertEqual("Volunteer",Create.objects.all().filter(Event='Volunteer').filter(Date__gte=date.today()).get(pk=1).get_type())


# Test cases for testing HTML pages

class URLTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('username', 'test@gmail.com', 'pass')
        user.profile.is_volunteer = False
        user.profile.first_login = False
        self.client.login(username='username', password='pass')

        thing = Create.objects.create(Description="Hi", xp=10)

    def test_initial(self):
        response = self.client.get('/home/', follow=True)
        user = User.objects.get(username='username')
        self.assertEqual(response.context['user'].email, 'test@gmail.com')

    def test_my_thing(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_my_thing2(self):
        response = self.client.get('/volunteer/')
        self.assertEqual(response.status_code, 200)

    def test_my_thing3(self):
        response = self.client.get('/donate/')
        self.assertEqual(response.status_code, 200)

    def test_my_thing4(self):
        response = self.client.get('/home/create', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_my_thing5(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_my_thing6(self):
        response = self.client.get('/home/1/')
        self.assertEqual(response.status_code, 200)

    def test_my_thing7(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_my_thing8(self):
        response = self.client.get('/schedule/')
        self.assertEqual(response.status_code, 200)

    def test_my_thing9(self):
        response = self.client.get('/submitted-events', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_my_thing10(self):
        response = self.client.get('/profile/edit')
        self.assertEqual(response.status_code, 200)

    def test_my_thing11(self):
        response = self.client.get('/leaderboard/')
        self.assertEqual(response.status_code, 200)

    def test_functionality(self):
        user = User.objects.get(username='username')
        thing = Create.objects.get(Description='Hi')
        thing.signup_list.add(user)
        self.assertEqual(thing.signup_list.get(pk=1), user)