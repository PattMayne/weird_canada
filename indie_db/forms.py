from django import forms
from django.forms import ModelForm, TextInput, Select, Textarea, FileInput, NumberInput, CheckboxInput
from indie_db.models import URL, Artist, Work, Contributor, ProductionCompany
from blog.models import Entry, Tag, Author


class AddArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = ('name', 'website', 'description')

        widgets = {
            'name': TextInput(attrs={'placeholder': 'Enter Artist Name', 'required': True}),
            'description': Textarea(attrs={'required': True, 'placeholder': 'Enter Artist Description'}),
            'website': TextInput(attrs={'required': False, 'placeholder': 'Enter Full Website URL'})
            }

    def save(self, commit=True):
        artist = super(AddArtistForm, self).save(commit=True)
        artist.name = self.cleaned_data['name']
        artist.description = self.cleaned_data['description']
        artist.website = self.cleaned_data['website']
        artist.save()
        return artist


class AddWorkForm(ModelForm):
    class Meta:
        model = Work
        fields = ('category', 'title', 'description', 'extra_data', 'created', 'city', 'self_published', 'creator', 'website', 'styles')

        widgets = {
            'category' = TextInput(attrs={'placeholder': 'Category', 'required': True}),
            'title': TextInput(attrs={'placeholder': 'Enter Title of Work', 'required': True}),
            'description': Textarea(attrs={'required': False, 'placeholder': 'Enter Work Description'}),
            'extra_data': Textarea(attrs={'required': False, 'placeholder': 'Enter Work Extra Data'}),
            'city': TextInput(attrs={'placeholder': 'Enter City and Abbreviated Province', 'required': False}),
            'website': TextInput(attrs={'required': False, 'placeholder': 'Enter Full Website URL'}),
            'styles': TextInput(attrs={'required': False, 'placeholder': 'Enter Styles and Genres'})
        }

    def save(self, commit=True):
        work = super(AddWorkForm, self).save(commit=True)
        work.title = self.cleaned_data['title']
        work.description = self.cleaned_data['description']
        work.website = self.cleaned_data['website']
        work.extra_data = self.cleaned_data['extra_data']
        work.city = self.cleaned_data['city']
        work.category = self.cleaned_data['category']
        work.styles = self.cleaned_data['styles']
        work.save()
        return work
