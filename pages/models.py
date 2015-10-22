from django.db import models

from tinymce.models import HTMLField

# Create your models here.

class FAQ(models.Model):
    """
    Model for frequently asked questions
    """
    question = models.TextField(verbose_name="Question")
    answer = models.TextField(verbose_name="Answer")
    created = models.DateField(verbose_name="Created", auto_now=True, blank=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "F.A.Q."
        verbose_name_plural = verbose_name
        ordering = ("created",)


class Pages(models.Model):
    """
    Pages model. For static pages.
    """
    title = models.TextField(verbose_name='Page title')
    content = HTMLField(verbose_name='Page content')
    url = models.SlugField(verbose_name='url', unique=True)
    ceo_keywords = models.TextField(verbose_name='META keywords', null=True, blank=True)
    ceo_description = models.TextField(verbose_name='META description', null=True, blank=True)
    created = models.DateField(auto_now=True, blank=True, verbose_name='Created')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        ordering = ("created",)


class Contacts(models.Model):
    """
    Contacts model. For contact page.
    """
    url = models.SlugField(verbose_name="URL", unique=True)
    phone = models.CharField(max_length=128, verbose_name="Phone")
    address = models.TextField(verbose_name="Address", null=True, blank=True)
    email = models.EmailField(verbose_name="Email")
    map = models.TextField(verbose_name="Map script", blank=True, null=True)
    comments = HTMLField(verbose_name="Comments", null=True, blank=True)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "Contacts"
        verbose_name_plural = verbose_name
