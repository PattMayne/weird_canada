from django import forms
from django.forms import ModelForm, TextInput, Select, Textarea, FileInput, NumberInput, CheckboxInput
from indie_db.models import URL, Artist, Work, Contributor, ProductionCompany
from blog.models import Entry, Tag, Author


class AddAuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('author_name', 'tagline', 'description', 'website')

    def save(self, commit=True):
        author = super(AddAuthorForm, self).save(commit=True)
        author.author_name = self.cleaned_data['author_name']
        author.tagline = self.cleaned_data['tagline']
        author.description = self.cleaned_data['description']
        author.website = self.cleaned_data['website']
        author.save()
        return author

    widgets = {
            'author_name': TextInput(attrs={'placeholder': 'Author Name', 'required': True, 'max_length': 200}),
            'tagline': TextInput(attrs={'placeholder': 'Genres & Styles', 'required': True}),
            'description': Textarea(attrs={'required': True}),
            'website': TextInput(attrs={'required': False})
        }