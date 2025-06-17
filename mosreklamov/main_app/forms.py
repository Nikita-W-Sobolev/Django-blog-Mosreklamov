from django import forms

from main_app.models import Article, Category


class AddPostForm(forms.ModelForm):
    categories = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label='Категория')
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }
