from rest_framework import generics, mixins, permissions, authentication
from .serializers import ProductSerializer
from .models import Product

from api.permissions import IsStaffEditorPermission
from api.authentication import TokenAuthentication
from api.mixins import (StaffEditorPermissionMixin,UserQuerySetMixin) 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# CreateAPIView --> only post 
# ListCreateAPIView --> get -> retrieve all data & post
# RetrieveAPIView --> Get
# UpdateAPIView --> put
# DestroyAPIView --> delete

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    #  even if this method is not defined then data will be saved in database this is usefull to alter some fields
    def perfrom_create(self,serializer):
        # this method will always called if some hits post request
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)

#this will show listof all products along with way to send post request so no need to use ListView
class ProductListCreateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #permissions & authentication
    
    # authentication_classes = [authentication.SessionAuthentication]
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication    
    ]


    # permission_classes = [permissions.IsAuthenticated] #inbuilt
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly] #inbuilt
    # permission_classes = [IsStaffEditorPermission] 
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] can have mulitple classes as wellthe first come first evaluated
    # With DjangoModelPermissions there is no restriction on view so that's why we need custome persmission
    # permission_classes = [permissions.DjangoModelPermissions] # if use this then it will check permissions given by admin
    #  even if this method is not defined then data will be saved in database this is usefull to alter some fields
    # here we have inherited permissionclassmixin so no need to write permission_classes
    
    def perfrom_create(self,serializer):
        # email = serializer.validated_data.pop('email')

        # this method will always called if some hits post request
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title

        #  it will call create method on serializer if instance is not already created otherwise it will call update
        serializer.save(user = self.request.user ,content=content)

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs) # -> Product.objects.all()
    #     request = self.request 
    #     user = request.user # get the user from the request
    #     if not user.is_authenticated: # return empty list if user is not authenticated
    #         return Product.objects.none()
    #     # print(request.user)
    #     return qs.filter(user=request.user) # return queryset with instance having user as current user




class ProductUpdateAPIView(StaffEditorPermissionMixin,generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

class ProductDestroyAPIView(StaffEditorPermissionMixin,generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        # instance 
        super().perform_destroy(instance)

# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

class ProductDetailAPIView(StaffEditorPermissionMixin,generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # by default it is pk if you not specified other
    # lookup_field = 'pk' # similar to Product.objects.get(pk = 1) or pk=2 lookup based on pk field

    # note : Note that when using hyperlinked APIs you'll need to ensure that both the API views and the serializer classes set the lookup fields if you need to use a custom value.

# list and single object view using function view
@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method  

    if method == "GET":
        if pk is not None:
            # detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        # list view
        queryset = Product.objects.all() 
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == "POST":
        # create an item
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"invalid": "not good data"}, status=400)

# ListModelMixin
# Provides a .list(request, *args, **kwargs) method, that implements listing a queryset.
# CreateModelMixin
# Provides a .create(request, *args, **kwargs) method, that implements creating and saving a new model instance.
# RetrieveModelMixin
# Provides a .retrieve(request, *args, **kwargs) method, that implements returning an existing model instance in a response.
# UpdateModelMixin
# Provides a .update(request, *args, **kwargs) method, that implements updating and saving an existing model instance.
# DestroyModelMixin
# Provides a .destroy(request, *args, **kwargs) method, that implements deletion of an existing model instance.

# similar to product_alt_view : All different views can be handled in GenericAPIView : it can also do update and destroy
class ProductMixinView(StaffEditorPermissionMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs): #HTTP -> get
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs) # return one particular instance with id = pk
        return self.list(request, *args, **kwargs) #this is comming from ListModelmixin if pk is not specified return all objects

    def post(self, request, *args, **kwargs): #HTTP -> Post
        return self.create(request, *args, **kwargs)
    
    # it can override all methods available in createapiview because it extends genericAPIView and createmodelmixin only 
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = "this is a single view doing cool stuff"
        serializer.save(content=content)
