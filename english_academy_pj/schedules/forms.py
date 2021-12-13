from django import forms

class DateForm(forms.Form):
    # date = forms.DateField(required=True, disabled=False, input_formats=["%d-%m-%Y"],
    #                          widget=forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
    #                          error_messages={'required': "This field is required."})
    # time = forms.TimeField(required=True, disabled=False, input_formats=["%H:%M:%S"],
    #                          widget=forms.TimeInput(attrs={'class': 'form-control', 'type':'time-local'}),
    #                          error_messages={'required': "This field is required."})
    
    date_time_field = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder':'Select a date an time'}))
    # date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], widget=(forms.DateInput(attrs={
    #     'type': 'text',
    #     'placeholder': 'Choose a date',
    #     'id': 'date'
    # })))

