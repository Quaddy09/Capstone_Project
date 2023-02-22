from django.test import TestCase, Client
from .models import *
from classes import myUser


class TestMyUser(TestCase):
    monkey = None

    def setUp(self):
        self.monkey = Client()
        u = User(username="test", password="test", email="test")
        u.save()

    def test_get_user(self):
        u = User.objects.get(username="test")
        self.assertEqual(myUser.get_user("test"), u)

    def test_set_username_length(self):
        u = myUser.get_user("test")
        s = ""
        while len(s) < 501:
            s = s + "-"
        with self.assertRaises(Exception, msg="username is too long"):
            myUser.set_username(u, s)

    def test_set_username_null(self):
        u = myUser.get_user("test")
        with self.assertRaises(Exception, msg="username is null"):
            myUser.set_username(u, None)

    def test_set_username(self):
        u = myUser.get_user("test")
        myUser.set_username(u, "new")
        self.assertEqual("new", u.username)

    def test_set_password_length(self):
        u = myUser.get_user("test")
        s = ""
        while len(s) < 501:
            s = s + "-"
        with self.assertRaises(Exception, msg="password is too long"):
            myUser.set_password(u, s)

    def test_set_password_null(self):
        u = myUser.get_user("test")
        with self.assertRaises(Exception, msg="password is null"):
            myUser.set_password(u, None)

    def test_set_password(self):
        u = myUser.get_user("test")
        myUser.set_password(u, "new")
        self.assertEqual("new", u.password)

    def test_set_email_length(self):
        u = myUser.get_user("test")
        s = ""
        while len(s) < 501:
            s = s + "-"
        with self.assertRaises(Exception, msg="email is too long"):
            myUser.set_email(u, s)

    def test_set_email_null(self):
        u = myUser.get_user("test")
        with self.assertRaises(Exception, msg="email is null"):
            myUser.set_email(u, None)

    def test_set_email(self):
        u = myUser.get_user("test")
        myUser.set_email(u, "new")
        self.assertEqual("new", u.email)

    def test_exists(self):
        self.assertTrue(myUser.exists("test"))

    def test_not_exists(self):
        self.assertFalse(myUser.exists("fake"))

    def test_add_user(self):
        myUser.add_user("new", "new", "new")
        self.assertTrue(myUser.exists("new"))

    def test_add_existing(self):
        with self.assertRaises(Exception, msg="user already in database"):
            myUser.add_user("test", "test", "test")

    def test_delete_user(self):
        u = myUser.get_user("test")
        myUser.delete_user(u)
        self.assertFalse(myUser.exists("test"))

    def test_delete_nonexistent_user(self):
        with self.assertRaises(Exception, msg="user not in database"):
            myUser.delete_user("fake")
