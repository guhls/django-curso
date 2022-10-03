import re

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
