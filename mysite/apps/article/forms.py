from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'column', 'tags']


class ArticleTagForm(forms.Form):
    name = forms.CharField(max_length=50)

