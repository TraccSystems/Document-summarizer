from django.shortcuts import render
import requests
from . forms import DocumentUploadForm,ChatForm
from django.http import HttpResponseRedirect
import os
import shutil
import time
from . documentuploader import (
    load_external_document,
    #load_uploaded_documments_to_pinecone,
    elasticsearch_document_embedding,
    load_local_document)



def chat_view(request):
    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.cleaned_data['chat']
            openai_api_key = "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"
            url = 'http://127.0.0.1:8000/api/summarizer/doc/summarizer/'
            data = {
                "message": chat,
                "openai_api_key":"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",
                "index_name":"text-data", ## request.user index_name
                "es_cloud_id":"5ff865cf73aa41adb21f70831b9360d1:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ0ZTRjMjkzZjViNDI0ZTI4OTA4ZDUzNzlkYWZkZTYxMCQzMzQyNTg4ZjlmZmE0YTZiYTRkYTYzZTQ2YzQ3ZTc1NA==",
                "es_user":"elastic",
                "es_password":"ZvCQE7pamHpmVCc70jaVWwTa",
                "es_api_key":"MnRvTjhZb0JFVUxsbG81ZmJ0RWU6X1FJN1ZGTjlTWktoMmVuMzd1SE01QQ=="
            }
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            }
            response = requests.post(url,data,headers)
            if response.status_code == 200:
               return render(request,'chattapp/chat.html',{'form':form,'response_data':response.json()})
    else:
        form = ChatForm()
    return render(request,'chattapp/chat.html',{'form':form})



def document_upload(request):
    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():

            uploaded_file= request.FILES["file"]

            tempdir = "file/uploads"
            os.makedirs(tempdir,exist_ok=True)
            file_path = os.path.join(tempdir,uploaded_file.name)

            with open(file_path,"wb") as locations:
                for chunk in uploaded_file.chunks():
                    locations.write(chunk)
            ## upload any file type to pincone
        
            elasticsearch_document_embedding(file_path=file_path,
                                             openai_api_key="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",
                                             index_name="text-data",
                                             es_cloud_id="5ff865cf73aa41adb21f70831b9360d1:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ0ZTRjMjkzZjViNDI0ZTI4OTA4ZDUzNzlkYWZkZTYxMCQzMzQyNTg4ZjlmZmE0YTZiYTRkYTYzZTQ2YzQ3ZTc1NA==", 
                                             es_user="elastic",
                                             es_password="ZvCQE7pamHpmVCc70jaVWwTa",
                                             es_api_key='MnRvTjhZb0JFVUxsbG81ZmJ0RWU6X1FJN1ZGTjlTWktoMmVuMzd1SE01QQ==',
                                             owner="request_user"
                                            
                                               )
            
            #shutil.rmtree(os.path.dirname(file_path))

            return HttpResponseRedirect("/chat/documentupload/")
    else:
         form = DocumentUploadForm()

    return render(request,'chattapp/documentupload.html',{'form':form})




def update_(request):
    load_external_document(space_key='',
                            space_secret='',
                            pinecone_api_key='788fc40b-a4bd-40b6-b4c5-6d02ae274428',
                            pinecone_environment='us-west4-gcp-free',
                            openai_api_key='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',
                            index_name='scrap-data')

    return HttpResponseRedirect('')






