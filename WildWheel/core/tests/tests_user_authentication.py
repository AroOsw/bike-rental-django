# import re
# from django.contrib.auth.models import User
# from django.core import mail
# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.sites.models import Site
# from allauth.socialaccount.models import SocialApp
# from allauth.account.models import EmailAddress
#
#
# class TestsAuthentication(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         site, created = Site.objects.get_or_create(id=2)
#
#         google_app, created = SocialApp.objects.get_or_create(
#             provider='google',
#             defaults={
#                 'name': 'Google Test App',
#                 'client_id': 'mock-google-client-id-for-tests',
#                 'secret': 'mock-google-secret-for-tests'
#             }
#         )
#         google_app.sites.add(site)
#
#         facebook_app, created = SocialApp.objects.get_or_create(
#             provider='facebook',
#             defaults={
#                 'name': 'Facebook Test App',
#                 'client_id': 'mock-facebook-client-id-for-tests',
#                 'secret': 'mock-facebook-secret-for-tests'
#             }
#         )
#         facebook_app.sites.add(site)
#
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="testuser",
#             email="testemail@example.com",
#             password="TestPass123!"
#         )
#
#         self.email, created = EmailAddress.objects.get_or_create(
#             user=self.user,
#             email=self.user.email,
#             verified=False,
#             primary=True,
#         )
#
#         if not created and self.email.verified:
#             self.email.verified = False
#             self.email.save()
#
#         mail.outbox = []
#
#     def test_if_user_was_created(self):
#         self.assertTrue(self.user)
#
#     def test_login_success(self):
#         response = self.client.post(reverse('account_login'), {
#             'login': 'testemail@example.com',
#             'password': 'TestPass123!',
#         })
#
#         # print(f"Status Code: {response.status_code}")
#         # print(f"Redirect URL: {response.url}")
#         # print(f"Content (first 500 chars): {response.content.decode('utf-8')[:500]}")
#
#         self.assertEqual(response.status_code, 302)
#
#     def test_signup_success(self):
#         response = self.client.post(reverse("account_signup"), {
#             "username": "signupuser",
#             "email": "signupemail@example.com",
#             "password1": "TestPass123!",
#             "password2": "TestPass123!",
#             "terms_of_service": True,
#         }, follow=False)
#
#         self.assertEqual(response.status_code, 302)
#         print(f"Redirect URL: {response.url}")
#         print(f"Content (first 500 chars): {response.content.decode('utf-8')[:500]}")
#         # To pokaże Ci HTML strony, na którą zostałeś przekierowany
#         print(f"Request URL: {response.request['PATH_INFO']}")
#         print(f"nagłówek {response["Location"]}")
#         self.assertRedirects(response, reverse("account_email_verification_sent"))
#         self.assertTrue(EmailAddress.objects.filter(email="signupemail@example.com").exists())
#
#     def test_email_verification_works(self):
#         response = self.client.post(reverse("account_signup"), {
#             "username": "signupuser",
#             "email": "signupemail@example.com",
#             "password1": "TestPass123!",
#             "password2": "TestPass123!",
#             "terms_of_service": True,
#         }, follow=False)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse("account_email_verification_sent"))
#
#         created_email = EmailAddress.objects.get(email="signupemail@example.com")
#         self.assertFalse(created_email.verified)
#
#         self.assertEqual(len(mail.outbox), 1)
#         sent_email = mail.outbox[0]
#         print(sent_email.body)
#         self.assertIn("Please Confirm Your Email Address", sent_email.subject)
#
#
#         match = re.search(r'(http://.+/accounts/confirm-email/.+/)', sent_email.body)
#         self.assertIsNotNone(match, "Nie znaleziono linku potwierdzającego w e-mailu")
#         confirm_url_full = match.group(1)
#         confirm_path = confirm_url_full.replace('http://testserver', '')
#
#         response_click_link = self.client.get(confirm_path, follow=True)
#         #
#         self.assertEqual(response_click_link.status_code, 200)
#         self.assertTemplateUsed(response_click_link, 'account/email_confirm.html')
#         self.assertContains(response_click_link,'Please confirm that')
#
#         csrf_token = response_click_link.context['csrf_token']
#
#         # 6. Symuluj drugie kliknięcie (POST request) - potwierdzenie formularza
#         response_final_confirmation = self.client.post(confirm_path, {'csrfmiddlewaretoken': csrf_token}, follow=True)
#
#         # 7. Asercje po finalnym potwierdzeniu
#         self.assertEqual(response_final_confirmation.status_code, 200)
#         self.assertTemplateUsed(response_final_confirmation, "account/login.html")  # To jest szablon sukcesu
#         # self.assertContains(response_final_confirmation, "Your e-mail address has been confirmed.")
#
#         updated_email_address = EmailAddress.objects.get(email="signupemail@example.com")
#         self.assertTrue(updated_email_address.verified)




import re
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from allauth.account.models import EmailAddress


