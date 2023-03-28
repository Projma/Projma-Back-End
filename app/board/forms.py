from django import forms
from board.models import Board

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
