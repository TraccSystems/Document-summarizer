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
        openai_api_key=openai_api_key,)
        messages = get_summarizer_question_query(message,question_answer)
        serializer = SummarizerSerializer({"message":{
            {"question":messages['question'],"anwser":messages['answer'],"sources":messages['sources']}
            }
            })
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

