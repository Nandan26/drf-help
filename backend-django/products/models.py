from django.db import models
from django.conf import settings
from django.db.models import Q

import random

TAGS_MODEL_VALUES = ['electronics', 'cars', 'boats', 'movies', 'cameras']

# Create your models here.
User = settings.AUTH_USER_MODEL

# return Product.objects.filter(public = True).filter(title__icontains='hello') below two class does exact same as this query

# class ProductQuerySet(models.QuerySet):
#     def is_public(self):
#         return self.filter(public=True)
    
#     def search(self, query, user=None):
#         return self.filter(title__icontains='hello')

#  If you need to execute more complex queries (for example, queries with OR statements), you can use Q objects.

# A Manager’s base QuerySet returns all objects in the system
# You can override a Manager’s base QuerySet by overriding the Manager.get_queryset() method.
# get_queryset() should return a QuerySet with the properties you require.
# now Product.objects.all() not return all object but only objects that are defined in the get_queryset() method.

#below two class are for the query search functionalities
class ProductManager(models.Manager):
    def get_queryset(self, *args,**kwargs):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        
        return self.get_queryset().is_public().search(query)

class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs


class Product(models.Model):

    user = models.ForeignKey(User, null = True, default = 1 , on_delete = models.SET_NULL)
    title = models.CharField(max_length=150)
    content = models.TextField(blank = True,null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=10.00)
    public = models.BooleanField(default=True)

    #custom manager
    objects = ProductManager()

    def is_public(self) -> bool:
        return self.public

    #with this decorator you can call this method as variable ex. product.sale_price() -> product.sale_price
    @property #this field are calculated based on the some fields of models and they are not stored every time we access them they are calculated
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)
        
    # fir this method you need to call :- product.get_discount()
    def get_discount(self):
        return "55%"

    def get_absolute_url(self):
        return f"/api/products/{self.pk}/"
        
    @property
    def path(self):
        return f"/products/{self.pk}/"

    def get_tags_list(self):
        return [random.choice(TAGS_MODEL_VALUES)]
