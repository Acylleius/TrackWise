# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    
    
    class Meta:
        model = User
        fields = ('username', 'email') + UserCreationForm.Meta.fields[1:]
       
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].required = True
            self.fields['email'].label = 'Email Address'
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

class CustomAuthenticationForm(AuthenticationForm):
    pass
