from django import forms

class UploadForm(forms.Form):
	docfile = forms.FileField(
		label = 'Select a file',
		help_text= 'You can upload a file directly by clicking browse'
	)

class SettingsForm(forms.Form):
	rpc_user = forms.CharField(label='RPC Username', max_length=100, required=True)
	rpc_pass = forms.CharField(label='RPC Password', max_length=100, required=True)
	rpc_port = forms.CharField(label='RPC Port', max_length=10, required=True)
	client_pin = forms.CharField(label='Client Pin', max_length=100, required=True)
	client_pass = forms.CharField(label='Client Password', max_length=100, required=True)
	masternode_ip = forms.CharField(label='Master Node IP', max_length=100, required=True)
