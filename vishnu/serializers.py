from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

###############################################
##              Register Users              ##
###############################################

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'email', 'password') # Automatic validation of email
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        '''
        Check that only certain domains are allowed to register
        '''

        email = data['email']
        domain = email.split('@')[1]
        domain_list = ["gmail.com", "nus.edu.sg",]
        if domain not in domain_list:
            raise serializers.ValidationError("Please enter an Email Address with a valid domain")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'],
                                        validated_data['email'],
                                        validated_data['password'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')

###############################################
##              Login Users                 ##
###############################################

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")