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

""" Create Log for Serializer"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)

""" block Create Serailizer """
class BlockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = '__all__'
        


""" Child Create Serializer """


class ChildCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        exclude = ['parent']

    # def to_representation(self, instance):
    #     try:
    #         instance = super(ChildCreateSerializer,
    #                          self).to_representation(instance)
    #         """ Update details in RESPONSE """
    #         instance['parent_data'] = self.context['parent_detail_serializer_data']
    #         instance['child_plan_data'] = self.context['child_plan_serializer']

    #         return instance
    #     except Exception as ex:
    #         print("error", ex)
    #         print("traceback", traceback.print_exc())
    #         logger.debug(ex)
    #         raise ValidationError(ex)

    def create(self, validated_data):
        try:

            validated_data = self.context['child_detail']

            child = super(ChildCreateSerializer, self).create(validated_data)

            parents_detail = self.context['parent_detail']['parents']

            parent_list = []
            for parent in parents_detail:

                try:

                    parent_serializer = ParentSerializer(data=dict(parent))
                    if parent_serializer.is_valid():
                        parent_serializer.save()
                        parent_data = {
                            "user_obj": parent_serializer.data['id'],
                            "relationship_with_child": parent['relationship_with_child'],
                            "phone": parent['phone']

                        }
                        parent_detail_serializer = ParentDetailSerializer(
                            data=dict(parent_data))

                        if parent_detail_serializer.is_valid():

                            parent_detail_serializer.save()

                            parent_id = parent_detail_serializer.data['user_obj']
                            parent_list.append(parent_id)
                            
                            # self.context.update({"parent_detail_serializer_data": parent_detail_serializer.data})
                        else:
                            raise ValidationError(
                                parent_detail_serializer.errors)

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
            # pdb.set_trace()
            academic_session_detail = {
                "child": 3,
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
            
                    # self.context.update({"child_plan_serializer_data":child_plan_serializer.data})

                else:
                    raise ValidationError(child_plan_serializer.errors)
            except Exception as ex:
                logger.debug(ex)
                logger.info(ex)
                raise ValidationError(ex)
            return child
            """ create block """
            try: 
                academic_session= AcademicSession.objects.get(id=acad_session,
                                                         grade=grade, section=section, class_teacher=class_teacher)
                
                start_date = academic_session.session_from
                end_date = academic_session.session_till
                """ calculate working days """
                working_days = calculate_working_days(start_date,end_date)
                print("working_days--->", working_days)

                """ calculate blocks"""
                blocks = calculate_blocks(working_days)

                print("Blocks", blocks)
                for block in range(1,blocks+1):
                    print("@@@@@@@@", block)

                    block_detail = {
                        "block_no": "Block" + " " + str(block),
                        "child_plan": child_plan_serializer.data['id'],
                        "activity": random_activity(academic_session)
                    }

                    print("$$$$$",block_detail)

                    blockCreateSerializer = BlockCreateSerializer(data=block_detail)

                    if blockCreateSerializer.is_valid():
                        blockCreateSerializer.save()
                        
                    else:
                        raise ValidationError(BlockCreateSerializer.errors)
            
            except Exception as ex:
                print("$$$$$$$$$",ex)
                logger.debug(ex)
                raise ValidationError(ex)

        except Exception as ex:
            print("@#######",ex)
            logger.info(ex)
            logger.debug(ex)
            raise ValidationError(ex)


""" Child List Serializer """


class ChildListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'
        depth = 1
    

    def to_representation(self, obj):
        serialized_data = super(
            ChildListSerializer, self).to_representation(obj)
        # print("DATA----", serialized_data)
        child_id = serialized_data.get('id')
        print("ID---", child_id)
        
        child_id_qs = ChildPlan.objects.filter(child__id=child_id)
        if child_id_qs:
            child_id_serializer = ChildPlanSerializer(
                child_id_qs, many=True)
            serialized_data['academic_session_data'] = child_id_serializer.data
        return serialized_data




class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'
       


""" Child Detail list """


class ChildDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildDetail
        fields = '__all__'
        depth = 2


""" Child Create Serializer """


class ChildDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildDetail
        fields = '__all__'


""" Attendance Create Serializer """


class AttendanceCreateSerializer(serializers.ModelSerializer):
    # childs = serializers.JSONField(required=False)
    class Meta:
        model = Attendance
        fields = '__all__'


""" Attendance List Serializer """


class AttendanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        depth = 1

