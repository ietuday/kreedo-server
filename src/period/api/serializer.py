import traceback
from rest_framework import serializers
from period.models import*
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import ValidationError
from activity.models import*
from ..models import*
from session.models import*
""" Period Template Serializer """


class PeriodTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplate
        fields = '__all__'


""" Period List Serializer """


class PeriodListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'
        depth = 1



""" Period  Serializer """


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'
        
        
""" getting classes according to teacher """


class ClassAccordingToTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['start_date']

    def to_representation(self, instance):
        try:

            instance = super(ClassAccordingToTeacherSerializer,
                             self).to_representation(instance)
            instance['data_list'] = self.context['data_list']
            print("INSTANCE@@@@@@@@@@@@@@@", instance)

            return instance
        except Exception as ex:
            raise ValidationError(ex)

    def create(self, validated_data):
        try:
            teacher = self.context['data_dict']['teacher'][0]
            print("TEACHER", teacher)

            period_list_qs = Period.objects.filter(
                teacher=teacher, start_date=validated_data['start_date'])
            print("##############", period_list_qs)

            periods_lists = []
            dict = {}
            for class_period in period_list_qs:
                dict['id'] = class_period.id
                dict['room_no'] = class_period.room_no.room_no
                dict['start_time'] = class_period.start_time
                dict['end_time'] = class_period.end_time
                dict['grade'] = class_period.academic_session.all()
                activity_missed = GroupActivityMissed.objects.filter(
                    period=class_period.id).count()
                dict['activity_behind'] = activity_missed
                periods_lists.append(dict)
                print("periods_lists----------->", periods_lists)
                dict = {}
            self.context.update({"data_list": periods_lists})
            return periods_lists

        except Exception as ex:
            print("ERROR", ex)
            print("@@@@@", traceback.print_exc())
            raise ValidationError(ex)


""" Period Create Serializer """


class PeriodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'

    def create(self, validated_data):
        p_qs = Period.objects.filter(start_date=validated_data['start_date'], end_date=validated_data['end_date'],
                                     start_time=validated_data['start_time'], end_time=validated_data['end_time']).count()
        if p_qs == 0:
            data = super(PeriodCreateSerializer, self).create(validated_data)
            return data
        else:
            print("ALready Created")
            return validated_data


""" Period Template Detail List Serializer """


class PeriodTemplateDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateDetail
        fields = '__all__'
        depth = 1


""" Period Template Detail Create Serializer """


class PeriodTemplateDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateDetail
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=PeriodTemplateDetail.objects.all(),
                fields=['room', 'start_time', 'end_time']
            )
        ]



""" PeriodTemplateToGrade List Serializer """
class PeriodTemplateToGradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateToGrade
        fields = '__all__'
        depth = 1



""" PeriodTemplateToGrade Create Serializer """
class PeriodTemplateToGradeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateToGrade
        fields = '__all__'