from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    send_to = forms.EmailField(
        required=True, help_text='Receipient\'s address')
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
