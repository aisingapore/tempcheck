from rest_framework import serializers
from .models import Entry

class EntrySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Entry
        fields = ["temperature", "x_coord", "y_coord", "file", "owner", "date_created"]
