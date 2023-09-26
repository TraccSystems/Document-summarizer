from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

from . summarizer import (
    get_similarity_search,
    get_summarizer_question_query,
    get_similarity_search_singlestore,
    get_summarizer_question_query_singlestore

    )
from . serializers import SummarizerSerializer
from rest_framework import status
# Create your views here.



class SummarizerView(GenericAPIView):
    serializer_class = SummarizerSerializer
    #permission_classes = [permissions.IsAuthenticated]
    @extend_schema(summary='Send a Message', methods=["GET"],description='Query Your Csv Files',filters=True,tags=['Summarizer'])
    def post(self,request,format=None):
        serializer = SummarizerSerializer(data=self.request.data)
        if serializer.is_valid():
            message_request = serializer.validated_data.get('message')
            openai_api_key = serializer.validated_data.get('openai_api_key')
            question_answer = get_similarity_search(openai_api_key=openai_api_key)
            message_response =  get_summarizer_question_query(message_request,question_answer)
            return Response(dict(message=message_response),status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

