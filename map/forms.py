from django import forms

class CarrierForm(forms.Form):
	carrier = forms.CharField()