from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    # ADD THE EMAIL FIELD HERE:
    email = forms.EmailField(required=True, label='Email') 

    class Meta(UserCreationForm.Meta):
        model = User
        # Include 'email' in the fields list
        fields = ('username', 'email') + UserCreationForm.Meta.fields[1:] 
        # The fields[1:] ensures you get password1 and password2

class CustomAuthenticationForm(AuthenticationForm):
    pass