from django.test import TestCase
from django.urls import reverse
from .models import Profile, Follower, Message
from .forms import SignInForm, SignUpForm, PostForm




def add_user():
    p = Profile(username='karen', email='karen@karen.dk')
    p.set_password("Manager2020")
    p.save()
    return p

class MyTimelineViewTests(TestCase):
    def test_usernames_me_and_followed(self):
        pass

class UserTimelineViewTests(TestCase):
    def test_unique_username_on_timeline(self):
        pass

class PublicTimelineViewTests(TestCase):
    def test_public_timeline(self):
        response = self.client.get(reverse('public_timeline'))
        self.assertEqual(response.status_code, 200)

    def test_no_messages(self):
        response = self.client.get(reverse('public_timeline'))
        self.assertContains(response, "There's no message so far.")

    def test_messages(self):
        p = add_user()
        text = "I'd like to speak to the manager"
        m = Message(author=p, content=text)
        m.save()
        response = self.client.get(reverse('public_timeline'))
        self.assertEqual(len(response.context.get("messages")), 1)
        self.assertEqual(response.context.get("messages")[0].get('text'), text)

class PostFormTest(TestCase):
    def test_post(self):
        text = "I am really sorry, but the manager is not in today. I'm sure we can figure something out. How about the sorbet?"
        form = PostForm(data={"content": text})
        self.assertEquals(form.errors['content'], ["Ensure this value has at most 60 characters (it has 111)."])


class SignInFormTests(TestCase):

    def test_sign_in_form_fails(self):
        response = self.client.post('/login/', {'username': 'bob', 'password': 'PornForAll'})
        self.assertEqual(response.context['form'].errors['__all__'], ['Please enter a correct username and password. Note that both fields may be case-sensitive.'])

    def test_sign_in_form_passes(self):
        p = add_user()
        response = self.client.post('/login/', {'username': 'karen', 'password': 'Manager2020'})
        self.assertRedirects(response, '/timeline/', status_code=302, target_status_code=200, fetch_redirect_response=True)


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
    def test_add_user(self):
        add_user()

    def test_remove_user(self):
        p = add_user()
        p.delete()


class FollowerTests(TestCase):
    def make_users(self):
        p = add_user()

        p2 = Profile(username='kevin', email='kevin@kevin.dk')
        p2.set_password("password1234")
        p2.save()

        return p, p2

    def test_add_follower(self):
        p, p2 = self.make_users()
        f = Follower(source_user=p, target_user=p2)
        f.save()

    def test_remove_follower(self):
        p, p2 = self.make_users()
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
