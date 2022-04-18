from django.db import models

# Create your models here.
class Category(models.Model):
    pass

class Service(models.Model):
    name = models.CharField(verbose_name="服务名", max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
