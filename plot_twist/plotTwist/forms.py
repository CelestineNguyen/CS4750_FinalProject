from django import forms
from .models import Lists
from .models import Review
import datetime

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



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} stars") for i in range(1, 6)]),
            'review_text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review...'}),
        }

    def save(self, commit=True, user=None, book=None):
        review = super().save(commit=False)
        review.user = user
        review.book = book
        review.created_at = datetime.date.today()

        # Manual PK handling since `managed = False`
        from django.db.models import Max
        max_id = Review.objects.aggregate(Max('review_id'))['review_id__max'] or 0
        review.review_id = max_id + 1

        if commit:
            review.save()
        return review