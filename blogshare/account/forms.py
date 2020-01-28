from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(label='Password', widget=forms.PasswordInput)
    password2=forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model=get_user_model()
        fields=('email', 'first_name', 'last_name', 'contact')

    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')

class USerEditForm(forms.ModelForm):
    class Meta:
        model=get_user_model()
        fields=('first_name', 'last_name', 'contact', 'discription', 'dob')
