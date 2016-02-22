from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.exceptions import ValidationError

from .forms import UploadForm
from .models import FileUpload
from .models import Document

from django.conf import settings

def index(request):
	latest_docs = Document.objects.order_by('-timestamp')[:10]
	form = UploadForm()
	context = {
		'latest_docs' : latest_docs,
		'form' : form
	}
	if request.method == 'GET':
		search_query = request.GET.get('search_id', None)
		upload_query = request.GET.get('upload_query', None)
		if search_query:
			doc = get_object_or_404(Document, pk=search_query)
			context = {
				'doc': doc
			}
			return render(request, 'details.html', context)
		if upload_query:
			new_doc = Document(content=upload_query, timestamp=timezone.now())
			new_doc.save()
			return HttpResponseRedirect('/')

	if request.method == 'POST':
		if request.FILES['docfile'].__str__().split(".")[1] not in settings.ALLOWED_UPLOAD_FORMATS:
			raise ValueError('This format is not allowed.')
		if request.FILES['docfile'].size > settings.UPLOAD_SIZE_LIMIT:
			raise ValueError("The size of your upload is too large.")

		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			new_doc = FileUpload(docfile=request.FILES['docfile'])
			new_doc.save()
			return HttpResponseRedirect('/')

	return render(request, 'index.html', context)

def details(request, doc_id):
	doc = get_object_or_404(Document, pk=doc_id)
	context = {
		'doc': doc
	}
	return render(request, 'details.html', context)