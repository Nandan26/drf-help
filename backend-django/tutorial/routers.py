# different method to do routing 
# now we can route easily it is just different way to use urlpatterns
# home page will have localhost:8000/api/v2/ :- product route link and by clicking that ProductViewSet will be called 
# localhost:8000/api/v2/products/
# and all the product will be listed and also you can perform post or update / delete on one single product 
# localhost:8000/api/v2/products/1

from rest_framework.routers import DefaultRouter

from products.viewsets import ProductViewSet, ProductGenericViewSet

router = DefaultRouter()

# router.register('products', ProductViewSet, basename = 'products')

#only two endpoints list and individual get object
router.register('products', ProductGenericViewSet, basename = 'products')

urlpatterns = router.urls 