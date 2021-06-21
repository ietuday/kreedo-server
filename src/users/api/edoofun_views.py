"""
    DJANGO LIBRARY IMPORT
"""
import math
import pdb
import csv
from pandas import DataFrame
import json
from .serializer import*
from ..models import*
from .filters import*
from kreedo.general_views import Mixins, GeneralClass
from kreedo.conf.logger import CustomFormatter
import traceback
import datetime
import logging
import pandas as pd

import random
from kreedo.settings import AWS_SNS_CLIENT, EMAIL_HOST_USER
from passlib.hash import pbkdf2_sha256

from rest_framework .generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rest_framework.decorators import permission_classes
from django.core.exceptions import ValidationError
from django.shortcuts import render
from users.api.custum_storage import FileStorage
from schools.models import*
from schools.api.serializer import*
from package.models import*
from package.api.serializer import*
from session.models import*
from session.api.serializer import*

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(