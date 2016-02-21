from __future__ import unicode_literals

from django.db import models

class Document(models.Model):
	content = models.CharField(max_length=200)
	timestamp = models.DateTimeField('Timestamp')

	def __str__(self):
		return self.content