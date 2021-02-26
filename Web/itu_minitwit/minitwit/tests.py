from django.test import TestCase

from .models import Profile, Follower, Message
from .forms import SignInForm, SignUpForm


class LogInViewTests(TestCase):
    def test_sign_in(self):
        pass

class MyTimelineViewTests(TestCase):
    def test_post(self):
        pass

    def test_usernames_me_and_followed(self):
        pass

class UserTimelineViewTests(TestCase):
    def test_unique_username_on_timeline(self):
        pass

class PublicTimelineViewTests(TestCase):
    def test_public_timeline(self):
        pass


class SignInFormTests(TestCase):
    def test_sign_in_form(self):
        pass

class SignUpFormTests(TestCase):
    def test_repeat_password(self):
        form = SignUpForm(data= {'username': 'karen',
                                'email': 'karen@karen.dk',
                                'password1': '2020Manager',
                                'password2': 'Manager2020'})
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.'])

    def test_email_validity(self):
        form = SignUpForm(data= {'username': 'karen',
                                'email': 'karen',
                                'password1': 'Manager2020',
                                'password2': 'Manager2020'})

        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])

    def test_required_field(self):
        form = SignUpForm(data= {'email': 'karen@karen.dk',
                                'password1': 'Manager2020',
                                'password2': 'Manager2020'})

        self.assertEqual(form.errors['username'], ["This field is required."])


class ProfileTests(TestCase):
    def add_user(self):
        p = Profile(username='karen', email='karen@karen.dk')
        p.set_password("Manager2020")
        p.save()

    def test_add_user(self):
        self.add_user()

    def test_remove_user(self):
        self.add_user()
        p = Profile.objects.get(username='karen')
        p.delete()


class FollowerTests(TestCase):
    def make_users(self):
        p = Profile(username='karen', email='karen@karen.dk')
        p.set_password("Manager2020")
        p.save()

        p2 = Profile(username='kevin', email='kevin@kevin.dk')
        p2.set_password("password1234")
        p2.save()

        return p, p2

    def test_add_follower(self):
        p, p2 = self.make_users()
        f = Follower(source_user=p, target_user=p2)
        f.save()

    def test_remove_follower(self):
        p = Profile(username='karen', email='karen@karen.dk')
        p.set_password("Manager2020")
        p.save()

        p2 = Profile(username='kevin', email='kevin@kevin.dk')
        p2.set_password("password1234")
        p2.save()

        f = Follower(source_user=p, target_user=p2)
        f.save()

        f = Follower.objects.get(source_user=p, target_user=p2)
        f.delete()


class MessageTests(TestCase):
    def add_message(self):
        p = Profile(username='karen', email='karen@karen.dk')
        p.set_password("Manager2020")
        p.save()

        m = Message(author=p, content="I'd like to speak to the manager")
        m.save()

    def test_add_message(self):
        self.add_message()

    def test_remove_message(self):
        self.add_message()
        m = Message.objects.get(content="I'd like to speak to the manager")
        m.delete()
