import traceback
from rest_framework import serializers
from child.models import*
from users.api.serializer import*

""" Child Create Serializer """


class ChildCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        # fields = ['photo', 'first_name', 'last_name', 'date_of_birth',
        #           'gender', 'date_of_joining', 'place_of_birth', 'blood_group']
        exclude = ['parent']

    def create(self, validated_data):
        try:

            validated_data = self.context['child_detail']
            print("Validated@@@@@ ", validated_data)
            child = super(ChildCreateSerializer, self).create(validated_data)
            print("Child---->", child)

            parents_detail = self.context['parent_detail']['parents']

            for parent in parents_detail:
                print("parent------>", parent['relationship_with_child'])

                try:

                    parent_serializer = ParentSerializer(data=dict(parent))
                    if parent_serializer.is_valid():
                        parent_serializer.save()

                        print("Serailizer called   ", parent_serializer.data)
                    else:
                        print("Serialzier-------->", parent_serializer.errors)

                except Exception as ex:
                    print("errpr", ex)

                parent_data = {
                    "user_obj": parent_serializer.data['id'],
                    "relationship_with_child": parent['relationship_with_child'],
                    "phone": parent['phone']

                }
                print("!!!!!!!!!!!!!1111", parent_data)
                try:
                    parent_detail_serializer = ParentDetailSerializer(
                        data=dict(parent_data))
                    if parent_detail_serializer.is_valid():
                        parent_detail_serializer.save()
                    else:
                        print(parent_detail_serializer.errors)
                except expression as identifier:
                    pass

        except Exception as ex:
            print("ex", ex)


""" Child List Serializer """


class ChildListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'
        depth = 1


""" Attendance Create Serializer """


class AttendanceCreateSerializer(serializers.ModelSerializer):
    # childs = serializers.JSONField(required=False)
    class Meta:
        model = Attendance
        fields = '__all__'


""" Attendance List Serializer """


class AttendanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        depth = 1
