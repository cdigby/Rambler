from django import forms
from django.contrib.auth.models import User

#Define user form
class UserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    #EmailField validates itself
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}), required=False)
    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}), required=False)

    def clean_username(self):
        data = self.cleaned_data['username']

        #Only if changing username
        if data != self.get_initial_for_field(self, 'username'):
            #Check not already taken
            if User.objects.filter(username__exact=data).exists():
                raise forms.ValidationError('Username already taken.')
        
        return data

    def clean(self):
        #Password with no confirmation
        if self.data['password'] and not self.data['password_confirmation']:
            self.add_error('password_confirmation', 'Please confirm your password.')

        #Confirmation with no password
        if not self.data['password'] and self.data['password_confirmation']:
            self.add_error('password', 'Please enter a password.')
        
        #Password and confirmation don't match
        if self.data['password'] and self.data['password_confirmation']:
            if self.data['password'] != self.data['password_confirmation']:
                err = "Password and confirmation don't match."
                self.add_error('password', err)
                self.add_error('password_confirmation', err)