from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.exceptions import ValidationError

from django.conf import settings

from .forms import UploadForm
from .forms import SettingsForm
from .models import FileUpload

from .stats import Stats
from smartchain.ioncloud_client import Client


import string, random, time

def index(request):
	if 'config' in locals() or 'config' in globals():
		RPC_USER = config['rpc_user'] 
		RPC_PASS = config['rpc_pass']
		RPC_PORT = int(config['rpc_port'])
		CLIENT_PIN = int(config['client_pin'])
		CLIENT_PASS = config['client_pass']
	else:
		RPC_USER = settings.RPC_USER 
		RPC_PASS = settings.RPC_PASS
		RPC_PORT = settings.RPC_PORT
		CLIENT_PIN = settings.CLIENT_PIN
		CLIENT_PASS = settings.CLIENT_PASS
	
	client = Client()
	client.authenticateAs(CLIENT_PASS, CLIENT_PIN)
	context = {}
	
	if request.method == 'GET':
		search_query = request.GET.get('search_id', None)

		if search_query:
			try:
				doc = FileUpload.objects.get(identifier = search_query)
			except FileUpload.DoesNotExist:
				raise Http404("Document does not exist.")
			context = {
				'doc': doc
			}
			return render(request, 'details.html', context)

	if request.method == 'POST':
		if request.FILES['docfile'].__str__().split(".")[1] not in settings.ALLOWED_UPLOAD_FORMATS:
			raise ValidationError('This format is not allowed.')
		if request.FILES['docfile'].size > settings.UPLOAD_SIZE_LIMIT:
			raise ValidationError("The size of your upload is too large.")

		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			context['upload'] = 'Upload Successful'
			new_doc = FileUpload(docfile=request.FILES['docfile'], timestamp=timezone.now(), content=request.FILES['docfile'].name, identifier=''.join(random.SystemRandom().choice(string.digits) for _ in range(10)))
			new_doc.save()
			
			client.uploadFile('./files/' + request.FILES['docfile'].name)
			#return HttpResponseRedirect('/')

	context['latest_docs'] = FileUpload.objects.order_by('-timestamp')[:10]
	context['form'] = UploadForm()
	context['stats'] = Stats(RPC_USER,RPC_PASS, RPC_PORT).stats

	return render(request, 'index.html', context)

def details(request, doc_id):
	if 'config' in locals() or 'config' in globals():
		CLIENT_PIN = int(config['client_pin'])
		CLIENT_PASS = config['client_pass']
	else:
		CLIENT_PIN = settings.CLIENT_PIN
		CLIENT_PASS = settings.CLIENT_PASS
	client = Client()
	client.authenticateAs(CLIENT_PASS, CLIENT_PIN)
	try:
		doc = FileUpload.objects.get(identifier = doc_id)
		try:
			context = {
				'doc': doc,
				'file_path': doc.docfile.file.name.split('/')[-1]
			}
		except IOError as e:
			# If file not stored locally then search on the Ion Cloud
			client.requestFileContents(doc.docfile.name.split('/')[-1], './files/' + doc.docfile.name.split('/')[-1])
			context = {
				'doc': doc,
				'file_path': doc.docfile.file.name.split('/')[-1]
			}
			return render(request, 'details.html', context)
	except FileUpload.DoesNotExist:
		raise Http404("Document does not exist.")

	return render(request, 'details.html', context)

def configuration(request):
	if request.method == 'POST':
		form = SettingsForm(request.POST)
		if form.is_valid():
			global config
			config = form.cleaned_data
			return HttpResponseRedirect('/')
	else:
		form = SettingsForm()
	context = {'form': form}
	return render(request, 'settings.html', context)