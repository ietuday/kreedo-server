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


""" Create Log for Utils"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("UTILS CAlled ")


""" Validate Email and Password """


def validate_auth_user(email, password):
    if email is not None and password is not None:
        return True
    else:
        return False





""" Validate Email """


def user_validate_email(email):
    try:
        email_valid = validate_email(email)
        return True
    except ValidationError:
        return False


""" genrate username """


def create_unique_username():
    try:
        username = generate_username(1)[0]
        while User.objects.filter(username=username).exists():
            username = generate_username(1)[0]
        return username
    except Exception as ex:
        logger.info(ex)
        logger.debug(ex)
        raise ValidationError("Username is not Created")


""" send User Details """


def send_user_details(user_obj, user_detail_obj):
    try:
        generate_user_activation_link_response = generate_user_activation_link(
            user_obj, user_detail_obj, True)
        logger.info(generate_user_activation_link_response)
        logger.debug(generate_user_activation_link_response)
    except Exception as ex:
        logger.info(ex)
        logger.debug(ex)
        raise ValidationError("Error in genrate verification link")



""" genrate activation link """


def generate_user_activation_link(user_obj, user_detail_obj, is_user_created=False):
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
        if is_user_created == True:
            link = os.environ.get('KREEDO_URL') + \
                '/users/email-confirm-verify/' + activation_key

            """ Call create mail function """
            user_created_mail(user_obj, link)
        else:

            link = os.environ.get('KREEDO_URL') + \
                '/users/reset_password_confirm/' + activation_key

            forgot_password_mail(user_obj, link)
        context = {'isSuccess': True,
                   'message': 'Token Sent to user', 'error': '', "data": user_detail_instance}
        return context
    except Exception as error:
        logger.debug(error)
        logger.info(error)
        raise ValidationError("Failed to send Token to user")


""" Account craeted function for mail """


def user_created_mail(user_obj, link):

    try:

        subject = 'Kreedp Application: Your account is created'
        template = 'user_creation_web_admin.html'
        from_email = EMAIL_HOST_USER
        to = user_obj.email
        html_content = get_template(template)
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content.render(
            {'first_name': user_obj.first_name, 'url': link, 'email': user_obj.email}), "text/html")
        msg.send()
    except Exception as error:
        raise ValidationError("Failed to send Email")


""" Forget password"""


def forgot_password_mail(user_obj, link):
    try:
        email = user_obj.email
        first_name = user_obj.first_name
        subject = 'Kreedo Application: Choose a new password'
        template = 'forgot_password.html'
        from_email = EMAIL_HOST_USER
        to = email
        html_content = get_template(template)
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content.render(
            {'first_name': first_name, 'url': link}), "text/html")
        msg.send()
    except Exception as error:
        raise serializers.ValidationError("Failed to send Email")


# authenticate password


def authenticate_password(username, old_password):
    try:
        user = authenticate(username=username, password=old_password)
        return user
    except Exception as ex:
        logger.debug(ex)
        logger.info(ex)
        raise ValidationError("User not Authorized")


"""  verified user email """


def verified_user_mail(first_name, email):
    try:
        print("first_name, email------>", first_name, email)
        subject = 'Kreedo Application: User Verified'
        template = 'user_verified.html'
        from_email = EMAIL_HOST_USER
        to = email
        html_content = get_template(template)
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content.render(
            {'first_name': first_name}), "text/html")
        msg.send()
    except Exception as error:
        raise ValidationError("Failed to send Email")


""" authenticate username and password """


def authenticate_username_password(username, password):
    try:

        return authenticate(username=username, password=password)
    except Exception as error:
        raise ValidationError("Login failed , Invalid Username and Password")


""" Genrate Token """


def genrate_token(user):
    try:
        payload = jwt_payload_handler(user)

        return jwt_encode_handler(payload)
    except Exception as error:
        raise ValidationError(error)


def password_reseted_mail(first_name, email):
    try:
        subject = 'Kreedo Application: New password is set'
        template = 'reset_password.html'
        from_email = EMAIL_HOST_USER
        to = email
        html_content = get_template(template)
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content.render(
            {'first_name': first_name}), "text/html")
        msg.send()
    except Exception as error:
        raise serializers.ValidationError("Failed to send Email")


""" Genrate password """


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    password = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", password)
    return password


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


"""  password mail function """


def user_created_password_mail(user_obj, genrated_password):

    try:

        subject = 'Kreedp Application: Your account is created'
        template = 'add_user.html'
        from_email = EMAIL_HOST_USER
        to = user_obj.email
        html_content = get_template(template)
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content.render(
            {'first_name': user_obj.first_name, 'password': genrated_password, 'email': user_obj.email}), "text/html")
        msg.send()
    except Exception as error:
        raise ValidationError("Failed to send Email")


""" Reset password link """
def generate_reset_password_link(user_obj):
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
        user_email = user_obj.email
        link = os.environ.get('FRONTEND_URL') + \
                '/auth/reset-password/' +user_email+'/'+ activation_key
        
        print("LINK------->", link)
        return link
    except Exception as error:
        logger.debug(error)
        logger.info(error)
        raise ValidationError("Failed to Create link")



def user_reset_password_link(user_obj, link):
    try:
        subject = 'Kreedp Application: Reset Your Password'
        template = 'reset_password.html'
        from_email = EMAIL_HOST_USER
        to = user_obj.email
        html_content = get_template(template)
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content.render(
            {'first_name': user_obj.first_name, 'url': link, 'email': user_obj.email}), "text/html")
        msg.send()
    except Exception as error:
        raise ValidationError("Failed to send Email")












def add_months(sourcedate, months):
    print("##############",sourcedate,months)
    # print(mont
    sourcedate = datetime.datetime.strptime(str(sourcedate), '%d/%m/%Y').date()
    # print(datetime.datetime.strptime(sourcedate , '%d/%m/%Y').date())
    months = int(months)
    print("##############",sourcedate,months)
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)


def addYears(d, years):
    try:
#Return same day of the current year        
        return d.replace(year = d.year + years)
    except ValueError:
#If not same day, it will return other, i.e.  February 29 to March 1 etc.        
        return d + (datetime.date(d.year + years, 1, 1) - datetime.date(d.year, 1, 1))


""" Encription """
def genrate_encrypted_string(random_string):
    try:
        encrypted_string =""
        for ch in random_string:
            encrypted_string += chr(ord(ch) + 15)
        return encrypted_string

    except Exception as ex:
        raise ValidationError(ex)

""" Decryption """

def genrate_decrypted_string(random_string):
    try:
        decrypted_string =""
        for ch in random_string:
            decrypted_string += chr(ord(ch) - 15)
          
        return decrypted_string
        
    except Exception as ex:
        raise ValidationError(ex)