from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(verbose_name="分类名", max_length=20)
    abbr = models.CharField(verbose_name="分类名缩写", max_length=20)
    resume = models.TextField(verbose_name="分类简介")

class Service(models.Model):
    name = models.CharField(verbose_name="服务名", max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
