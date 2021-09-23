from activity.models import ActivityComplete
import traceback
from rest_framework import serializers
from child.models import*
from plan.models import*
from users.api.serializer import*
from session.api.serializer import*
from plan.api.serializer import*

from session.models import*
from .utils import*
import logging
from kreedo.conf.logger import*
import pdb
from users.models import*
from child.api.utils import get_range_of_days_in_session

""" Create Log for Serializer"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('scheduler.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)


class ChildPlanCreateSerailizer(serializers.ModelSerializer):
    class Meta:
        model = ChildPlan
        fields = ['child', 'academic_session',
                   'curriculum_start_date']


class ChildPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildPlan
        fields = ['academic_session']
        depth = 2


class ChildPlanOfChildSerializer(serializers.ModelSerializer):
    academic_session = AcademicSessionListForChildSerializer()

    class Meta:
        model = ChildPlan
        fields = '__all__'
        # depth = 1


class ChildPlanOfSubjectChildSerializer(serializers.ModelSerializer):
    # academic_session = AcademicSessionListForChildSerializer()

    class Meta:
        model = ChildPlan
        fields = ['subjects']
        depth = 1


""" block Create Serailizer """


class BlockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = '__all__'


""" Child Create Serializer """


# class ChildCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Child
#         # exclude = ['parent']
#         fields = '__all__'

#     # def to_representation(self, instance):
#     #     try:
#     #         instance = super(ChildCreateSerializer,
#     #                          self).to_representation(instance)
#     #         """ Update details in RESPONSE """
#     #         instance['parent_data'] = self.context['parent_detail_serializer_data']
#     #         instance['child_plan_data'] = self.context['child_plan_serializer']

#     #         return instance
#     #     except Exception as ex:
#     #         print("error", ex)
#     #         print("traceback", traceback.print_exc())
#     #         logger.debug(ex)
#     #         raise ValidationError(ex)

#     def create(self, validated_data):
#         try:

#             validated_data = self.context['child_detail']
#             print("validated_data", validated_data)
#             child = super(ChildCreateSerializer, self).create(validated_data)

#             parents_detail = self.context['parent_detail']['parents']

#             parent_list = []
#             for parent in parents_detail:

#                 try:

#                     parent_serializer = ParentSerializer(data=dict(parent))
#                     if parent_serializer.is_valid():
#                         parent_serializer.save()
#                         parent_data = {
#                             "user_obj": parent_serializer.data['id'],
#                             "relationship_with_child": parent['relationship_with_child'],
#                             "phone": parent['phone'],
#                             "gender": parent['gender'],
#                             "photo": parent['photo']

#                         }
#                         parent_detail_serializer = ParentDetailSerializer(
#                             data=dict(parent_data))

#                         if parent_detail_serializer.is_valid():

#                             parent_detail_serializer.save()

#                             parent_id = parent_detail_serializer.data['user_obj']
#                             parent_list.append(parent_id)

#                             # self.context.update({"parent_detail_serializer_data": parent_detail_serializer.data})
#                         else:
#                             raise ValidationError(
#                                 parent_detail_serializer.errors)

#                     else:
#                         raise ValidationError(parent_serializer.errors)

#                 except Exception as ex:
#                     logger.debug(ex)
#                     logger.info(ex)

#                     raise ValidationError(ex)

#             validated_data['parent'] = parent_list

#             child.parent.set(validated_data['parent'])

#             child.save()

#             acad_session = self.context['academic_session_detail']['academic_session']
#             section = self.context['academic_session_detail']['section']
#             grade = self.context['academic_session_detail']['grade']
#             class_teacher = self.context['academic_session_detail']['class_teacher']

#             acadmic_ids = AcademicSession.objects.filter(id=acad_session,
#                                                          grade=grade, section=section, class_teacher=class_teacher).values('id')[0]['id']

#             child_id = child.id
#             academic_session_detail = {
#                 "child": child_id,
#                 "academic_session": acadmic_ids,
#                 "subjects": self.context['academic_session_detail']['subjects'],
#                 "curriculum_start_date": self.context['academic_session_detail']['curriculum_start_date']
#             }
#             """  create child plan """
#             try:

#                 child_plan_serializer = ChildPlanCreateSerailizer(
#                     data=dict(academic_session_detail))
#                 if child_plan_serializer.is_valid():
#                     child_plan_serializer.save()

#                     # self.context.update({"child_plan_serializer_data":child_plan_serializer.data})

#                 else:
#                     raise ValidationError(child_plan_serializer.errors)
#             except Exception as ex:
#                 logger.debug(ex)
#                 logger.info(ex)
#                 raise ValidationError(ex)
#             return child
#             """ create block """
#             try:
#                 academic_session = AcademicSession.objects.get(id=acad_session,
#                                                                grade=grade, section=section, class_teacher=class_teacher)

#                 start_date = academic_session.session_from
#                 end_date = academic_session.session_till
#                 """ calculate working days """
#                 working_days = calculate_working_days(start_date, end_date)

#                 """ calculate blocks"""
#                 blocks = calculate_blocks(working_days)

#                 for block in range(1, blocks+1):

#                     block_detail = {
#                         "block_no": "Block" + " " + str(block),
#                         "child_plan": child_plan_serializer.data['id'],
#                         "activity": random_activity(academic_session)
#                     }

#                     blockCreateSerializer = BlockCreateSerializer(
#                         data=block_detail)

#                     if blockCreateSerializer.is_valid():
#                         blockCreateSerializer.save()

#                     else:
#                         raise ValidationError(BlockCreateSerializer.errors)

#             except Exception as ex:
#                 print("$$$$$$$$$", ex)
#                 logger.debug(ex)
#                 raise ValidationError(ex)

#         except Exception as ex:
#             print("@#######", ex)
#             logger.info(ex)
#             logger.debug(ex)
#             raise ValidationError(ex)


class ChildListForPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'


""" Child List Serializer """


class ChildListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'
        depth = 2

    def to_representation(self, obj):
        serialized_data = super(
            ChildListSerializer, self).to_representation(obj)
        child_id = serialized_data.get('id')

        child_id_qs = ChildPlan.objects.filter(child__id=child_id)
        print("child_id_qschild_id_qschild_id_qschild_id_qs", child_id_qs)
        if child_id_qs:
            child_id_serializer = ChildPlanSerializer(
                child_id_qs, many=True)
            serialized_data['academic_session_data'] = child_id_serializer.data
        return serialized_data


class ChildUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        fields = '__all__'


class ChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        fields = '__all__'
        # depth= 2

    def to_representation(self, obj):
        try:
            serialized_data = super(
                ChildSerializer, self).to_representation(obj)

            child_id = serialized_data.get('id')

            parent_list = serialized_data.get('parent')

            print("$$$$$$$$$$", parent_list)
            user_qs = UserDetail.objects.filter(
                user_obj__in=parent_list).order_by('user_obj')
            user_qs_serializer = UserDetailListSerializer(user_qs, many=True)

            serialized_data['parents'] = user_qs_serializer.data

            child_id_qs = ChildPlan.objects.filter(child=child_id)
            if child_id_qs:
                print("child_id_qs----", child_id_qs)
                child_id_serializer = ChildPlanOfChildSerializer(
                    child_id_qs, many=True)
                serialized_data['academic_session_data'] = child_id_serializer.data

            else:
                serialized_data['academic_session_data'] = ""
            """ Subject Population"""
            child_subject_id_qs = ChildPlan.objects.filter(child=child_id)[0]
            if child_subject_id_qs:
                child_subject_serializer = ChildPlanOfSubjectChildSerializer(
                    child_subject_id_qs)
                print("child_subject_serializer.data----------->",
                      child_subject_serializer.data['subjects'])

                serialized_data['subject_list'] = child_subject_serializer.data['subjects']

            else:
                serialized_data['subject_list'] = ""

            child_session_qs = ChildSession.objects.filter(child=child_id)
            if child_session_qs:
                child_session_serializer = ChildSessionListSerializer(
                    child_session_qs, many=True)
                serialized_data['session_details'] = child_session_serializer.data
            else:
                serialized_data['session_details'] = ""

            return serialized_data
        except Exception as ex:
            print("ERROR@@@@@@@@@@@", ex)
            print("TRACEBACK-------------->", traceback.print_exc())


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


""" ChildSession List Serializer """


class ChildSessionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildSession
        fields = '__all__'
        depth = 2


""" ChildSession Create Serializer """


class ChildSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildSession
        fields = '__all__'


""" Attendance Create Serializer """


class AttendanceCreateSerializer(serializers.ModelSerializer):
    # childs = serializers.JSONField(required=False)
    class Meta:
        model = Attendance
        fields = '__all__'


class AttendanceChildSerializer(serializers.ModelSerializer):
    # childs = serializers.JSONField(required=False)
    class Meta:
        model = Attendance
        fields = '__all__'

    def to_representation(self, obj):

        serialized_data = super(
            AttendanceChildSerializer, self).to_representation(obj)
        print("serialized_data['childs']", serialized_data['childs'])

        for i in serialized_data['childs']:
            # i['activity_behind'] = 0
            print("=== i", i['child_id'])
            child_activity_count = ActivityComplete.objects.filter(
                child__id=i['child_id'], is_completed=False).count()
            i['activity_behind'] = child_activity_count if child_activity_count else 0
        return serialized_data


""" Attendance List Serializer """


class AttendanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        depth = 1

    def to_representation(self, obj):
        try:
            serialized_data = super(
                AttendanceListSerializer, self).to_representation(obj)
            print("serialized_data['childs']", serialized_data['childs'])
            for child in serialized_data['childs']:

                if ActivityComplete.objects.filter(child=child['child_id'], period=self.context['period_detail']['period'],
                                                   activity=self.context['period_detail']['activity']).exists():
                    activity_qs = ActivityComplete.objects.filter(child=child['child_id'], period=self.context['period_detail']['period'],
                                                                  activity=self.context['period_detail']['activity'])
                    if len(activity_qs) != 0:
                        child['is_completed'] = activity_qs[0].is_completed
                    else:
                        child['is_completed'] = False
                else:
                    child['is_completed'] = False

            return serialized_data

        except Exception as ex:
            print("ERROR", ex)
            print("traceback------", traceback.print_exc())


class ChildParentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        exclude = ['parent']

    def create(self, validated_data):
        try:
            print("validated_data", validated_data, ChildPlanCreateSerailizer)
            # return Child.objects.create(**validated_data)
            registered_by = validated_data.pop('registered_by')
            school = validated_data.pop('school')
            print("validated_data", validated_data)
            
            child_instance = Child.objects.create(**validated_data)
            child_instance.registered_by = registered_by
            child_instance.school = school
            child_instance.save()
            # return child_instance
        
            parents_detail = self.context['parent_detail']['parents']

            parent_list = []
            for parent in parents_detail:

                try:

                    parent_serializer = ParentSerializer(data=dict(parent))
                    if parent_serializer.is_valid():
                        parent_serializer.save()
                        role_id = Role.objects.filter(
                            name="Parent")[0].id
                        type_id = UserType.objects.filter(
                            name='School Users-Parent')[0].id
                       
                        parent_data = {
                            "user_obj": parent_serializer.data['id'],
                            "relationship_with_child": parent['relationship_with_child'],
                            "phone": parent['phone'],
                            "gender": parent['gender'],
                            "photo": parent['photo'],
                            "role": [role_id],
                            "type": type_id

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
            
            child_instance.parent.set(validated_data['parent'])

            child_instance.save()

            acad_session = self.context['academic_session_detail']['academic_session']
            section = self.context['academic_session_detail']['section']
            grade = self.context['academic_session_detail']['grade']
            class_teacher = self.context['academic_session_detail']['class_teacher']
            acadmic_ids = AcademicSession.objects.filter(academic_calender=acad_session,
                                                         grade=grade, section=section, class_teacher=class_teacher)

            #  .values('id')[0]['id']
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", acadmic_ids)
            if acadmic_ids:
                print(
                    "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", acadmic_ids)
                child_id = child_instance.id
                academic_session_detail = {
                    "child": child_id,
                    "academic_session": acadmic_ids[0].id,
                    # "subjects": self.context['academic_session_detail']['subjects'],
                    "curriculum_start_date": self.context['academic_session_detail']['curriculum_start_date'],
                    "kreedo_previous_session": self.context['academic_session_detail']['kreedo_previous_session'],
                    "is_active": True
                }

                start_date = academic_session_detail['curriculum_start_date']
                range_of_working_days = get_range_of_days_in_session(start_date,acadmic_ids[0])
                subject_list =  self.context['academic_session_detail']['subjects']
                """  create child plan """
                try:
                    child_plan_serializer = ChildPlanCreateSerailizer(
                        data=dict(academic_session_detail))
                    if child_plan_serializer.is_valid():
                        child_plan_serializer.save()
        
                        child_plan = child_instance.child_plan.all()[0]
                        acad_session_qs = AcademicCalender.objects.filter(
                            id=acad_session)
                       
                        subject_plan = get_subject_plan(subject_list,child_instance,range_of_working_days)
                        
                        child_plan.subject_plan.set(subject_plan)
                        child_plan.save()
                        child_session = [
                            {
                                "child": child_id,
                                "session_name": acad_session_qs[0].session_name,
                                "session_type": "Individual",
                                "academic_session": acadmic_ids[0].id,
                                "start_date": acad_session_qs[0].start_date,
                                "end_date": acad_session_qs[0].end_date,
                                "is_active": True
                            },
                            {
                                "child": child_id,
                                "session_name": acad_session_qs[0].session_name,
                                "session_type": "Group",
                                "academic_session": acadmic_ids[0].id,
                                "start_date": acad_session_qs[0].start_date,
                                "end_date": acad_session_qs[0].end_date,
                                "is_active": True
                            }
                        ]

                        child_session_serilizer = ChildSessionCreateSerializer(
                            data=child_session, many=True)
                        if child_session_serilizer.is_valid():
                            child_session_serilizer.save()
                            print(child_session_serilizer.data)
                        else:
                            print(child_session_serilizer.errors)
                    else:
                        raise ValidationError(child_plan_serializer.errors)
                except Exception as ex:
                    logger.debug(ex)
                    logger.info(ex)
                    raise ValidationError(ex)
                return child_instance
                """ create block """
                try:
                    academic_session = AcademicSession.objects.get(id=acad_session,
                                                                   grade=grade, section=section, class_teacher=class_teacher)

                    start_date = academic_session.session_from
                    end_date = academic_session.session_till
                    """ calculate working days """
                    working_days = calculate_working_days(start_date, end_date)

                    """ calculate blocks"""
                    blocks = calculate_blocks(working_days)

                    for block in range(1, blocks+1):

                        block_detail = {
                            "block_no": "Block" + " " + str(block),
                            "child_plan": child_plan_serializer.data['id'],
                            "activity": random_activity(academic_session)
                        }

                        blockCreateSerializer = BlockCreateSerializer(
                            data=block_detail)

                        if blockCreateSerializer.is_valid():
                            blockCreateSerializer.save()

                        else:
                            raise ValidationError(BlockCreateSerializer.errors)

                except Exception as ex:
                    print("$$$$$$$$$", ex)
                    logger.debug(ex)
                    raise ValidationError(ex)

            return child_instance
        except Exception as ex:
            print("@#######", ex)
            logger.info(ex)
            logger.debug(ex)
            raise ValidationError(ex)