class TestsAuthentication(TestCase):
    """
    Test suite for user authentication functionality, including login, signup, and email verification.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Sets up test data shared across all test methods in this class.
        Creates mock social applications (Google and Facebook) and associates them with a test site.
        """
        site, created = Site.objects.get_or_create(id=2)

        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google Test App',
                'client_id': 'mock-google-client-id-for-tests',
                'secret': 'mock-google-secret-for-tests'
            }
        )
        google_app.sites.add(site)

        facebook_app, created = SocialApp.objects.get_or_create(
            provider='facebook',
            defaults={
                'name': 'Facebook Test App',
                'client_id': 'mock-facebook-client-id-for-tests',
                'secret': 'mock-facebook-secret-for-tests'
            }
        )
        facebook_app.sites.add(site)

    def setUp(self):
        """
        Sets up test-specific data before each test method.
        Creates a test user and ensures their email is unverified.
        Clears the email outbox.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="testemail@example.com",
            password="TestPass123!"
        )

        self.email, created = EmailAddress.objects.get_or_create(
            user=self.user,
            email=self.user.email,
            verified=True,
            primary=True,
        )

        if not created and self.email.verified:
            self.email.verified = False
            self.email.save()

        mail.outbox = []

    def test_if_user_was_created(self):
        """
        Tests if the test user was successfully created.
        """
        self.assertTrue(self.user)

    def test_login_success(self):
        """
        Tests if a user can successfully log in with valid credentials.
        Asserts that the response status code is 302 (redirect).
        """
        response = self.client.post(reverse('account_login'), {
            'login': 'testemail@example.com',
            'password': 'TestPass123!',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.session.get('_auth_user_id'))

    def test_login_failure(self):
        """
        Tests if login fails with invalid credentials.
        Asserts that the response status code is 200 (login page reloaded).
        """
        response = self.client.post(reverse('account_login'), {
            'login': 'wrongemail@example.com',
            'password': 'WrongPass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The email address and/or password you specified are not correct')

    def test_signup_success(self):
        """
        Tests if a user can successfully sign up with valid data.
        Asserts that the response redirects to the email verification page.
        """
        response = self.client.post(reverse("account_signup"), {
            "username": "signupuser",
            "email": "signupemail@example.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
            "terms_of_service": True,
        }, follow=False)

        self.assertEqual(response.status_code, 302)
        print(f"Redirect URL: {response.url}")
        print(f"Content (first 500 chars): {response.content.decode('utf-8')[:500]}")
        print(f"Request URL: {response.request['PATH_INFO']}")
        print(f"nagłówek {response['Location']}")
        self.assertRedirects(response, reverse("account_email_verification_sent"))
        self.assertTrue(EmailAddress.objects.filter(email="signupemail@example.com").exists())

    def test_signup_failure(self):
        """
        Tests if signup fails when passwords do not match.
        Asserts that the response status code is 200 (signup page reloaded).
        """
        response = self.client.post(reverse("account_signup"), {
            "username": "signupuser",
            "email": "signupemail@example.com",
            "password1": "TestPass123!",
            "password2": "DifferentPass123!",
            "terms_of_service": True,
        })
        self.assertEqual(response.status_code, 200)

    def test_email_verification_works(self):
        """
        Tests the email verification process.
        Simulates user signup, email confirmation link retrieval, and final confirmation.
        Asserts that the email is marked as verified after the process.
        """
        response = self.client.post(reverse("account_signup"), {
            "username": "signupuser",
            "email": "signupemail@example.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
            "terms_of_service": True,
        }, follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("account_email_verification_sent"))

        created_email = EmailAddress.objects.get(email="signupemail@example.com")
        self.assertFalse(created_email.verified)

        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        print(sent_email.body)
        self.assertIn("Please Confirm Your Email Address", sent_email.subject)

        match = re.search(r'(http://.+/accounts/confirm-email/.+/)', sent_email.body)
        self.assertIsNotNone(match, "Confirmation link not found in the email")
        confirm_url_full = match.group(1)
        confirm_path = confirm_url_full.replace('http://testserver', '')
        response_click_link = self.client.get(confirm_path, follow=True)

        self.assertEqual(response_click_link.status_code, 200)
        self.assertTemplateUsed(response_click_link, 'account/email_confirm.html')
        self.assertContains(response_click_link, 'Please confirm that')

        csrf_token = response_click_link.context['csrf_token']
        response_final_confirmation = self.client.post(confirm_path, {
            'csrfmiddlewaretoken': csrf_token
        }, follow=True)

        self.assertEqual(response_final_confirmation.status_code, 200)
        self.assertTemplateUsed(response_final_confirmation, "account/login.html")

        updated_email_address = EmailAddress.objects.get(email="signupemail@example.com")
        self.assertTrue(updated_email_address.verified)

    def test_logout(self):
        """
        Tests the logout functionality.
        Ensures that the user is logged out and the session is cleared.
        """
        self.client.login(email='testuser@example.com', password='StrongPass123!')
        response = self.client.post(reverse('account_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.client.session.get('_auth_user_id'))

    def test_signup_duplicate_email(self):
        """
        Tests the signup process with a duplicate email.
        Ensures that a user cannot sign up with an email that is already in use.
        """
        response_duplicate_signup = self.client.post(reverse('account_signup'), {
            'username': 'anotheruser',
            'email': 'testemail@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'terms_of_service': 'on'
        }, follow=False)

        self.assertEqual(response_duplicate_signup.status_code, 302)
        self.assertEqual(response_duplicate_signup['Location'], reverse('account_email_verification_sent'))
        self.assertFalse(User.objects.filter(username='anotheruser').exists())

    def test_password_reset_request(self):
        """
        Tests the password reset request functionality.
        Ensures that a password reset email is sent when a valid email is provided.
        """
        response = self.client.post(reverse('account_reset_password'), {
            'email': 'testemail@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('[example.com] Password Reset Email', mail.outbox[0].subject)

    def test_email_verification_page_load_correctly(self):
        """
        Tests if the email verification page loads correctly.
        Ensures that the correct template is used and the page is accessible.
        """
        response = self.client.get(reverse('account_email_verification_sent'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/verification_sent.html')
