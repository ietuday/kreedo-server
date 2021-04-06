
#validate email
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

# import os , environment
import os
import datetime

# authentictaion package
from django.contrib.auth import authenticate

# get template
from django.template.loader import get_template

import traceback

""" Validate Email and Password """
def validate_auth_user(email, password):
    if email is not None and password is not None:
        print("trueee------>")
        
        return True
    else:
        return False

""" Validate Email """
def user_validate_email(email):
    try:
        print("email--------->",email)
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
            print("username",username)
        return username
    except Exception as ex:
        raise ValidationError("Username is not Created")


    
""" send User Details """

def send_user_details(user_obj, user_detail_obj):
    try:
        print("send_user_details------->",user_obj,user_detail_obj)
        generate_user_activation_link_response = generate_user_activation_link(
                        user_obj, user_detail_obj, True)
        print(generate_user_activation_link_response)
    except Exception as x:
        raise ValidationError("Error in genrate verification link")
    
""" genrate activation link """

def generate_user_activation_link(user_obj, user_detail_obj, is_user_created=False):
    try:

        x = {
            'email_subject':'Kreedo Application: Your account is created',
            'uid':urlsafe_base64_encode(force_bytes(user_obj.pk)),
            'token': default_token_generator.make_token(user_obj),
        }
        print("x------------>",x)
        """Create Email Verified link"""
        activation_key = x['uid'] + '-' + x['token']
        
        """Add activation key and expiration date to user detail"""
        
            
        user_detail_instance = UserDetail.objects.filter(user_obj = user_detail_obj['user_obj']).first()
        print("user_detail_instance------------>",user_detail_instance)

        user_detail_instance.activation_key = activation_key
        user_detail_instance.key_expires = datetime.datetime.strftime(
            datetime.datetime.now() + datetime.timedelta(days=60), "%Y-%m-%d %H:%M:%S")

        user_detail_instance.save()
        if is_user_created == True:
            link = os.environ.get('KREEDO_URL') + \
            '/users/email_confirm_verify/' + activation_key
            
            """ Call create mail function """
            user_created_mail(user_obj, link)
        else:

            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ else",user_detail_instance)
            link = os.environ.get('KREEDO_URL') + \
            '/users/reset_password_confirm/' + activation_key
            forgot_password_mail(user_obj, link)
        context = {'isSuccess': True,
                   'message': 'Token Sent to user', 'error': '', "data" : user_detail_instance}
        return context
    except Exception as error:
        print("error",error)
        print(traceback.print_exc())
        raise ValidationError("Failed to send Token to user")


""" Account craeted function for mail """
def user_created_mail(user_obj, link):

    try:
        print("LINK",link)
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


   


