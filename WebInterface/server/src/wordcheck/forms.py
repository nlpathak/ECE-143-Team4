from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class WordCheckForm(forms.Form):
    """
        Defines a form for entering text and getting a sentiment response. 
    """
    # widget=forms.TextInput(attrs = {'class':'form-control mr-sm-2', 'placeholder':'Insert a tweet.', 'aria-label':'Search'})
    txt = forms.CharField(label="",help_text='',min_length=1, max_length=280)
    def clean_txt(self):
        """
            Gets 'cleaned' data and returns.
        """
        # Todo: Use tweepy here to check if username is valid
        txt = self.cleaned_data['txt']
        # if not valid:
        #   raise ValidationError(_('Not a valid Twitter user.'))
        return user
