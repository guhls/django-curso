from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr, attr_value):
    field.widget.attrs[attr] = attr_value


def add_placeholder(field, placeholder_value):
    add_attr(field, 'placeholder', placeholder_value)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['last_name'], 'Your last name goes here')

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat the password',
            }
        )
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
            'password': 'Password'
        }

        help_texts = {
            'email': 'The email must have @'
        }

        error_messages = {
            'username': {
                'required': 'This field is required'
            },
        }

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Type your user here',
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'placeholder': 'Type your password',
                    'class': 'input-password',
                }
            )
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'teste' in data:
            raise ValidationError(
                'Palavra %(value)s não é permitida',
                code='invalid',
                params={'value': '"teste"'}
            )

    def clean(self):
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
