from django import forms
from .models import Student
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