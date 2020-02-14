from rest_framework import serializers
from django.contrib.auth import authenticate
from django.conf import settings
from .models import Entry, User

class EntrySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Entry
        fields = ["temperature", "lat", "long", "file", "owner", "date_created"]

    def validate_temperature(self, value):
        if value < 32 or value > 42:
            raise serializers.ValidationError("Please enter a humanly possible temperature \
                                               in Celcius (32 < T < 42)")
        return value

    def validate_lat(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Please enter valid coordinates: -90 < latitude < 90")
        return value

    def validate_long(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Please enter valid coordinates: -180 < longitude < 180")
        return value


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password') # Automatic validation of email
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        '''
        Check that only certain domains are allowed to register
        '''

        domain_list = getattr(settings, "DOMAIN_LIST", [])
        email = data['email']
        domain = email.split('@')[1]
        if domain_list is None:
            raise serializers.ValidationError("Please contact your administrators to create valid domain names")
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

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")
