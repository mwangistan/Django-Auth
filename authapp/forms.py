from django import forms

class EmailConfimationForm(forms.Form):
	email = forms.EmailField(required=True, help_text="Required")