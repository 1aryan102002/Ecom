from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import Profile
from .token import account_activation_token


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class RegisterAndVerifyTests(TestCase):
    def test_register_creates_inactive_user_and_sends_email(self):
        response = self.client.post(reverse('register'), {
            'username': 'newbie', 'email': 'newbie@example.com',
            'first_name': 'New', 'last_name': 'Bie',
            'password1': 'Str0ng-pass-123', 'password2': 'Str0ng-pass-123',
        })
        self.assertRedirects(response, reverse('email_verification_sent'))
        user = User.objects.get(username='newbie')
        self.assertFalse(user.is_active)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('/users/email-verification/', mail.outbox[0].body)

    def test_valid_link_activates_user_once(self):
        user = User.objects.create_user('pending', password='Str0ng-pass-123', is_active=False)
        url = reverse('email_verification', args=[
            urlsafe_base64_encode(force_bytes(user.pk)),
            account_activation_token.make_token(user),
        ])
        self.assertRedirects(self.client.get(url), reverse('email_verification_success'))
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        # The token includes is_active, so the same link fails the second time.
        self.assertRedirects(self.client.get(url), reverse('email_verification_failed'))

    def test_tampered_link_fails(self):
        url = reverse('email_verification', args=['not-base64!', 'bad-token'])
        self.assertRedirects(self.client.get(url), reverse('email_verification_failed'))


class LoginLogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('shopper', password='Str0ng-pass-123', first_name='Asha')

    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'id="login-form"')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {'username': 'shopper', 'password': 'Str0ng-pass-123'}, follow=True)
        self.assertRedirects(response, reverse('hero_home'))
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertContains(response, 'Welcome back, Asha!')
        self.assertContains(response, 'id="nav-logout-btn"')

    def test_wrong_password(self):
        response = self.client.post(reverse('login'), {'username': 'shopper', 'password': 'nope'})
        self.assertContains(response, 'Invalid username or password.')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_unverified_user_gets_clear_message(self):
        User.objects.create_user('unverified', password='Str0ng-pass-123', is_active=False)
        response = self.client.post(reverse('login'), {'username': 'unverified', 'password': 'Str0ng-pass-123'})
        self.assertContains(response, 'Please verify your email before logging in.')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_get_shows_confirmation_and_keeps_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertContains(response, 'id="logout-confirm-btn"')
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout_post_logs_out(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('hero_home'))
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'You have been logged out.')


class ProfilePageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('shopper', email='asha@example.com', password='Str0ng-pass-123',
                                             first_name='Asha', last_name='Rao')

    def test_anonymous_user_is_sent_to_login(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_profile_shows_account_and_profile_details(self):
        Profile.objects.create(user=self.user, phone_number='9876543210', recovery_email='backup@example.com')
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        for text in ('Asha Rao', '@shopper', 'asha@example.com', '9876543210', 'backup@example.com',
                     'id="profile-cart-empty"'):
            self.assertContains(response, text)

    def test_user_without_profile_row_still_renders(self):
        # e.g. accounts made with createsuperuser before Profile existed
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'Not added', count=2)
