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

class BoardForm(forms.ModelForm):
    class Meta:
        models = Board
        fields = '__all__'
    
    def clean(self):
        """Make sure owner is also members."""
        admins = self.cleaned_data['admins']
        members = list(self.cleaned_data['members'])
        for admin in admins:
            if admin not in members:
                members.append(admin)
        self.cleaned_data['members'] = members
        return self.cleaned_data
