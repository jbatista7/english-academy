from django import forms

class DateForm(forms.Form):
    date_time_field = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder':'Select a date an time'}))

