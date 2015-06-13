from django import forms
from django.forms import ModelForm, TextInput, Select, Textarea, FileInput, NumberInput, CheckboxInput
from indie_db.models import URL, Artist, Work, Contributor, ProductionCompany
from blog.models import Article, Tag, Author


class AddAuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('authorname', 'tagline', 'description', 'website')

        widgets = {
                'authorname': TextInput(attrs={'placeholder': 'Enter Name', 'required': True}),
                'tagline': TextInput(attrs={'placeholder': 'From the SOMETHING of...', 'required': True}),
                'description': Textarea(attrs={'required': True, 'placeholder': 'Enter Description'}),
                'website': TextInput(attrs={'required': False, 'placeholder': 'Enter Full URL'})
            }

    def save(self, commit=True):
        author = super(AddAuthorForm, self).save(commit=True)
        author.authorname = self.cleaned_data['authorname']
        author.tagline = self.cleaned_data['tagline']
        author.description = self.cleaned_data['description']
        author.website = self.cleaned_data['website']
        author.save()
        return author


class AddArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'body_en', 'body_fr', 'publish', 'created')

        widgets = {
            'created': DateInput(attrs={'required': True}),
            'title': TextInput(attrs={'placeholder': 'Enter Title', 'required': True}),
            'body_en': Textarea(attrs={'placeholder': 'Write English Article', 'required': False}),
            'publish': CheckboxInput(attrs={'required': False}),
            'body_fr': Textarea(attrs={'placeholder': 'Donnez votre article Française', 'required': False})
        }

        labels = {
            'created': _('Orignal Publication Date'),
            'title': _('Title'),
            'body_en': _('English Text'),
            'publish': _('Publish Now?'),
            'body_fr': _('Article Français'),
        }

    def save(self, commit=True):
        article = super(AddArticleForm, self).save(commit=True)
        article.title = self.cleaned_data['title']
        article.created = self.cleaned_data['created']
        article.body_en = self.cleaned_data['body_en']
        article.body_fr = self.cleaned_data['body_fr']
        article.publish = self.cleaned_data['publish']
        article.save()
        return article


