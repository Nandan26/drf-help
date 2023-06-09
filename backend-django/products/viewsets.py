from rest_framework import mixins, viewsets

from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    '''
    get -> list -> Queryset
    get -> retrieve -> Product Instance Detail View
    post -> create -> New Instance
    put -> Update
    patch -> Partial UPdate
    delete -> destroy 
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk' # default

#  only get methods are allowed
class ProductGenericViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    '''
    get -> list -> Queryset
    get -> retrieve -> Product Instance Detail View 
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk' # default

# this can be called inside the urlpatters as normal function based views product_list_view, product_detail_view
# product_list_view = ProductGenericViewSet.as_view({'get': 'list'})
# product_detail_view = ProductGenericViewSet.as_view({'get': 'retrieve'})