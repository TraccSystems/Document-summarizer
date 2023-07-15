from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

from . summarizer import (get_similarity_search,get_summarizer_question_query
    )
from . serializers import SummarizerSerializer
from rest_framework import status
# Create your views here.



class SummarizerView(APIView):
    #permission_classes = [permissions.IsAuthenticated]
    @extend_schema(summary='Send a Message', methods=["GET"],description='Query Your Csv Files',filters=True,tags=['Summarizer'])
    def post(self,request,message,openai_api_key,format=None):
        question_answer = get_similarity_search(
        openai_api_key=openai_api_key,
        host="svc-39f86d53-e0bf-4708-9e17-18faf0dfe22c-dml.aws-virginia-6.svc.singlestore.com",
        password="84563320Owo",db='scrap_db')
        messages = get_summarizer_question_query(message,question_answer)
        serializer = SummarizerSerializer({"message":messages})
        return Response(serializer.data,status=status.HTTP_200_OK)


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()



class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()

