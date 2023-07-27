from django.db import models

class Product(models.Model):
  description = models.CharField(max_length=200)
  password = models.CharField(max_length=10)
  pdffile = models.FileField(upload_to ='product/')
  