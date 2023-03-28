from django import forms
from .models import *

class WorkSpaceForm(forms.ModelForm):
    class Meta:
        model = WorkSpace
        fields = '__all__' 

    def clean(self):
        """Make sure owner is also members."""
        owner = self.cleaned_data['owner']
        members = list(self.cleaned_data['members'])
        if owner not in members:
            members.append(owner)
        self.cleaned_data['members'] = members
        return self.cleaned_data
