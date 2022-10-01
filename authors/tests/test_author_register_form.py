from unittest import TestCase

from authors.forms import RegisterForm
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Type your name'),
        ('last_name', 'Type your last name'),
        ('email', 'Type your E-mail'),
        ('username', 'Type your username'),
        ('password', 'Type your password'),
        ('password2', 'Repeat the password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        actual_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, actual_placeholder)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('username', 'Username'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label(self, field, label):
        form = RegisterForm()
        actual_label = form[field].field.label
        self.assertEqual(label, actual_label)

    @parameterized.expand([
        ('email', 'The email must have @'),
        ('username', (
            'Obrigatório. 150 caracteres ou menos. Letras, '
            'números e @/./+/-/_ apenas.'
        )),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )),
    ])
    def test_fields_help_text(self, field, help_text):
        form = RegisterForm()
        actual_help_text = form[field].field.help_text
        self.assertEqual(help_text, actual_help_text)

    @parameterized.expand([
        ('username', 'This field username is required'),
        ('email', 'The E-mail must not be empty')
    ])
    def test_fields_required_error_text(self, field, error_text):
        form = RegisterForm()
        actual_error = form[field].field.error_messages['required']
        self.assertEqual(error_text, actual_error)


class AuthorRegisterFormIntegration(DjangoTestCase):
    def setUp(self) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'user@email.com',
            'password': 'Password123',
            'password2': 'Password123'
        }
        return super().setUp()

    @parameterized.expand([
        ('username', 'This field username is required'),
        ('first_name', 'First name is required'),
        ('last_name', 'Last name is required'),
        ('email', 'The E-mail must not be empty'),
        ('password', 'Your must provide a password'),
        ('password2', 'Please, repeat your password')
    ])
    def test_check_if_fields_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_field_username_has_least_4_characters(self):
        self.form_data['username'] = 'job'

        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)

        msg = 'Username must have least 4 characters'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertEqual(
            msg, response.context['form'].errors.get('username')[0])

    def test_field_username_has_less_150_characters(self):
        self.form_data['username'] = 'A' * 151

        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)

        msg = 'Username must have less than 150 characters'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertEqual(
            msg, response.context['form'].errors.get('username')[0])

    # Checa se quando a senha for fraca retorne o texto de erro
    def test_password_field_is_strong(self):
        self.form_data['password'] = 'abc'

        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)

        msg = 'Password is weak, check the help text'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

    # Confere se as senhas forem diferentes retorne o texto de erro
    def test_passwords_filds_is_same(self):
        self.form_data['password'] = 'Abc12345'
        self.form_data['password2'] = 'Abc'

        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)

        msg = 'Passwords not equals'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

        self.form_data['password'] = 'Abc12345'
        self.form_data['password2'] = 'Abc12345'

        response = self.client.post(url, self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_view_create_returns_404_for_get(self):
        url = reverse('authors:create')
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)

    def test_email_is_unique(self):
        self.form_data['email'] = 'email@email.com'

        url = reverse('authors:create')
        # Create a user
        self.client.post(url, self.form_data, follow=True)

        self.form_data['username'] = 'user2'
        response = self.client.post(url, self.form_data, follow=True)

        msg = 'Email alright exists, please try another'

        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))
