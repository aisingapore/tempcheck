from rest_framework import serializers
from .models import Entry

class EntrySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Entry
        fields = ["temperature", "lat", "long", "file", "owner", "date_created"]

    def validate_temperature(self, value):
        if value < 32 or value > 42:
            raise serializers.ValidationError("Please enter a humanly possible temperature in Celcius (32 < T < 42)")
        return value

    def validate_lat(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Please enter valid coordinates: -90 < latitude < 90")
        return value

    def validate_long(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Please enter valid coordinates: -180 < longitude < 180")
        return value
