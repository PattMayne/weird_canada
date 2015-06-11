from django import forms
from django.forms import ModelForm, TextInput, Select, Textarea, FileInput, NumberInput, CheckboxInput
from indie_db.models import URL, Artist, Work, Contributor, ProductionCompany
from blog.models import Entry, Tag, Author


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


class BlogEntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ('author', 'title', 'slug', 'category', 'body_en', 'body_fr', 'publish', 'tags')

        widgets = {
            'title': TextInput(attrs={'placeholder': 'Enter Title', 'required': True}),
            'body_en': Textarea(attrs={'placeholder': 'English Body', 'required': False}),
            'publish': CheckboxInput(attrs={'label': 'Publish Now?', 'required': False}),
            'body_en': Textarea(attrs={'placeholder': 'Article Français', 'required': False})
        }
