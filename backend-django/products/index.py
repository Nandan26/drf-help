from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register


from .models import Product


@register(Product)
class ProductIndex(AlgoliaIndex):
    # should_index = 'is_public' #show only if is public == True
    # field that you want to display in query result and it is fetched by 3rd party api so they have access to this field 
    fields = [
        'title',
        'price',
        'user',
        'public',
        'path',
        'get_absolute_url',
    ]
    settings = {
        'searchableAttributes': ['title', 'body'],
        'attributesForFaceting': ['user', 'public'] # For filtering cannot be used in search
    }
    tags = 'get_tags_list'