from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Document(models.Model):
	content = models.CharField(max_length=200)
	timestamp = models.DateTimeField('Timestamp')
	identifier = models.TextField(default=None, null=True, blank=True)

	def __str__(self):
		return self.content

class FileUpload(models.Model):
	docfile = models.FileField(upload_to='')
	timestamp = models.DateTimeField(default=None, null=True, blank=True)
	content = models.TextField(default=docfile.name, null=True, blank=True)
	identifier = models.TextField(default=None, null=True, blank=True)

	def __str__(self):
		return self.docfile.name