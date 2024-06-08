from django.db import models

# Create your models here.
class File(models.Model):
    file = models.FileField(upload_to='files/')
    uploaded_ad = models.DateTimeField(auto_now_add=True)

