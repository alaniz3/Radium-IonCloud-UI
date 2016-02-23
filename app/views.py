from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.exceptions import ValidationError

from .forms import UploadForm
from .models import FileUpload
from .models import Document
from .stats import Stats

from django.conf import settings

from itertools import chain
from operator import attrgetter
import string
import random

def index(request):
	context = {}
	if request.method == 'GET':
		search_query = request.GET.get('search_id', None)
		upload_query = request.GET.get('upload_query', None)

		if search_query:
			try:
				doc = Document.objects.get(identifier = search_query)
			except Document.DoesNotExist:
				try:
					doc = FileUpload.objects.get(identifier = search_query)
				except FileUpload.DoesNotExist:
					raise Http404("Document does not exist.")
			context = {
				'doc': doc
			}
			return render(request, 'details.html', context)

		if upload_query:
			new_doc = Document(content=upload_query, timestamp=timezone.now(), identifier=''.join(random.SystemRandom().choice(string.digits) for _ in range(10)))
			new_doc.save()
			return HttpResponseRedirect('/')

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
			#return HttpResponseRedirect('/')

	context['latest_docs'] = sorted(chain(Document.objects.all(), FileUpload.objects.all()), key = attrgetter('timestamp'), reverse=True)[:10]
	context['form'] = UploadForm()
	context['stats'] = Stats().stats

	return render(request, 'index.html', context)

def details(request, doc_id):
	try:
		print "hello"
		doc = Document.objects.get(identifier = doc_id)
		print doc
	except Document.DoesNotExist:
		try:
			doc = FileUpload.objects.get(identifier = doc_id)
		except FileUpload.DoesNotExist:
			raise Http404("Document does not exist.")
	context = {
		'doc': doc
	}
	return render(request, 'details.html', context)

def configuration(request):
	context = {}
	return render(request, 'settings.html', context)