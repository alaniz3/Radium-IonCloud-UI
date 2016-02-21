from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Document

def index(request):
	latest_docs = Document.objects.order_by('-timestamp')[:10]
	context = {
		'latest_docs' : latest_docs,
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

	return render(request, 'index.html', context)

def details(request, doc_id):
	doc = get_object_or_404(Document, pk=doc_id)
	context = {
		'doc': doc
	}
	return render(request, 'details.html', context)