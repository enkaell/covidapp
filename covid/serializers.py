from rest_framework import serializers
from .models import *


class UserCardSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    second_name = serializers.CharField()
    last_name = serializers.CharField()
    sex = serializers.CharField()
    age = serializers.IntegerField()
    diagnosis = serializers.CharField()
    comment = serializers.CharField()
    user = serializers.RelatedField(source='User', read_only=True)

    class Meta:
        model = UserCard


class DailyDictSerializer(serializers.Serializer):
    pulse = serializers.FloatField()
    temperature = serializers.FloatField()
    exercises = serializers.CharField()
    sleep_time = serializers.IntegerField()
    user = serializers.RelatedField(source='User', read_only=True)

    class Meta:
        model = DailyDictionary
