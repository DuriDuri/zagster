from django import forms

class TaskForm(forms.Form):
    requestor = forms.CharField(max_length=32, label='Name')
    task = forms.CharField(max_length=1000, label='What do you need?')
    offer = forms.DecimalField(max_digits=1000, decimal_places=2, label='Your offer')