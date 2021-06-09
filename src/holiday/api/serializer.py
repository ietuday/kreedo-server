from rest_framework import serializers
from holiday.models import*


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
