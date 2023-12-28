from django import forms

from .models import Email

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = '__all__'

class SingleEmailForm(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control custom-class', 'rows': 5}))
