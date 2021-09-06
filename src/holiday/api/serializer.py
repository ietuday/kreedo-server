from django.db.models.query_utils import Q
from rest_framework import serializers
from holiday.models import*
from django.core.exceptions import ValidationError

from plan.models import No

""" Holiday Type List Serializer """


class HolidayTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolidayType
        fields = '__all__'
        # depth = 2


""" School Holiday List Serializer """


class SchoolHolidayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolHoliday
        fields = '__all__'
        depth = 2


""" School Holiday  Serializer """


class SchoolHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolHoliday
        fields = '__all__'
        depth = 1


""" School Holiday create Serializer """


class SchoolHolidayCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolHoliday
        fields = '__all__'


""" Create School holiday serializer"""


class CreateSchoolHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolHoliday
        fields = '__all__'

    def validate(self, validated_data):
        try:

            holiday_from = validated_data['holiday_from']
            holiday_till = validated_data['holiday_till']
            school = validated_data.get('school', None)
            academic_calender = validated_data.get('academic_calender', None)
            academic_session = validated_data.get('academic_session', None)

            if school:
                record_aval = SchoolHoliday.objects.filter(
                    school=school,
                    title=validated_data['title']
                ).exclude(
                    Q(holiday_till__lt=holiday_from) |
                    Q(holiday_from__gt=holiday_till)
                )
                if record_aval:
                    raise ValidationError("Already exists")
                else:

                    return validated_data
            elif academic_calender:
                record_aval = SchoolHoliday.objects.filter(
                    academic_calender=academic_calender,
                    title=validated_data['title']
                ).exclude(
                    Q(holiday_till__lt=holiday_from) |
                    Q(holiday_from__gt=holiday_till)
                )
                print("record_aval@@", record_aval)
                # pdb.set_trace()
                if record_aval:
                    raise ValidationError("Already exists")
                else:

                    return validated_data
            else:
                record_aval = SchoolHoliday.objects.filter(
                    academic_session=academic_session,
                    title=validated_data['title']
                ).exclude(
                    Q(holiday_till__lt=holiday_from) |
                    Q(holiday_from__gt=holiday_till)
                )

                if record_aval:
                    raise ValidationError("Already exists")
                else:

                    return validated_data

        except Exception as ex:
            print("ex------------", ex)
            raise ValidationError(ex)


""" Create School holiday serializer"""


class UpdatedSchoolHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolHoliday
        fields = '__all__'

    def to_representation(self, instance):
        instance = super(UpdatedSchoolHolidaySerializer,
                         self).to_representation(instance)
        print("@@@@@@@@@ to representation", self.context)
        if 'validation_error' in self.context:
            instance['validation_error'] = self.context['validation_error']
        return instance

    def update(self, instance, validated_data):

        try:
            print("instance************8", instance)
            holiday_from = validated_data['holiday_from']
            holiday_till = validated_data['holiday_till']
            print("holiday_from--------", holiday_from)
            print("holiday_till------", holiday_till)
            school = validated_data.get('school', None)
            academic_calender = validated_data.get('academic_calender', None)
            academic_session = validated_data.get('academic_session', None)
            print("SCHOOL--------", school)
            print("academic_calender---------", academic_calender)
            instance = self.instance
            print("instance----->", instance.pk)
            if school is not None:
                print("SCHOOL")
                record_avl = SchoolHoliday.objects.filter(~Q(id=instance.pk), holiday_from=holiday_from,
                                                          holiday_till=holiday_till,
                                                          school=school,
                                                          title=validated_data['title'])
                print("record_avl", record_avl)
                if record_avl:
                    print("@@@@@@@@@")
                    validation_error = "Holiday already exists in this date"
                    self.context.update(
                        {"validation_error": validation_error})
                    return validated_data
                else:

                    period_template_qs = SchoolHoliday.objects.filter(
                        pk=instance.pk).update(**validated_data)
                    print("Update")
                    return instance
            elif academic_calender is not None:
                print("academic_calender")
                record_avl = SchoolHoliday.objects.filter(
                    ~Q(id=instance.pk),
                    academic_calender=academic_calender,
                    title=validated_data['title']
                ).exclude(
                    Q(holiday_till__lte=holiday_from) |
                    Q(holiday_from__gte=holiday_till),

                )

                print("2 record_avl", record_avl)
                if record_avl:
                    print("@@@@@@@@@")
                    validation_error = "Holiday already exists in this date"
                    self.context.update(
                        {"validation_error": validation_error})
                    return validated_data
                else:

                    period_template_qs = SchoolHoliday.objects.filter(
                        pk=instance.pk).update(**validated_data)
                    print("Update")
                    return instance
            elif academic_session:
                print("academic_session", academic_session)
                record_avl = SchoolHoliday.objects.filter(
                    ~Q(id=instance.pk),
                    academic_session=academic_session,
                    title=validated_data['title']
                ).exclude(
                    Q(holiday_till__lte=holiday_from) |
                    Q(holiday_from__gte=holiday_till),

                )
                print(" academic_session record_avl", record_avl)

                if record_avl:
                    print("@@@@@@@@@")
                    validation_error = "Holiday already exists in this date"
                    self.context.update(
                        {"validation_error": validation_error})
                    return validated_data
                else:

                    period_template_qs = SchoolHoliday.objects.filter(
                        pk=instance.pk).update(**validated_data)
                    print("Update")
                    return instance

        except Exception as ex:
            print("ex------------", ex)
            raise ValidationError(ex)


class DownloadSchoolHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolHoliday
        fields = '__all__'


""" School Weak Off List Serailizer """


class SchoolWeakOffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolWeakOff
        fields = '__all__'
        depth = 1


""" School Weak Off Create Serailizer """


class SchoolWeakOffCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolWeakOff
        fields = '__all__'


""" Calendar serializer """


# class CalendarSerializer(serializers.ModelSerializer):
#     pass
#     # class Meta:
#     #     # model = SchoolHoliday
#     #     fields = '__all__'

#     def create(self, validated_data):
#         print("Self", self)
