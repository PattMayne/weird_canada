from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, TextInput, Select, Textarea, FileInput, NumberInput, CheckboxInput, DateField, DateInput
from indie_db.models import URL, Artist, Work, Contributor, ProductionCompany
from blog.models import Article, Tag, Author


class AddArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = ('name', 'description', 'birthdate', 'deathdate', 'group')

        labels = {
            'name': _('Name'),
            'birthdate': _('Birth or Formed Date'),
            'deathdate': _('Death or Disbanded Date'),
            'group': _('Select if this artist is a group/band'),
            'description': _('Description'),
            }

        widgets = {
            'name': TextInput(attrs={'placeholder': 'Enter Artist Name', 'required': True}),
            'birthdate': DateInput(attrs={'required': False}),
            'deathdate': DateInput(attrs={'required': False}),
            'group': CheckboxInput(attrs={'required': False}),
            'description': Textarea(attrs={'required': True, 'placeholder': 'Enter Artist Description'}),
            }

    def save(self, commit=True):
        artist = super(AddArtistForm, self).save(commit=True)
        artist.name = self.cleaned_data['name']
        artist.description = self.cleaned_data['description']
        artist.birthdate = self.cleaned_data['birthdate']
        artist.deathdate = self.cleaned_data['deathdate']
        artist.save()
        return artist


class AddWorkForm(ModelForm):
    class Meta:
        model = Work
        fields = ('work_category', 'title', 'description', 'extra_data', 'created', 'city', 'self_published')

        labels = {
            'created': _('Release Date'),
            'work_category': _('Media Category'),
            'title': _('Title'),
            'description': _('Description'),
            'extra_data': _('Extra Info'),
            'city': _('City and Province'),
            #'styles': _('Styles and Genres')
        }

        widgets = {
            'created': DateInput(attrs={'required': False}),
            'work_category': TextInput(attrs={'placeholder': 'Enter Category', 'required': True}),
            'title': TextInput(attrs={'placeholder': 'Enter Title', 'required': True}),
            'description': Textarea(attrs={'required': False, 'placeholder': 'Enter Description'}),
            'extra_data': Textarea(attrs={'required': False, 'placeholder': 'Enter Extra Info'}),
            'city': TextInput(attrs={'placeholder': 'City, PR', 'required': False}),
            #'styles': TextInput(attrs={'required': False, 'placeholder': 'Separate them with a comma (" , ") Max five'})
        }

    def save(self, commit=True):
        work = super(AddWorkForm, self).save(commit=True)
        work.title = self.cleaned_data['title']
        work.created = self.cleaned_data['created']
        work.description = self.cleaned_data['description']
        work.extra_data = self.cleaned_data['extra_data']
        work.city = self.cleaned_data['city']
        work.work_category = self.cleaned_data['work_category']
        work.save()
        return work


class AddProductionCompanyForm(ModelForm):
    class Meta:
        model = ProductionCompany
        fields = ('name', 'website', 'location')

        labels = {
            'name': _('Name of Company'),
            'website': _('Full official URL (include http://)'),
            'location': _('City and Province'),
            }

        widgets = {
            'name': TextInput(attrs={'placeholder': 'Enter Artist Name', 'required': True}),
            'website': TextInput(attrs={'required': False}),
            'location': TextInput(attrs={'required': False}),
            }

    def save(self, commit=True):
        production_company = super(AddProductionCompanyForm, self).save(commit=True)
        production_company.name = self.cleaned_data['name']
        production_company.website = self.cleaned_data['website']
        production_company.location = self.cleaned_data['location']
        production_company.save()
        return production_company
