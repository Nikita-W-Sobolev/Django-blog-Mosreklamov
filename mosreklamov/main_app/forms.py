from django import forms

from main_app.models import Article


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
