from rest_framework import serializers
""" 
    Django Files 
"""
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
""" 
    App Files  
"""
from ..models import*
from address.api.serializer import AddressSerializer
from .utils import*
import traceback
import logging
from kreedo.conf.logger import*



""" Create Log for Edoo-Fun  Serializer"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('edoofun_scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("Serailizer CAlled ")

