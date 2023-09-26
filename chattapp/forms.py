from django import forms




class DocumentUploadForm(forms.Form):
    file = forms.FileField()

class ChatForm(forms.Form):
    chat = forms.CharField(max_length=255)