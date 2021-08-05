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
from session.api.serializer import*
from plan.api.edoofun_serializer import*

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
            print("validated_data---------", validated_data)
            child_instance = Child.objects.create(**validated_data)
            child_instance.save()
            # return child_instance

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
                            parent_list.append(
                                parent_serializer.data['user_obj'])
                            print("User Exist1", parent_list)

                    else:
                        print("User Exist2")
                except Exception as ex:
                    logger.debug(ex)
                    logger.info(ex)

                    raise ValidationError(ex)
            validated_data['parent'] = parent_list

            child_instance.parent.set(validated_data['parent'])

            child_instance.save()
            return child_instance

            # self.context['child_detail']['parent'] = parent_list
            # validated_data = self.context['child_detail']

            # print("validated_data-----------",
            #       self.context['school_detail']['school'])
            # school = validated_data.pop('school')

            # class_teacher = validated_data.pop('class_teacher')
            # account_manager = validated_data.pop('account_manager')
            # parents = validated_data.pop('parent')
            # print("%%%%%%%%%%%%", parents, account_manager,class_teacher,school)

            # child_instance = Child.objects.create(**validated_data)
            # child_instance.school = self.context['school_detail']['school']
            # # child_instance.parent.set(parent_list)
            # # child_instance.class_teacher=class_teacher
            # # child_instance.account_manager=account_manager

            # child_instance.save()

            # child = super(ChildRegisterSerializer, self).create(validated_data)
            # print("child Created")
            # child.save()
            # return child_instance

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
        fields = ['secret_pin']

    def to_representation(self, instance):
        instance = super(UpdateSecretPinForChildSerializer,
                         self).to_representation(instance)
        instance['data'] = self.context['data']
        return instance

    def create(self, validated_data):
        try:
            
            child_id = self.context['child_detail']['child']
          
            user_id = self.context['child_detail']['logged_user']
            user_obj_detail = UserDetail.objects.get(pk=user_id.id)
            if user_obj_detail:
                user_id = User.objects.get(
                    id=self.context['child_detail']['parent_id']).id
                if Child.objects.filter(id=child_id, parent=user_id, secret_pin=self.context['child_detail']['old_pin']).exists():
                    child_qs = Child.objects.get(
                        id=child_id, parent=user_id, secret_pin=self.context['child_detail']['old_pin'])
                
                    child_qs.secret_pin = self.context['child_detail']['new_pin']
                    child_qs.save()
                    data = "PIN has been reset."
                    self.context.update({"data": data})
                    return validated_data
                else:
                    raise ValidationError("Child not found")
            else:
                ValidationError("InValid Signature")
        except Exception as ex:
          
            raise ValidationError(ex)


class ChildListParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'
        depth = 1


class ChildDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        fields = '__all__'
        # depth= 2

    def to_representation(self, obj):
        serialized_data = super(
            ChildDetailSerializer, self).to_representation(obj)

        child_id = serialized_data.get('id')

        parent_list = serialized_data.get('parent')

        print("$$$$$$$$$$", parent_list)
        user_qs = UserDetail.objects.filter(user_obj__in=parent_list)
        user_qs_serializer = UserDetailListSerializer(user_qs, many=True)

        serialized_data['parents'] = user_qs_serializer.data

        child_id_qs = ChildPlan.objects.filter(child=child_id)
        # if child_id_qs:
        #     print("child_id_qs----", child_id_qs)
        #     child_id_serializer = ChildPlanChildSerializer(
        #         child_id_qs, many=True)
        #     serialized_data['academic_session_data'] = child_id_serializer.data

        # else:
        #     serialized_data['academic_session_data'] = ""

        return serialized_data


""" Child list by License Serializer """


class ChildListbylicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'
        depth = 1
