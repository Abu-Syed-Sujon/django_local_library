from django import forms
from .models import Author 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
from .models import BookInstance

class RenewBookModelForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('Renewal date')}
        help_text = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}

    # This method MUST be inside the class
    def clean_due_back(self):
        """Validate the due_back date."""
        # Use 'due_back' because that is the field name in your Model
        data = self.cleaned_data['due_back']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data

class AuthorForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        #help_text="Enter the author's date of birth (YYYY-MM-DD)",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}))
    date_of_death = forms.DateField(
        #help_text="Enter the author's date of death (YYYY-MM-DD)",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Author
        fields = '__all__'

