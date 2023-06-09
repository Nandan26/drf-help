from django.shortcuts import render

from rest_framework.response import Response # for response to client

from rest_framework.decorators import api_view

from products.serializers import ProductSerializer
from products.models import Product

# Create your views here.
# @api_view(["GET"]) # this is api view : REST framework provides an APIView class, which subclasses Django's View class.
# def api_home(request):

#     instance = Product.objects.all().first()

#     data = {}
#     if instance:
#         data = ProductSerializer(instance).data
    
#     return Response(data)
 
@api_view(["POST"]) 
def api_home(request):

    # data  = request.POST or request.data

    # data = request.data

    # validate the data comming with post request using the serializer
    serializer = ProductSerializer(data = request.data)

    # it is based on first the serializers and then on the model likw the required field should be there in post request 
    if serializer.is_valid(raise_exception=True): # for the error message in response 
        # if you dont call save method then two fields defined in the serializer won't be sent back to response and 
        # there will be error object has no attribute get_discount since instance was not created and we can not call instance method 
        # you can avoid this by adding if condition in serializer in get_my_discount method
        # and also without save method there wont be any update in the database
        instance = serializer.save()

        #if without calling the serializer.save() method if we directly call serializer.data then 
        # if (if condition is added in serializer get_my_discount) response will be (title , content ='None' bcz it can be null as we defined in model, my discount) if only title is sent in the request
        # title , content ='None' bcz it can be null as we defined in model, price,my discount) -> if title, price in request 
        # bcz serializer instance is not created and it is not touching the database so it will only return what is specified in request and null fields 
        # my_discount is returned because we define in method that if instance is not created then return None for this field
        return Response(serializer.data)
    
    return Response(data)