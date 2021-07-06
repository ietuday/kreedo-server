import traceback
from rest_framework import serializers
from child.models import*
from users.api.serializer import*
from session.api.serializer import*
from plan.api.serializer import*
from session.models import*
from .utils import*
import logging
from kreedo.conf.logger import*
import pdb
from users.models import*


""" logger """

from kreedo.conf import logger
from kreedo.conf.logger import CustomFormatter
import logging

""" Logger Function """


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('edoofun_scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
# A string with a variable at the "info" level
logger.info("UTILS CAlled ")


""" Child register serializer """


class ChildRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        exclude = ['parent']

    def create(self, validated_data):
        try:
            print("@----->", self)

        except Exception as ex:
            logger.info(ex)
            logger.debug(ex)
            raise ValidationError(ex)
