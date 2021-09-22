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
from .utils import *

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
                period_template=period_template_id, day=week_name).order_by('start_time', 'end_time')
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

    def to_representation(self, instance):
        instance = super(PeriodListSerializer,
                         self).to_representation(instance)
        start_time = get_seconds_removed(instance['start_time'])
        end_time = get_seconds_removed(instance['end_time'])
        instance['start_time'] = start_time
        instance['end_time'] = end_time
        return instance


class PeriodListSerializerWeb(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['id', 'name', 'type', 'start_time', 'end_time',
                  'room', 'subject', 'period_template_detail']
        depth = 1

    def to_representation(self, instance):
        instance = super(PeriodListSerializerWeb,
                         self).to_representation(instance)
        start_time = get_seconds_removed(instance['start_time'])
        end_time = get_seconds_removed(instance['end_time'])
        instance['start_time'] = start_time
        instance['end_time'] = end_time
        return instance


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
                dict['room'] = class_period.room.room_no
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
            print("validated_data", validated_data)
            p_qs = Period.objects.filter(start_date=validated_data['start_date'], end_date=validated_data['end_date'],
                                         start_time=validated_data['start_time'], end_time=validated_data['end_time']).count()
            if p_qs == 0:
                data = super(PeriodCreateSerializer,
                             self).create(validated_data)
                return data
            else:
                print("ALready Created")
                return ValidationError("Alreday Created")

        except Exception as ex:
            print("@@@@@", traceback.print_exc())
            print("ERROR", ex)
            # raise ValidationError(ex)


""" Period Template Detail List Serializer """


class PeriodTemplateDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateDetail
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        instance = super(PeriodTemplateDetailListSerializer,
                         self).to_representation(instance)
        start_time = get_seconds_removed(instance['start_time'])
        end_time = get_seconds_removed(instance['end_time'])
        instance['start_time'] = start_time
        instance['end_time'] = end_time
        return instance


""" Period Template Detail Create Serializer """


class PeriodTemplateDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateDetail
        fields = '__all__'

    def validate(self, validated_data):
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']
        # period_temp_qs = PeriodTemplateDetail.objects.filter(
        #                 Q(start_time__lte=start_time,start_time__lt=end_time) ,
        #                 # Q(end_time__gt=start_time,end_time__lt=end_time) ,
        #                 # Q(start_time__gte=start_time,end_time__gt=end_time),
        #                 room=validated_data['room'],
        #                 day=validated_data['day'],
        #                 period_template = validated_data['period_template']

        #
        #  )
        period_temp_qs = PeriodTemplateDetail.objects.filter(
            room=validated_data['room'],
            day=validated_data['day'],
            period_template=validated_data['period_template']
        ).exclude(
            Q(end_time__lte=start_time) |
            Q(start_time__gte=end_time)

        )
        print(period_temp_qs)

        # pdb.set_trace()
        # # period_temp_qs = []
        if period_temp_qs:
            raise ValidationError("Period With This Time Exists")
        else:
            return validated_data


""" period template detail update serialzer"""


class PeriodTemplateDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateDetail
        fields = '__all__'

    def validate(self, validated_data):
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']
        instance = self.instance
        if (instance.start_time != start_time and instance.end_time != end_time) or (instance.end_time != end_time) or (instance.start_time != start_time):
            period_temp_qs = PeriodTemplateDetail.objects.filter(
                room=validated_data['room'],
                day=validated_data['day'],
                period_template=validated_data['period_template']
            ).exclude(
                Q(end_time__lte=start_time) |
                Q(start_time__gte=end_time)
            )

        print("Serializer", period_temp_qs)
        # pdb.set_trace()
        # # period_temp_qs = []
        if period_temp_qs:
            raise ValidationError("Period With This Time Exists")
        else:
            return validated_data


class UpdatePeriodTemplateSerializer(serializers.ModelSerializer):
    # validation_time = serializers.Field()

    class Meta:
        model = PeriodTemplateDetail
        fields = '__all__'

    def to_representation(self, instance):
        instance = super(UpdatePeriodTemplateSerializer,
                         self).to_representation(instance)
        print("@@@@@@@@@ to representation", self.context)
        if 'validation_error' in self.context:
            instance['validation_error'] = self.context['validation_error']
        return instance

    def update(self, instance, validated_data):

        try:
            start_time = validated_data['start_time']
            end_time = validated_data['end_time']

            instance = self.instance
            print("start time", start_time)
            print("end time", end_time)
            print("instance.end_time > end_time------",
                  instance.end_time > end_time)
            print("instance.start_time < start_time",
                  instance.start_time < start_time)
            record_avl = PeriodTemplateDetail.objects.filter(start_time=start_time,
                                                             end_time=end_time,
                                                             room=validated_data['room'],
                                                             day=validated_data['day'],
                                                             period_template=validated_data['period_template'])
            if record_avl:
                period_template_qs = PeriodTemplateDetail.objects.filter(
                    pk=instance.pk).update(**validated_data)
                print("Update")
                return instance
            else:
                record_avl = PeriodTemplateDetail.objects.filter(
                    ~Q(id=instance.pk),
                    room=validated_data['room'],
                    day=validated_data['day'],
                    period_template=validated_data['period_template']
                ).exclude(
                    Q(end_time__lte=start_time) |
                    Q(start_time__gte=end_time),

                )
                # record_avl_s = record_avl.exclude(instance)
                print("record_avl------------", record_avl)
                if record_avl:
                    validation_error = "Period already exists in this time"
                    self.context.update({"validation_error": validation_error})
                    return validated_data
                else:
                    period_template_qs = PeriodTemplateDetail.objects.filter(
                        pk=instance.pk).update(**validated_data)
                    print("Update")
                    return instance

        except Exception as ex:
            print("@@@@@@@@ SERIALIZER", ex)
            print("Traceback------>", traceback.print_exc())
            raise ValidationError(ex)


""" PeriodTemplateToGrade List Serializer """


class PeriodTemplateToGradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateToGrade
        fields = '__all__'
        depth = 2


class PeriodTemplateToGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateToGrade
        fields = '__all__'
        # depth = 2

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
        fields = ['academic_session', 'start_date',
                  'end_date', 'period_template', 'is_active']

    def validate(self, validated_data):
        print("validated_data", validated_data)
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        # record_aval = PeriodTemplateToGrade.objects.filter(
        #     academic_session=validated_data['academic_session'],
        #     period_template=validated_data['period_template'],
        # ).exclude(
        #     Q(end_date__lt=start_date) |
        #     Q(start_date__gt=end_date)
        # )
        # print("record_aval-----------", record_aval)
        # if record_aval:
        #     print("% EXIST")
        #     raise ValidationError("Already exist")
        # else:

        instance = super(PeriodTemplateToGradeCreateSerializer,
                         self).create(validated_data)
        print("instance------", instance)
        academic_session = instance.academic_session
        academic_session.period_template.add(instance.period_template)
        academic_session.is_applied = True
        academic_session.save()
        instance.save()
        return validated_data


class PeriodTemplateToGradeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateToGrade
        fields = '__all__'

    # def to_representation(self, instance):
    #     instance = super(PeriodTemplateToGradeUpdateSerializer,
    #                      self).to_representation(instance)
    #     print("@@@@@@@@@ to representation", self.context)
    #     if 'validation_error' in self.context:
    #         instance['validation_error'] = self.context['validation_error']
    #     return instance

    # def update(self, instance, validated_data):
    #     try:
    #         print("################3")
    #         # print("validated_data-----------", validated_data)
    #         # print("###############", self)

    #         start_date = validated_data['start_date']
    #         end_date = validated_data['end_date']
    #         instance = self.instance
    #         if (instance.start_date != start_date and instance.end_date != end_date) or (instance.end_date != end_date) or (instance.start_date != start_date):
    #             period_temp_qs = PeriodTemplateToGrade.objects.filter(~Q(id=instance.pk)).exclude(
    #                 Q(end_date__lte=start_date) |
    #                 Q(start_date__gte=end_date)
    #             )

    #         print("Serializer---->", period_temp_qs)

    #         if period_temp_qs:
    #             validation_error = "Time Exist"
    #             self.context.update({"validation_error": validation_error})
    #             return validated_data
    #         else:
    #             period_template_qs = PeriodTemplateToGrade.objects.filter(
    #                 pk=instance.pk).update(**validated_data)
    #             print("Update")
    #             return instance
    #             # return validated_data

    #     except Exception as ex:
    #         print("ERROR", ex)
    #         print("TRACEBACK", traceback.print_exc())
    #         return ValidationError(ex)


"""PeriodTemplateToGrade  for template listSerializer """


class PeriodTemplateForGradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTemplateToGrade
        fields = ['start_date', 'end_date', 'period_template']
        depth = 1
