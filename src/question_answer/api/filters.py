from django_filters import rest_framework as filters
from question_answer.models import*

""" Question Answer filter """

class QuestionAnswerFilter(filters.FilterSet):
    question = filters.CharFilter(field_name='question', lookup_expr='icontains')
    answer = filters.CharFilter(
        field_name='answer', lookup_expr='icontains')
   
    class Meta:
        model = QuestionAnswer
        fields = '__all__'


