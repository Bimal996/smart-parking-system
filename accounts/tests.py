from django.contrib.auth.models import User
from django.test import TestCase

from .models import UserProfile


class SignupTests(TestCase):
	def setUp(self):
		self.signup_url = "/accounts/signup/"
		self.valid_data = {
			"username": "bimal_test",
			"first_name": "Bimal",
			"last_name": "Test",
			"email": "bimal_test@example.com",
			"phone_number": "9800000000",
			"password1": "StrongPass123!",
			"password2": "StrongPass123!",
		}

	def test_signup_creates_user_and_profile(self):
		response = self.client.post(self.signup_url, self.valid_data)

		self.assertRedirects(response, "/")
		user = User.objects.get(username="bimal_test")
		self.assertTrue(user.check_password("StrongPass123!"))
		self.assertEqual(user.email, "bimal_test@example.com")
		self.assertEqual(user.profile.phone_number, "9800000000")

	def test_duplicate_email_is_rejected(self):
		User.objects.create_user(username="existing", email=self.valid_data["email"])

		response = self.client.post(self.signup_url, self.valid_data)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "An account with this email already exists.")
		self.assertEqual(User.objects.filter(username="bimal_test").count(), 0)

	def test_password_errors_are_visible(self):
		data = {**self.valid_data, "password2": "DifferentPass123!"}

		response = self.client.post(self.signup_url, data)

		self.assertEqual(response.status_code, 200)
		self.assertIn("password2", response.context["form"].errors)
		self.assertTrue(response.context["form"].errors["password2"])
		self.assertEqual(User.objects.filter(username="bimal_test").count(), 0)

# Create your tests here.
