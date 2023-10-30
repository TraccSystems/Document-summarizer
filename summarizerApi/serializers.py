from rest_framework import serializers

class SummarizerSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=200)
    index_name = serializers.CharField(max_length=200)
    openai_api_key  = serializers.CharField(required=True, allow_blank=False, max_length=255)
    es_cloud_id = serializers.CharField(max_length=200)
    es_user = serializers.CharField(max_length=200)
    es_password = serializers.CharField(max_length=200)
    es_api_key = serializers.CharField(max_length=200)



class SingleStoreSerializer(serializers.Serializer):
    pass
