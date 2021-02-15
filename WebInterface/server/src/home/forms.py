from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class UserForm(forms.Form):
    """
        Defines a form for entering a username to validate inputs.
    """
    username = forms.CharField(label='', min_length=1, max_length=30, widget=forms.TextInput(attrs = {'class':'form-control mr-sm-2', 'placeholder':'Username', 'aria-label':'Search'}))
    def clean_username(self):
        """
            Gets 'cleaned' data and returns.
        """
        # Todo: Use tweepy here to check if username is valid
        user = self.cleaned_data['username']
        # if not valid:
        #   raise ValidationError(_('Not a valid Twitter user.'))
        return user
