from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=150, required=True, widget=forms.TextInput(attrs={
        'class': 'validate',
        'id': 'register_username'
    }))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={
        'id': 'register_email',
        'class': 'validate'
    }))
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput({
        'id': 'register_password',
        'class': 'validate'
    }))

    def is_valid(self):
        valid = super(RegisterForm, self).is_valid()

        if not valid:
            return valid

        user = User.objects.filter(email=self.cleaned_data['email']).first()

        if user:
            self._errors['email'] = 'Email is already exists!'
            return False

        return True

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class': 'validate'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'validate'
    }))
