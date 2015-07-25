import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django.forms import ModelForm, TextInput, Select, Textarea, FileInput, NumberInput, CheckboxInput, DateField, DateInput, DateTimeInput, SelectMultiple
from indie_db.models import URL, Artist, Work, Contributor, ProductionCompany
from blog.models import Article, Tag, Author


class AddAuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('authorname', 'tagline', 'description_en', 'description_fr', 'website')

        widgets = {
                'authorname': TextInput(attrs={'placeholder': 'Enter Name', 'required': True}),
                'tagline': TextInput(attrs={'placeholder': 'From the SOMETHING of...', 'required': True}),
                'description_en': Textarea(attrs={'required': True, 'placeholder': 'Enter Description (English)'}),
                'description_en': Textarea(attrs={'required': True, 'placeholder': 'Entrez Description (Français)'}),
                'website': TextInput(attrs={'required': False, 'placeholder': 'Enter Full URL'})
            }

    def save(self, commit=True):
        author = super(AddAuthorForm, self).save(commit=True)
        author.authorname = self.cleaned_data['authorname']
        author.tagline = self.cleaned_data['tagline']
        author.description_en = self.cleaned_data['description_en']
        author.description_fr = self.cleaned_data['description_fr']
        author.website = self.cleaned_data['website']
        author.save()
        return author


class EditAuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('authorname', 'tagline', 'description_en', 'description_fr', 'website')

        widgets = {
                'authorname': TextInput(attrs={'placeholder': 'Enter Name', 'required': True}),
                'tagline': TextInput(attrs={'placeholder': 'From the SOMETHING of...', 'required': True}),
                'description_en': Textarea(attrs={'required': True, 'placeholder': 'Enter Description (English)'}),
                'description_en': Textarea(attrs={'required': True, 'placeholder': 'Entrez Description (Français)'}),
                'website': TextInput(attrs={'required': False, 'placeholder': 'Enter Full URL'})
            }

    def save(self, commit=True):
        author = super(EditAuthorForm, self).save(commit=True)
        author.authorname = self.cleaned_data['authorname']
        author.tagline = self.cleaned_data['tagline']
        author.description_en = self.cleaned_data['description_en']
        author.description_fr = self.cleaned_data['description_fr']
        author.website = self.cleaned_data['website']
        author.save()
        return author


class AddArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('date_created', 'title', 'body_en', 'body_fr', 'article_category', 'how_category', 'publish', 'epoch', 'cover_image')

        widgets = {
            'cover_image': FileInput(),
            'title': TextInput(attrs={'placeholder': 'Enter Title', 'required': True}),
            'date_created': DateTimeInput(attrs={'required': True}),
            'epoch': Select(attrs={'required': True}),
            'article_category': Select(attrs={'required': True}),
            'how_category': SelectMultiple(attrs={'required': False}),
            'body_en': Textarea(attrs={'placeholder': 'Write English Article', 'required': False}),
            'publish': CheckboxInput(attrs={'required': False}),
            'body_fr': Textarea(attrs={'placeholder': 'Donnez votre article Française', 'required': False})
        }

        labels = {
            'cover_image': _('Cover Image'),
            'date_created': _('Orignal Publication Date'),
            'title': _('Title'),
            'body_en': _('English Text'),
            'publish': _('Publish Now?'),
            'body_fr': _('Article Français'),
            'article_category': _('Choose Main Category'),
            'how_category': _('Choose How Category'),
            'epoch': _('Epoch ("When" Category)'),
        }

    def save(self, commit=True):
        article = super(AddArticleForm, self).save(commit=True)
        article.title = self.cleaned_data['title']
        article.cover_image = self.cleaned_data['cover_image']
        chosen_creation_date = self.cleaned_data['date_created']
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        chosen_creation_date = chosen_creation_date.replace(hour=hour, minute=minute)
        article.date_created = chosen_creation_date
        article.date_modified = datetime.datetime.now()
        article.body_en = self.cleaned_data['body_en']
        article.body_fr = self.cleaned_data['body_fr']
        article.publish = self.cleaned_data['publish']
        article.article_category = self.cleaned_data['article_category']
        article.how_category = self.cleaned_data['how_category']
        article.epoch = self.cleaned_data['epoch']
        article.save()
        return article


class UpdateProfileForm(forms.ModelForm):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super(UpdateProfileForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
