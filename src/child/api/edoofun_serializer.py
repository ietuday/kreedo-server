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

            validated_data = self.context['child_detail']

            child = super(ChildCreateSerializer, self).create(validated_data)

            parents_detail = self.context['parent_detail']['parents']

            parent_list = []
            for parent in parents_detail:

                try:

                    parent_serializer = EdoofunParentSerializer(data=dict(parent))
                    if parent_serializer.is_valid():
                        parent_serializer.save()
                        parent_data = {
                            "user_obj": parent_serializer.data['id'],
                            "relationship_with_child": parent['relationship_with_child'],
                            "phone": parent['phone'],
                            "gender":parent['gender'],
                            "photo":parent['photo']

                        }
                        parent_detail_serializer = EdoofunParentDetailSerializer(
                            data=dict(parent_data))
                        if parent_detail_serializer.is_valid():
                            parent_detail_serializer.save()
                            parent_id = parent_detail_serializer.data['user_obj']
                            parent_list.append(parent_id)
                        else:

                            raise ValidationError(parent_detail_serializer.errors)

                    else:
                        raise ValidationError(parent_serializer.errors)

                except Exception as ex:
                    logger.debug(ex)
                    logger.info(ex)

                    raise ValidationError(ex)

            validated_data['parent'] = parent_list

            child.parent.set(validated_data['parent'])

            child.save()

            acad_session = self.context['academic_session_detail']['academic_session']
            section = self.context['academic_session_detail']['section']
            grade = self.context['academic_session_detail']['grade']
            class_teacher = self.context['academic_session_detail']['class_teacher']

            acadmic_ids = AcademicSession.objects.filter(id=acad_session,
                                                         grade=grade, section=section, class_teacher=class_teacher).values('id')[0]['id']
            
            child_id = child.id
            academic_session_detail = {
                "child":child_id,
                "academic_session": acadmic_ids,
                "subjects": self.context['academic_session_detail']['subjects'],
                "curriculum_start_date": self.context['academic_session_detail']['curriculum_start_date']
            }
            """  create child plan """

            try:

                child_plan_serializer = ChildPlanCreateSerailizer(
                    data=dict(academic_session_detail))
                if child_plan_serializer.is_valid():
                    child_plan_serializer.save()

                else:
                    raise ValidationError(child_plan_serializer.errors)
            except Exception as ex:
                print("@@@@@@@@@@@@@@", ex)
                logger.debug(ex)
                logger.info(ex)
                raise ValidationError(ex)

            return child
           

        except Exception as ex:
            print("@#######", ex)
            print("traceback---------", traceback.print_exc())
            logger.info(ex)
            logger.debug(ex)
            raise ValidationError(ex)
