from django import forms
from django.forms import ModelForm, TextInput, Select, Textarea, FileInput, NumberInput, CheckboxInput
from indie_db.models import URL, Artist, Work, Contributor, ProductionCompany
from blog.models import Entry, Tag, Author


class AddAuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('authorname', 'tagline', 'description', 'website')

    def save(self, commit=True):
        author = super(AddAuthorForm, self).save(commit=True)
        author.authorname = self.cleaned_data['authorname']
        author.tagline = self.cleaned_data['tagline']
        author.description = self.cleaned_data['description']
        author.website = self.cleaned_data['website']
        author.save()
        return author

    widgets = {
            'authorname': TextInput(attrs={'placeholder': 'Author Name', 'required': True, 'max_length': 200}),
            'tagline': TextInput(attrs={'placeholder': 'Genres & Styles', 'required': True}),
            'description': Textarea(attrs={'required': True}),
            'website': TextInput(attrs={'required': False})
        }