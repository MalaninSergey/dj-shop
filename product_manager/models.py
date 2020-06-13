from django.urls import reverse
from django.utils.encoding import iri_to_uri
from django_extensions.db.fields import AutoSlugField
from django.db.models import *
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models
from django_extensions.db import fields as extension_fields


class Product(models.Model):
    # Fields
    name = models.CharField(max_length=155)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    description = models.TextField(max_length=250)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    in_or = models.BooleanField(default=False)

    # Relationship Fields
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='category'
    )

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return u'%s' % self.name

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('product_manager_product_detail', args=(self.slug,))

    def rm(self):
        self.in_or = False
        self.save()
        return iri_to_uri('/orders/')

    def set_to_or(self):
        self.in_or = True
        self.save()
        return iri_to_uri('/')

    def get_delete_url(self):
        return reverse('product_manager_product_delete', args=(self.slug,))


class Category(models.Model):
    # Fields
    name = models.CharField(max_length=155)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return u'%s' % self.name

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('product_manager_category_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('product_manager_category_update', args=(self.slug,))
