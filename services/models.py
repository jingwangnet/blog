from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(verbose_name="分类名", max_length=20)
    abbr = models.CharField(verbose_name="分类名缩写", max_length=20)
    resume = models.TextField(verbose_name="分类简介")

class Service(models.Model):
    name = models.CharField(verbose_name="服务名", max_length=20)
    category = models.ForeignKey(Category, verbose_name="服务分类", on_delete=models.CASCADE)
    resume = models.TextField(verbose_name="服务简介")
