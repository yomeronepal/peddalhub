from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class AddCycleForm(forms.ModelForm):
    class Meta:
        model = Cycle
        fields ='__all__'
        widgets={
            'name':forms.TextInput(attrs={ 'placeholder':'PRODUCT Name','id':'product_name','class':"form-control input-md", 'required':""}),
            'color':forms.TextInput(attrs={ 'class':"form-control input-md", 'required':""}),
            'cycle_description':forms.Textarea(attrs={'class':"form-control input-md", 'required':""}),
            'hire_description': forms.Textarea(attrs={'class': "form-control input-md", 'required': ""}),



        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class CustomerDetailForm(forms.ModelForm):
    class Meta:
        model= Customer
        fields=['name','address','contact','profile_pic']

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class RentalForm(forms.ModelForm):
    rental_date = forms.DateField(widget=DateInput)
    return_date = forms.DateField(widget=DateInput)
    rental_time = forms.TimeField(widget=TimeInput)
    rental_status = forms.BooleanField()
    class Meta:
        model = Rental
        fields = ['rental_date','rental_time','return_date','rental_status']

