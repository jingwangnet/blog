from django.db import models

# Create your models here.
class Service(models.Model):
    name = models.CharField(verbose_name="服务名", max_length=20)
