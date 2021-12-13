from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields
from .models import Student, Teacher
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='', label_suffix='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter first name"}),)
    last_name = forms.CharField(label='', label_suffix='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter last name"}),)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )

class StudentUploadForm(forms.ModelForm):
    avatar = forms.ImageField(label='', label_suffix='', widget=forms.FileInput(attrs={'class': 'form-control', 'type':'file', 'accept':'image/*'}),)
    phone_number = forms.CharField(required=False, label='', label_suffix='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter phone number"}),)
    country = forms.CharField(required=False, label='', label_suffix='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter country"}),)

    class Meta:
        model = Student
        fields = ('avatar', 'phone_number', 'country')
        # fields = ('avatar',)

class TeacherUploadForm(forms.ModelForm):
    avatar = forms.ImageField(label='', label_suffix='', widget=forms.FileInput(attrs={'class': 'form-control', 'type':'file', 'accept':'image/*'}),)
    phone_number = forms.CharField(required=False, label='', label_suffix='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter phone number"}),)
    country = forms.CharField(required=False, label='', label_suffix='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter country"}),)

    class Meta:
        model = Student
        fields = ('avatar', 'phone_number', 'country')

# class DateForm(forms.Form):
#     # date = forms.DateField(required=True, disabled=False, input_formats=["%d-%m-%Y"],
#     #                          widget=forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
#     #                          error_messages={'required': "This field is required."})
#     # time = forms.TimeField(required=True, disabled=False, input_formats=["%H:%M:%S"],
#     #                          widget=forms.TimeInput(attrs={'class': 'form-control', 'type':'time-local'}),
#     #                          error_messages={'required': "This field is required."})
    
#     date_time_field = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder':'Select a date an time'}))
#     # date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], widget=(forms.DateInput(attrs={
#     #     'type': 'text',
#     #     'placeholder': 'Choose a date',
#     #     'id': 'date'
    # })))



class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text='Required. 254 characters maximum and must be valid', label='', label_suffix='')
    
    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("The email is already registered, try another")
        return email