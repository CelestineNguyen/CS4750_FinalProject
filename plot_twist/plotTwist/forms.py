from django import forms
from .models import Lists

class CreateListForm(forms.ModelForm):
    class Meta:
        model = Lists
        fields = ['list_name']
        labels = {
            'list_name': 'List Name'
        }
        widgets = {
            'list_name': forms.TextInput(attrs={'class': 'list-input'}),
        }
