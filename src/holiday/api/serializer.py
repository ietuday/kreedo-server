from rest_framework import serializers
from holiday.models import*


""" School Holiday List Serializer """


class SchoolHolidayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolHoliday
        fields = '__all__'
        depth = 2


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
