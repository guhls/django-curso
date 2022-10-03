from django.forms import CharField, Form, PasswordInput
from utils.funcs_forms import add_placeholder


class LoginForm(Form):
    def __init__(self):
        super().__init__()

        add_placeholder(self.fields['username'], 'Type your username')
        add_placeholder(self.fields['password'], 'Type your password')

    username = CharField()
    password = CharField(
        widget=PasswordInput()
    )
