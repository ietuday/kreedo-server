import traceback
from rest_framework import serializers
from period.models import*
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import ValidationError
from activity.models import*
from ..models import*
from session.models import*
from holiday.models import *
from holiday.api.serializer import *
from django.db.models import Q

""" Period Template Serializer """


class PeriodTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplate
        fields = '__all__'
    

class PeriodTemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplate
        fields = ['id', 'name']

    def to_representation(self, obj):
        serialized_data = super(
            PeriodTemplateListSerializer, self).to_representation(obj)

        period_template_id = serialized_data.get('id')
        week_list = ['MONDAY', 'TUESDAY', 'WEDNESDAY',
                     'THURSDAY', 'FRIDAY', 'SATURDAY']
        period_details = []
        for week_name in week_list:
            week_dict = {}
            week_dict['name'] = week_name
            period_template_detail_qs = PeriodTemplateDetail.objects.filter(
                period_template=period_template_id, day=week_name)
            period_template_detail_serializer = PeriodTemplateDetailListSerializer(
                period_template_detail_qs, many=True)
            week_dict['periods'] = period_template_detail_serializer.data
            period_details.append(week_dict)
        serialized_data['period_template_details'] = period_details
        return serialized_data


""" Period List Serializer """


class PeriodListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'
        depth = 2


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

            return instance
        except Exception as ex:
            raise ValidationError(ex)

    def create(self, validated_data):
        try:
            teacher = self.context['data_dict']['teacher'][0]

            period_list_qs = Period.objects.filter(
                teacher=teacher, start_date=validated_data['start_date'])

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
        try:
            p_qs = Period.objects.filter(start_date=validated_data['start_date'], end_date=validated_data['end_date'],
                                     start_time=validated_data['start_time'], end_time=validated_data['end_time']).count()
            if p_qs == 0:
                data = super(PeriodCreateSerializer, self).create(validated_data)
                return data
            else:
                print("ALready Created")
                return ValidationError("Alreday Created")


        except Exception as ex:
            print("ERROR", ex)
            print("@@@@@", traceback.print_exc())
            raise ValidationError(ex)

        
""" Period Template Detail List Serializer """


class PeriodTemplateDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateDetail
        fields = '__all__'
        depth = 1
    
    def to_representation(self, instance):
        instance = super(PeriodTemplateDetailListSerializer,
                                                self).to_representation(instance)
        start_time = instance['start_time']
        end_time = instance['end_time']
        strt_time_list = start_time.split(':')
        formated_strt_time = ":".join(strt_time_list[0:2])
        end_time_list = end_time.split(':')
        formated_end_time = ":".join(end_time_list[:2])
        instance['start_time'] = formated_strt_time
        instance['end_time'] = formated_end_time
        return instance


""" Period Template Detail Create Serializer """


class PeriodTemplateDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateDetail
        fields = '__all__'
    
    def validate(self,validated_data):
            start_time = validated_data['start_time']
            end_time = validated_data['end_time']
            # period_temp_qs = PeriodTemplateDetail.objects.filter( 
            #                                               Q(Q(end_time__range=(start_time,end_time) | Q(end_time__gt=end_time),start_time__gte=start_time) |
            #                                               Q(Q(end_time__gt=start_time) | Q(end_time__gt=end_time) | Q(end_time__range=(start_time,end_time)),start_time__lt=start_time),
            #                                                 # start_time__gte=start_time,
            #                                                         room=validated_data['room'],
            #                                                        day=validated_data['day'],
                                                                       
            #                                             )
           
            period_temp_qs = []
            if period_temp_qs:
                raise ValidationError("Period With This Time Exists")
            else:
                # data = super(PeriodTemplateDetailCreateSerializer, self).create(validated_data)
                return validated_data
    
    


""" PeriodTemplateToGrade List Serializer """


class PeriodTemplateToGradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateToGrade
        fields = '__all__'
        depth = 2

    
    # def to_representation(self, instance):
    #     instance = super(PeriodTemplateToGradeListSerializer,
    #                          self).to_representation(instance)

    #     start_date = instance['start_date']
    #     end_date = instance['end_date']
    #     academic_session = instance['academic_session']['id']
    #     calendar_data = SchoolHoliday.objects.filter(academic_session=academic_session,
    #     holiday_from__gte=start_date, holiday_till__gte=end_date, is_active=True)
    #     print("Calendar", calendar_data)
    #     calendar_data_qs = SchoolHolidayListSerializer(calendar_data, many=True)
    #     instance['holidays_list'] = calendar_data_qs.data
    #     return instance


""" PeriodTemplateToGrade Create Serializer """


class PeriodTemplateToGradeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateToGrade
        fields = '__all__'

    def validate(self,validated_data):
        instance = super(PeriodTemplateToGradeCreateSerializer,self).create(validated_data)
        academic_session = instance.academic_session
        academic_session.period_template = instance.period_template
        academic_session.is_applied = True
        academic_session.save()
        instance.save()
        return instance
