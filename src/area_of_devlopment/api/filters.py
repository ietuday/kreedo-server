from area_of_devlopment.models import*
from django_filters import rest_framework as filters


""" Area of Devlopment Filter """


class AreaOfDevlopmentFilter(filters.FilterSet):
    class Meta:
        model = AreaOfDevlopment
        fields = '__all__'


""" Concept Filter """


class ConceptFilter(filters.FilterSet):
    class Meta:
        model = Concept
        fields = '__all__'


""" Skill Filter """


class SkillFilter(filters.FilterSet):
    class Meta:
        model = Skill
        fields = '__all__'
