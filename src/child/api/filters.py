from django_filters import rest_framework as filters
from child.models import*

# """ Child Filter """


# class ChildFilter(filters.FilterSet):
#     class Meta:
#         model = 'Child'
#         fields = '__all__'


""" Activity filter """


class ChildFilter(filters.FilterSet):
    class Meta:
        model = Child
        fields = '__all__'


# """ Child Detail Filter """


# class ChildDetailFilter(filters.FilterSet):
#     class Meta:
#         model = ChildDetail
#         fields = '__all__'


"""  Attendance filter """


# class AttendanceFilter(filters.FilterSet):
#     class Meta:
#         model = Attendance
#         fields = '__all__'
