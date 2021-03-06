from django.db import models
from django.utils.text import slugify
from pypinyin import lazy_pinyin

# Create your models here.
class Category(models.Model):
    name = models.CharField(verbose_name="分类名", max_length=30, null=False)
    abbr = models.CharField(
        verbose_name="分类名缩写", 
        max_length=20, 
        null=False, 
        unique=True
    )
    resume = models.TextField(verbose_name="分类简介", default='')
    slug = models.SlugField(verbose_name="Slug", null=False, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(lazy_pinyin(self.abbr))
        super(Category, self).save(*args, **kwargs)

class Service(models.Model):
    name = models.CharField(verbose_name="服务名", max_length=20)
    category = models.ForeignKey(Category, verbose_name="服务分类", on_delete=models.CASCADE)
    abbr = models.CharField(
        verbose_name="服务名缩写", 
        max_length=20, 
        null=False, 
        unique=True
    )
    resume = models.TextField(verbose_name="服务简介")
