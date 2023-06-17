from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Board, Comment, Category


class BoardForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Board
        fields = ('category', 'title', 'content',)


class CommentForm(forms.ModelForm):
    text = forms.CharField(label='Комментарий:')

    class Meta:
        model = Comment
        fields = ('text',)

