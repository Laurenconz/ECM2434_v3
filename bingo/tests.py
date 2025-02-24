import os
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from .models import Task, UserTask, Leaderboard
from bingo.models import BingoTask
from .views import email_validation

User = get_user_model()

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user for login and profile tests.
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@exeter.ac.uk"
        )
        # Create a leaderboard entry for the user.
        self.leaderboard = Leaderboard.objects.create(user=self.user, points=0)
        # Create a sample task for complete_task tests.
        self.task = Task.objects.create(
            id=99,
            description="Test Task",
            points=10,
            requiresUpload=False,
            requireScan=False
        )

    # ---------- Helper Function Tests ----------
    def test_email_validation_valid(self):
        self.assertTrue(email_validation("user@exeter.ac.uk"))

    def test_email_validation_invalid_domain(self):
        self.assertFalse(email_validation("user@gmail.com"))
        self.assertFalse(email_validation("user@hotmail.com"))
        self.assertFalse(email_validation("user@outlook.com"))

    def test_email_validation_invalid_format(self):
        invalid_emails = [
            "userexeter.ac.uk",  # missing '@'
            "user@@exeter.ac.uk",  # double '@'
            "user@exeter",  # missing domain extension
            "user@exeter..ac.uk",  # double dots in domain
            "user@.ac.uk",  # missing domain name before dot
            "user@exetercom",  # missing dot in domain extension
            " user@exeter.ac.uk",  # leading whitespace
            "user@exeter.ac.uk ",  # trailing whitespace
            "user @exeter.ac.uk",  # space in local part
            ""  # empty string
        ]
        for email in invalid_emails:
            self.assertFalse(email_validation(email), f"Email '{email}' should be invalid")

    # ---------- Home Page Test ----------
    def test_home_page(self):
        # The home page is defined at the root URL.
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ---------- Login Tests ----------
    def test_login_user_missing_fields(self):
        response = self.client.post('/api/login/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_login_missing_profile(self):
        # Missing profile should result in an invalid profile error.
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_login_invalid_profile(self):
        data = {"username": "testuser", "password": "testpassword", "profile": "InvalidProfile"}
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_login_nonexistent_user(self):
        data = {"username": "nonexistent", "password": "anything", "profile": "Player"}
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    def test_login_user_incorrect_password(self):
        data = {"username": "testuser", "password": "wrongpassword", "profile": "Player"}
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    def test_login_user_success(self):
        data = {"username": "testuser", "password": "testpassword", "profile": "Player"}
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data.get("user"), "testuser")

    def test_login_game_keeper_wrong_extra_password(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
            "profile": "Game Keeper",
            "extraPassword": "wrong"
        }
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_login_developer_wrong_extra_password(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
            "profile": "Developer",
            "extraPassword": "wrong"
        }
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_login_game_keeper_success(self):
        gk_password = os.environ.get('GK_PASSWORD', 'GKFeb2025BINGO#')
        data = {
            "username": "testuser",
            "password": "testpassword",
            "profile": "Game Keeper",
            "extraPassword": gk_password
        }
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_developer_success(self):
        dv_password = os.environ.get('DV_PASSWORD', 'DVFeb2025BINGO@')
        data = {
            "username": "testuser",
            "password": "testpassword",
            "profile": "Developer",
            "extraPassword": dv_password
        }
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    # ---------- Registration Tests ----------
    def test_register_user_missing_fields(self):
        data = {"username": "", "password": "", "email": ""}
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_register_user_invalid_email(self):
        data = {
            "username": "newuser",
            "password": "StrongPassw0rd!",
            "passwordagain": "StrongPassw0rd!",
            "email": "newuser@gmail.com"
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_register_user_passwords_mismatch(self):
        data = {
            "username": "newuser",
            "password": "StrongPassw0rd!",
            "passwordagain": "DifferentPass!",
            "email": "newuser@exeter.ac.uk"
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_register_user_existing_username(self):
        data = {
            "username": "testuser",  # already exists
            "password": "StrongPassw0rd!",
            "passwordagain": "StrongPassw0rd!",
            "email": "another@exeter.ac.uk"
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_register_user_existing_email(self):
        data = {
            "username": "anotheruser",
            "password": "StrongPassw0rd!",
            "passwordagain": "StrongPassw0rd!",
            "email": "test@exeter.ac.uk"  # already used
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_register_user_weak_password(self):
        data = {
            "username": "weakpassuser",
            "password": "123",  # intentionally weak password
            "passwordagain": "123",
            "email": "weakpassuser@exeter.ac.uk"
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_register_user_missing_password_again(self):
        data = {
            "username": "missingpassagain",
            "password": "StrongPassw0rd!",
            "email": "missingpassagain@exeter.ac.uk"
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_register_user_success(self):
        data = {
            "username": "newuser",
            "password": "StrongPassw0rd!",
            "passwordagain": "StrongPassw0rd!",
            "email": "newuser@exeter.ac.uk"
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data.get("message"), "User registered successfully!")

    # ---------- Tasks Tests ----------
    def test_tasks(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)
