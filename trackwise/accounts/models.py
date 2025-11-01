from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    contact_info = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('business_owner', 'Business Owner'),
        ('staff', 'Staff'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Add the missing fields that exist in your database
    assigned_location = models.CharField(max_length=100, blank=True, default='Main Office')
    department = models.CharField(max_length=100, blank=True, default='General')
    position = models.CharField(max_length=100, blank=True, default='')
    date_joined = models.DateField(auto_now_add=True)  # Matches the date_joined in database
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role} - {self.company.name}"