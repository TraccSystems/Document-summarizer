from django.shortcuts import render
import requests
from . forms import DocumentUploadForm,ChatForm
from django.http import HttpResponseRedirect
import os
import shutil
import time
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth import authenticate, login
from .models import Profile
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


from . documentuploader import (
    load_external_document,
    #load_uploaded_documments_to_pinecone,
    elasticsearch_document_embedding,
    load_local_document)

def login_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("chat-bot", args=(user.username,)))
        
    else:
        # Return an 'invalid login' error message.
        pass
    return render(request,"pages/login.html")


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@login_required(login_url="/chat/login/")
def chat_view(request,username):
    user = get_object_or_404(User,username=username)
    # get profile tgo filter vector_index_db
    user_profile = Profile.objects.get(user=request.user) 
    vector_index_name = user_profile.vectordb_index_name
    print(vector_index_name)
    if request.method == "POST":
        chatform = ChatForm(request.POST)
        uploadform = DocumentUploadForm(request.POST, request.FILES)
        if chatform.is_valid():
            chat = chatform.cleaned_data['chat']
            openai_api_key = "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"
            url = 'http://127.0.0.1:8000/api/summarizer/doc/summarizer/'
            data = {
                "query": chat,
                "openai_api_key":"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",
                "index_name":vector_index_name, ## request.user index_name
                "es_cloud_id":"tracc:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRmN2E5NjFiYTUzZDU0NzAyYjBkNmRiZDE3MWJiYTYwZSQyZjIxNDI0Nzg1ZjI0YWViYWE4M2QxMWU4MzhkZGZhYg==",
                "es_user":"elastic",
                "es_password":"6VXYyRVExbNPq15x9RdEXFQP",
                "es_api_key":"RGVJaWdJc0JGazl3TXAtR05TWUk6cE1yMlRWN1JTZ2FrdFk2aWtfbEpKQQ=="
            }
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            }
            response = requests.post(url,data,headers)
            if response.status_code == 200:
               print(response.json())
               return render(request,'pages/chat.html',{'chatform':chatform,"uploadform":uploadform,'response_data':response.json()['message'],'documentSource':response.json()['source']})
            
        elif uploadform.is_valid():

            uploaded_file= request.FILES["file"]

            tempdir = "file/uploads"
            os.makedirs(tempdir,exist_ok=True)
            file_path = os.path.join(tempdir,uploaded_file.name)

            with open(file_path,"wb") as locations:
                for chunk in uploaded_file.chunks():
                    locations.write(chunk)
           
            user = get_object_or_404(User,username=request.user)
    
           # get profile tgo filter vector_index_db
            user_profile = Profile.objects.get(user=user)
            user_profile.vectordb_index_name = f"{request.user}_index_name"
            user_profile.save()

            elasticsearch_document_embedding(file_path=file_path,
                                             openai_api_key="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",
                                             index_name=user_profile.vectordb_index_name,
                                             es_cloud_id="tracc:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRmN2E5NjFiYTUzZDU0NzAyYjBkNmRiZDE3MWJiYTYwZSQyZjIxNDI0Nzg1ZjI0YWViYWE4M2QxMWU4MzhkZGZhYg==", 
                                             es_user="elastic",
                                             es_password="6VXYyRVExbNPq15x9RdEXFQP",
                                             es_api_key='RGVJaWdJc0JGazl3TXAtR05TWUk6cE1yMlRWN1JTZ2FrdFk2aWtfbEpKQQ==',
                                             owner="request_user"
                                               )
            
            shutil.rmtree(os.path.dirname(file_path))

            return HttpResponseRedirect(reverse("chat-bot", args=(user.username,)))

    else:
        chatform = ChatForm()
        uploadform = DocumentUploadForm()
    return render(request,'pages/chat.html',{'chatform':chatform,"uploadform":uploadform})



def update_(request):
    load_external_document(space_key='',
                            space_secret='',
                            pinecone_api_key='788fc40b-a4bd-40b6-b4c5-6d02ae274428',
                            pinecone_environment='us-west4-gcp-free',
                            openai_api_key='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',
                            index_name='scrap-data')

    return HttpResponseRedirect('')






