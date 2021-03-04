from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class WordCheckForm(forms.Form):
    """
        Defines a form for entering text and getting a sentiment response. 
    """
    txt = forms.CharField(label="",min_length=1, max_length=280,widget=forms.TextInput(attrs = {'placeholder':'Insert a tweet.'}))
    def clean_txt(self):
        """
            Gets 'cleaned' data and returns.
        """
        # Todo: Use tweepy here to check if username is valid
        txt = self.cleaned_data['txt']
        # if not valid:
        #   raise ValidationError(_('Not a valid Twitter user.'))
        return txt
