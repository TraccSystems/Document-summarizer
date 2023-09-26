from rest_framework import serializers

class SummarizerSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)
    openai_api_key  = serializers.CharField(required=True, allow_blank=False, max_length=255)
