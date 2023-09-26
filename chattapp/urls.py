from django.urls import path

from . import views



urlpatterns = [
    path('',views.chat_view,name='chat'),
    path('documentupload/',views.document_upload,name='document-upload'),
    
]
