from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    ValidationError)
from ..models import*



""" Question answer Serializer """

class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = '__all__'
        depth = 1


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ['id','question','is_active']


""" Question answer Serializer """

class GetSecretQuestionBasedOnParentIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ['id','question','is_active','created_at','updated_at']

    def to_representation(self, obj):
        serialized_data = super(
            GetSecretQuestionBasedOnParentIDSerializer, self).to_representation(obj)
        
        serialized_data['parent_id'] = self.context['user_detail']['user']
        serialized_data['email_id'] = self.context['user_detail']['email']
        return serialized_data






        