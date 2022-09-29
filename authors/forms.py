import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr, attr_value):
    field.widget.attrs[attr] = attr_value


def add_placeholder(field, placeholder_value):
    add_attr(field, 'placeholder', placeholder_value)


# A função retornara None para o campo password caso não haja match do regex
def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError('Password is weak', code='invalid')


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # First_name e Last_name usando o init
        add_placeholder(self.fields['first_name'], 'Type your name')
        add_placeholder(self.fields['last_name'], 'Type your last name')

    # Password e password2 sobreescrevendo os campos no Meta usando variaveis
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Type your password',
            }
        ),
        validators=[strong_password],
        label='Password',
        help_text='Password must have at least one uppercase letter, '
        'one lowercase letter and one number. The length should be '
        'at least 8 characters.'
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat the password',
            }
        ),
        label='Password2'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
        }

        help_texts = {
            'email': 'The email must have @'
        }

        error_messages = {
            'username': {
                'required': 'This field is required'
            },
        }

        # Adcionando placeholders em username e email em widgets no Meta
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Type your username',
                }
            ),
            'email': forms.PasswordInput(
                attrs={
                    'placeholder': 'Type your E-mail',
                    'class': 'input-email',
                }
            )
        }

    # Ele primeiro checa usnado os validators
    # O clean_password e clean é realizado depois
    def clean(self):
        if not self.errors:
            data = super().clean()

            password = data.get('password')
            password2 = data.get('password2')

            passwords_errors = ValidationError(
                'Passwords not equals', code='invalid')

            if password != password2:
                raise ValidationError(
                    {
                        'password': passwords_errors,
                        'password2': [passwords_errors],
                    }
                )
