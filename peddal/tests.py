from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.
User = get_user_model()

class UserTestCase():

    def setUp(self):
        user_a = User(username='cfe', email='rojesh76@gmail.com')
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.set_password('Rojesh9849#')
        user_a.save()
        print(user_a.id)

    def test_user_exist(self):
        user_count = User.object.all().count()
        self.assertEqual(user_count,1)  #user_count == 1
        self.assertNotEqual(user_count,0) #user_count != 0