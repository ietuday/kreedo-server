# validate email
from kreedo.conf.logger import*
import logging
import traceback
from django.template.loader import get_template
from django.contrib.auth import authenticate
import datetime
import calendar
import os
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# import auth user
from django.contrib.auth.models import User

# genrate username
from random_username.generate import generate_username

# email
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from users.models import UserDetail
from kreedo.settings import EMAIL_HOST_USER
import random
import string
from kreedo.conf.logger import CustomFormatter


""" Token genrate package """
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


""" Validate Email """


def user_validate_email(email):
    try:

        email_valid = validate_email(email)
        return True
    except ValidationError:
        return False


""" genrate username """


def create_username():
    try:
        username = generate_username(1)[0]
        while User.objects.filter(username=username).exists():
            username = generate_username(1)[0]
        return username
    except Exception as ex:
        raise ValidationError("Username is not Created")


""" Genrate password """


def create_password(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    password = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", password)
    return password


""" authenticate username and password """


def authenticate_username_password(username, password):
    try:

        return authenticate(username=username, password=password)
    except Exception as error:
        raise ValidationError("Login failed , Invalid Username and Password")


def authenticate_username(username, old_password):
    try:
        #  authenticate(username=username)
        return authenticate(username=username)
    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        raise ValidationError("User not Authorized")


""" Validate Email and Password """


def validate_auth_user(email, password):
    if email is not None and password is not None:
        return True
    else:
        return False


""" Validate Email and Password """


def validate_auth_user_phone(phone, password):
    if phone is not None and password is not None:
        return True
    else:
        return False


""" Genrate Token """


def genrate_token(user):
    try:
        payload = jwt_payload_handler(user)

        return jwt_encode_handler(payload)
    except Exception as error:
        raise ValidationError(error)


""" send temprorary link function """


def send_temprorary_password_mail(user_obj, user_detail_obj, genrated_password):
    try:
        genrate_active_link = genrate_link(
            user_obj, user_detail_obj, genrated_password)
    except Exception as ex:
        raise ValidationError("Error in genrate verification link")


""" genrate activation link """


def genrate_link(user_obj, user_detail_obj, genrated_password):
    try:

        x = {
            'email_subject': 'Kreedo Application: Your account is created',
            'uid': urlsafe_base64_encode(force_bytes(user_obj.pk)),
            'token': default_token_generator.make_token(user_obj),
        }
        """Create Email Verified link"""
        activation_key = x['uid'] + '-' + x['token']

        """Add activation key and expiration date to user detail"""

        user_detail_instance = UserDetail.objects.filter(
            user_obj=user_obj).first()

        user_detail_instance.activation_key = activation_key
        user_detail_instance.activation_key_expires = datetime.datetime.strftime(
            datetime.datetime.now() + datetime.timedelta(days=60), "%Y-%m-%d %H:%M:%S")

        user_detail_instance.save()

        """ Call  create  temproray passwordmail function """
        user_created_password_mail(user_obj, genrated_password)

        context = {'isSuccess': True,
                   'message': 'Token Sent to user', 'error': '', "data": user_detail_instance}
        return context
    except Exception as error:
        logger.debug(error)
        logger.info(error)
        raise ValidationError("Failed to send Token to user")


"""authenticate_user"""


def authenticate_user(username):
    try:
        user = authenticate(username=username)
        return user
    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        raise ValidationError("User not Authorized")
