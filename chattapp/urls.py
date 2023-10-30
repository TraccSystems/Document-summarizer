from django.urls import path
from django.contrib.auth import views as auth_views

from . import views



urlpatterns = [
    #path('documentupload/',views.document_upload,name='document-upload'),
    path("login/",views.login_view,name="login"),
    path('<username>/',views.chat_view,name='chat-bot'),
]
