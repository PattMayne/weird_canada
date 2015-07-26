from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, TextInput, Select, Textarea, FileInput, NumberInput, CheckboxInput, DateField, DateInput
from indie_db.models import URL, Artist, Work, Contributor, ProductionCompany, Style
from blog.models import Article, Tag, Author


class AddArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = ('name', 'description_en', 'description_fr', 'birthdate', 'deathdate', 'group')

        labels = {
            'name': _('Name'),
            'birthdate': _('Birth or Formed Date'),
            'deathdate': _('Death or Disbanded Date'),
            'group': _('Select if this artist is a group/band'),
            'description_en': _('English Description'),
            'description_fr': _('Français Description'),
            }

        widgets = {
            'name': TextInput(attrs={'placeholder': 'Enter Artist Name', 'required': True}),
            'birthdate': DateInput(attrs={'required': False}),
            'deathdate': DateInput(attrs={'required': False}),
            'group': CheckboxInput(attrs={'required': False}),
            'description_en': Textarea(attrs={'required': True, 'placeholder': 'Enter Artist Description (English)'}),
            'description_fr': Textarea(attrs={'required': True, 'placeholder': 'Entrez Artiste description (Français)'}),
            }

    def save(self, commit=True):
        artist = super(AddArtistForm, self).save(commit=True)
        artist.name = self.cleaned_data['name']
        artist.description_en = self.cleaned_data['description_en']
        artist.description_fr = self.cleaned_data['description_fr']
        artist.birthdate = self.cleaned_data['birthdate']
        artist.deathdate = self.cleaned_data['deathdate']
        artist.save()
        return artist


class AddWorkForm(ModelForm):
    class Meta:
        model = Work
        fields = ('work_category', 'title', 'description_en', 'description_fr', 'extra_data', 'created', 'city', 'self_published')

        labels = {
            'created': _('Release Date'),
            'title': _('Title'),
            'work_category': _('Media Category'),
            'description_en': _('English Description'),
            'description_fr': _('Français Description'),
            'extra_data': _('Extra Info'),
            'city': _('City and Province'),
        }

        widgets = {
            'created': DateInput(attrs={'required': False}),
            'work_category': Select(attrs={'required': True}),
            'title': TextInput(attrs={'placeholder': 'Enter Title', 'required': True}),
            'description_en': Textarea(attrs={'required': True, 'placeholder': 'Enter Description (English)'}),
            'description_fr': Textarea(attrs={'required': True, 'placeholder': 'Entrez description (Français)'}),
            'extra_data': Textarea(attrs={'required': False, 'placeholder': 'Enter Extra Info'}),
            'city': TextInput(attrs={'placeholder': 'City, PR', 'required': False}),
        }

    def save(self, commit=True):
        work = super(AddWorkForm, self).save(commit=True)
        work.title = self.cleaned_data['title']
        work.created = self.cleaned_data['created']
        work.description_en = self.cleaned_data['description_en']
        work.description_fr = self.cleaned_data['description_fr']
        work.extra_data = self.cleaned_data['extra_data']
        work.city = self.cleaned_data['city']
        work.work_category = self.cleaned_data['work_category']
        work.save()
        return work


class AddProductionCompanyForm(ModelForm):
    class Meta:
        model = ProductionCompany
        fields = ('name', 'city', 'description_en', 'description_fr')

        labels = {
            'name': _('Name of Company'),
            'city': _('City and Province'),
            'description_en': _('English Description'),
            'description_fr': _('Français Description'),
            }

        widgets = {
            'name': TextInput(attrs={'placeholder': 'Enter Artist Name', 'required': True}),
            'city': TextInput(attrs={'required': False}),
            'description_en': Textarea(attrs={'required': False, 'placeholder': 'Enter Description (English)'}),
            'description_fr': Textarea(attrs={'required': False, 'placeholder': 'Entrez description (Français)'}),
            }

    def save(self, commit=True):
        production_company = super(AddProductionCompanyForm, self).save(commit=True)
        production_company.name = self.cleaned_data['name']
        production_company.city = self.cleaned_data['city']
        production_company.description_en = self.cleaned_data['description_en']
        production_company.description_fr = self.cleaned_data['description_fr']
        production_company.save()
        return production_company
