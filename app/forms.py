from django import forms

class UploadForm(forms.Form):
	docfile = forms.FileField(
		label = 'Select a file',
		help_text= 'You can upload a file directly by clicking browse'
	)