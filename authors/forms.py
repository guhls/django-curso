import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr, attr_value):
    field.widget.attrs[attr] = attr_value


def add_placeholder(field, placeholder_value):
    add_attr(field, 'placeholder', placeholder_value)


def add_error_messages(field, type_error, msg_error):
    field.error_messages[type_error] = msg_error


def add_label(field, label_value):
    field.label = label_value


def set_field_required(fields):
    for field in fields:
        field.required = True


# A função retornara None para o campo password caso não haja match do regex
def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            'Password is weak, check the help text', code='invalid')


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # First_name e Last_name usando o init
        add_placeholder(self.fields['first_name'], 'Type your name')
        add_placeholder(self.fields['last_name'], 'Type your last name')

        add_error_messages(
            self.fields['first_name'], 'required', 'First name is required'
        )
        add_error_messages(
            self.fields['last_name'], 'required', 'Last name is required'
        )

        add_label(self.fields['first_name'], 'First name')
        add_label(self.fields['last_name'], 'Last name')

        set_field_required([
            self.fields['first_name'],
            self.fields['last_name']
        ])

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
        error_messages={
            'required': 'Your must provide a password'
        },
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
        label='Password2',
        error_messages={
            'required': 'Please, repeat your password'
        },
    )

    username = forms.CharField(
        min_length=4, max_length=150,
        label='Username',
        help_text=('Obrigatório. 150 caracteres ou menos. Letras, '
                   'números e @/./+/-/_ apenas.'),
        error_messages={
            'required': 'This field username is required',
            'min_length': 'Username must have least 4 characters',
            'max_length': 'Username must have less than 150 characters',
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Type your username'
            }
        )
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Type your E-mail',
            }
        ),
        label='E-mail',
        help_text='The email must have @',
        error_messages={
            'required': 'The E-mail must not be empty'
        }
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

    # Para tornar o email unique é necessario criar a logica no clean
    #   pois não é possivel modificar o model User
    def clean_email(self):
        email = self.cleaned_data['email']

        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'Email alright exists, please try another', code='invalid')
        else:
            return email

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
