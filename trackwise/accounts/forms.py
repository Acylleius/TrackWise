from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, Company

class BusinessOwnerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'you@example.com'
    }))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter first name'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter last name'
    }))
    
    # Company selection
    company_choice = forms.ChoiceField(
        choices=[('new', 'New Company'), ('existing', 'Existing Company')],
        widget=forms.RadioSelect(attrs={'class': 'radio-input'}),
        initial='new'
    )
    existing_company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select a company'
        }),
        empty_label="-- Select Existing Company --"
    )
    new_company_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'E.g., TrackWise Logistics Inc.'
        })
    )
    company_address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control form-textarea',
            'placeholder': 'Street, City, Postal Code',
            'rows': 3
        })
    )
    company_contact = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone or primary contact email'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Update field attributes for the new design
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Min 8 characters'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Repeat password'
        })
        
        # Style the radio buttons properly
        self.fields['company_choice'].widget.attrs.update({'class': 'radio-input'})

    def clean(self):
        cleaned_data = super().clean()
        company_choice = cleaned_data.get('company_choice')
        
        if company_choice == 'new':
            if not cleaned_data.get('new_company_name'):
                self.add_error('new_company_name', 'Company name is required when creating a new company.')
        else:  # existing
            if not cleaned_data.get('existing_company'):
                self.add_error('existing_company', 'Please select an existing company.')
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
            # Handle company creation/selection
            company_choice = self.cleaned_data['company_choice']
            if company_choice == 'new':
                company = Company.objects.create(
                    name=self.cleaned_data['new_company_name'],
                    address=self.cleaned_data['company_address'] or '',
                    contact_info=self.cleaned_data['company_contact'] or ''
                )
            else:
                company = self.cleaned_data['existing_company']
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                role='business_owner',
                company=company,
                phone_number='',
                assigned_location='Main Office',
                department='Management',
                position='Owner',
                is_active=True,
                notes='Business owner account',
            )
        return user

class StaffRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'you@example.com'
    }))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter first name'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter last name'
    }))
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select your company'
        }),
        empty_label="-- Select Your Company --"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Min 8 characters'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Repeat password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role='staff',
                company=self.cleaned_data['company'],
                phone_number='',
                assigned_location='Main Office',
                department='General',
                position='Staff Member',
                is_active=True,
                notes='Staff account',
            )
        return user

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })