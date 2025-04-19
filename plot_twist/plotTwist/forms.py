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

    def clean_list_name(self):
        name = self.cleaned_data.get('list_name')
        if not name or name.strip() == "":
            raise forms.ValidationError("List name cannot be empty")
        return name