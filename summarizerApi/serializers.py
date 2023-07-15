from rest_framework import serializers

class SummarizerSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)