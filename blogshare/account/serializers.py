from rest_framework import serializers
from .models import MyUser
from django.contrib.auth import get_user_model


class CreateUserSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password', 'contact')
        extra_kwargs={
            'password':{
                'write_only':True,
                'style':{'input_type':'password'}
            }
        }

    def create(self, validated_data):
        user=get_user_model().objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            contact=validated_data['contact'],
            password=validated_data['password']
        )
        return user

class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=('first_name', 'last_name', 'contact', 'discription', 'dob')

class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
