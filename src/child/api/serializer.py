import traceback
from rest_framework import serializers
from child.models import*
from users.api.serializer import*
from session.api.serializer import*
from plan.api.serializer import*
from session.models import*
""" Child Create Serializer """


class ChildCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        # fields = ['photo', 'first_name', 'last_name', 'date_of_birth',
        #           'gender', 'date_of_joining', 'place_of_birth', 'blood_group']
        exclude = ['parent']

    # def to_representation(self, instance):
    #     try:
    #         instance = super(ChildCreateSerializer,
    #                          self).to_representation(instance)
    #         """ Update details in RESPONSE """
    #         instance['child_plan_data'] = self.context['child_plan_serializer']

    #         return instance
    #     except Exception as ex:
    #         print("error", ex)
    #         print("traceback", traceback.print_exc())

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

                    else:
                        raise ValidationError(parent_serializer.errors)

                except Exception as ex:

                    raise ValidationError(ex)

                parent_data = {
                    "user_obj": parent_serializer.data['id'],
                    "relationship_with_child": parent['relationship_with_child'],
                    "phone": parent['phone']

                }
            try:
                parent_detail_serializer = ParentDetailSerializer(
                    data=dict(parent_data))

                if parent_detail_serializer.is_valid():

                    parent_detail_serializer.save()
                    parent_id = parent_detail_serializer.data['user_obj']
                    parent_list.append(parent_id)

                else:
                    print(parent_detail_serializer.errors)
                    raise ValidationError(parent_detail_serializer.errors)
            except Exception as ex:
                print(ex)
                raise ValidationError(ex)

            validated_data['parent'] = parent_list

            child.parent.set(validated_data['parent'])

            child.save()
            return child
            acad_session = self.context['academic_session_detail']['academic_session']
            section = self.context['academic_session_detail']['section']
            grade = self.context['academic_session_detail']['grade']
            class_teacher = self.context['academic_session_detail']['class_teacher']

            acadmic_ids = AcademicSession.objects.filter(id=acad_session,
                                                         grade=grade, section=section, class_teacher=class_teacher).values('id')[0]['id']

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
                    print("Child plan---->", child_plan_serializer.data)
                    # self.context.update(
                    #     {"child_plan_serializer": child_plan_serializer.data})
                else:
                    print("Errors", child_plan_serializer.errors)
                    raise ValidationError(child_plan_serializer.errors)
            except Exception as ex:
                print("Child plan ", ex)
                raise ValidationError(ex)

        except Exception as ex:
            print("ex", ex)
            raise ValidationError(ex)


""" Child List Serializer """


class ChildListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'
        depth = 1


""" Child Detail list """


class ChildDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildDetail
        fields = '__all__'
        depth = 1


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
