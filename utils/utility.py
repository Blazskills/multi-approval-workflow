# import re
from django.http import JsonResponse
from logging import Handler
import random
from string import digits
from django.template import loader
from rest_framework.response import Response
import requests
from rest_framework import status

# from ideasproject.settings.local import DEFAULT_FROM_EMAIL, MAIL_API_KEY, MAIL_DOMAIN  # TODO:change back

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.relations import RelatedField
from rest_framework import serializers


class UUIDRelatedField(RelatedField):
    """
    A read-write field that represents the target of the relationship
    by a unique 'slug' attribute.
    """

    default_error_messages = {
        "does_not_exist": _("Object with {uuid_field}={value} does not exist."),
        "invalid": _("Invalid value."),
    }

    def __init__(self, uuid_field=None, **kwargs):
        assert uuid_field is not None, "The `uuid_field` argument is required."
        self.uuid_field = uuid_field
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.uuid_field: data})
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                self.error_messages["does_not_exist"].format(
                    uuid_field=self.uuid_field, value=str(data)
                )
            )
        except (TypeError, ValueError):
            raise serializers.ValidationError(self.error_messages["invalid"])


def strreverse(value_str):
    value_str = value_str[::-1]
    return value_str


def generate_digits(length):
    code = ""
    for i in range(length):
        code += random.choice(digits)
    return code


def generate_user_number():
    # Generate a random 12-digit number
    user_number = "".join([str(random.randint(0, 9)) for _ in range(12)])
    return user_number


def generate_username(first_name, last_name, more=False):
    username = f"{first_name[0]}{last_name}"
    username = f"{username}{random.randint(1, 99)}" if more else username
    return username.lower().replace(" ", "")


# def email_sending(
#     from_email,
#     temp_path,
#     subject_construct,
#     email_receiver_list: list,
#     context_construct: dict,
#     email_copy: None,
# ):
#     context = context_construct
#     template = loader.get_template(temp_path)
#     message = template.render(context)
#     API_KEY = MAIL_API_KEY
#     from_email = from_email
#     response = requests.post(
#         f"https://api.mailgun.net/v3/{MAIL_DOMAIN}/messages",
#         auth=("api", API_KEY),
#         data={
#             "from": from_email,
#             "to": email_receiver_list,
#             "cc": email_copy,
#             "subject": subject_construct,
#             "html": message,
#         },
#     )
#     # print(response)
#     if response.status_code != 200:
#         print(response.content)
#         return Response(
#             data={"message": f"Failed to send email {response.content}"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )


def extract_year_pattern(text):
    words = text.split()  # Split the text into words

    for word in words:
        if (
            "/" in word and len(word) == 9
        ):  # Check if the word contains '/' and is 9 characters long
            return word

    return None

# from core_apps.account.tasks import send_email_task



import string
import secrets


def generate_password(length, last_name):
    # Define the characters that can be used in the password
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate a secure random password
    password = ''.join(secrets.choice(characters) for _ in range(length))

    # Modify the last name
    modified_last_name = last_name.lower()[-3:] if len(last_name) > 3 else last_name

    # Combine the password and the modified last name
    final_password = f"{password}{modified_last_name}"

    return final_password


def generate_otp(length):
    # Define the characters that can be used in the password
    characters = string.digits

    # Generate a secure random password
    otp = ''.join(secrets.choice(characters) for _ in range(length))

    return otp
