from django import forms




class DocumentUploadForm(forms.Form):
    file = forms.FileField()
    file.widget.attrs.update({"class":"hidden","id":"dropzone-file"})

class ChatForm(forms.Form):
    chat = forms.CharField(max_length=255)
    chat.widget.attrs.update({'class':
                              "block w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                              "id":"default-search","type":"search","placeholder":"Send query message ......"})