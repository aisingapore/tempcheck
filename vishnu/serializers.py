from rest_framework import serializers
from .models import Entry

class EntrySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Entry
        fields = ["temperature", "x_coord", "y_coord", "file", "owner", "date_created"]

    def validate_temperature(self, value):
        if value < 32 or value > 42:
            raise serializers.ValidationError("Please enter a humanly possible temperature in Celcius (32 < T < 42)")
        return value
