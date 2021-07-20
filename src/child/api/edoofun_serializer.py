import traceback
from rest_framework import serializers
from child.models import*
from users.api.edoofun_serializer import*
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

            parents_detail = self.context['parent_detail']['parents']

            parent_list = []
            for parent in parents_detail:

                try:
                    parent_serializer = EdoofunParentSerializer(
                        data=dict(parent))
                    if parent_serializer.is_valid():
                        parent_serializer.save()

                        if parent_serializer.data['msg'] == 'user create':

                            parent_data = {
                                "user_obj": parent_serializer.data['user_obj'],
                                "relationship_with_child": parent['relationship_with_child'],
                                "phone": parent['phone'],
                                "gender": parent['gender'],
                                "photo": parent['photo'],
                                "role": []
                            }
                            parent_detail_serializer = EdoofunParentDetailSerializer(
                                data=dict(parent_data))
                            if parent_detail_serializer.is_valid():
                                parent_detail_serializer.save()
                                parent_id = parent_detail_serializer.data['user_obj']
                                parent_list.append(parent_id)

                            else:

                                print("Detail  Serializer--------",
                                      parent_detail_serializer.errors)
                        else:
                            parent_list.append(parent_serializer.data['user_obj'])
                            print("User Exist")
                    else:
                        print("User Exist")
                except Exception as ex:
                    logger.debug(ex)
                    logger.info(ex)

                    raise ValidationError(ex)

            self.context['child_detail']['parent'] = parent_list
            validated_data = self.context['child_detail']

            child = super(ChildRegisterSerializer, self).create(validated_data)
            print("child Created")
            child.save()
            return child
            # section = self.context['academic_session_detail']['section']
            # grade = self.context['academic_session_detail']['grade']

            # acadmic_ids = AcademicSession.objects.filter(
            #     grade=grade, section=section)
            # if len(acadmic_ids) != 0:
            #     child_id = child.id
            #     academic_session_detail = {
            #         "child": child_id,
            #         "academic_session": acadmic_ids,
            #     }
            #     """  create child plan """

            #     try:

            #         child_plan_serializer = ChildPlanCreateSerailizer(
            #             data=dict(academic_session_detail))
            #         if child_plan_serializer.is_valid():
            #             child_plan_serializer.save()

            #         else:
            #             raise ValidationError(child_plan_serializer.errors)
            #     except Exception as ex:
            #         print("@@@@@@@@@@@@@@", ex)
            #         logger.debug(ex)
            #         logger.info(ex)
            #         raise ValidationError(ex)
            # else:
            #     print("Child plan not created")

        except Exception as ex:
            print("serializer error", ex)
            print("traceback---------", traceback.print_exc())
            logger.info(ex)
            logger.debug(ex)
            raise ValidationError(ex)




""" Update Secret Pin For Child Serializer """
class UpdateSecretPinForChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        field = ['secret_pin']
    

    def create(self,validated_data):
        try:
            print("Validated data",validated_data)
            
        except Exception as ex:
            print(ex)
