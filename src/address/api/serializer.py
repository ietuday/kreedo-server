from rest_framework import serializers
from ..models import*


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    def create(self, validated_data):
        try:
            print("Called", validated_data)
            return Address.objects.create(**validated_data)

        except Exception as ex:
            raise serializers.ValidationError("Error", ex)
