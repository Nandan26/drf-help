from rest_framework import serializers
from .models import Product

from api.serializers import UserPublicSerializer

from .validators import validate_title
# for adding url field on each instance fot better routing
from rest_framework.reverse import reverse
# You can have mulitple serializers for one model

# read_only = True  : - True to ensure that the field is used when serializing a representation, but is not used when creating or updating an instance during deserialization
# write_only = True : - True to ensure that he field may be used when updating or creating an instance, but is not included when serializing the representation in GET request.

class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True) # convert get_discount field to my_discount on response
    # edit_url = serializers.SerializerMethodField(read_only=True) 
    
    # other way to show url
    # url = serializers.HyperlinkedIdentityField(
    #         view_name='product-detail',
    #         lookup_field='pk',
    #         read_only=True
    # )

    # email = serializers.EmailField(write_only=True) # required in post request and this field is not seen in get 
    # it can throw error since email field is write but not defined in model so we need to overrride create method
    # you can do this in view also 

    # owner maps to user now if you use owner in fields and make changes in it: it will be updated in database also 
    # but in databse/model the field name will be user and here it is changed to user
    owner = UserPublicSerializer(source='user', read_only=True)
    # name = serializers.CharField(read_only=True, source = 'user.name') if our model had foreign key for user than we can set name field equal to user name field automatically

    class Meta:
        model = Product
        # field you want to serialize
        # fields= [ 
        #     'title',
        #     'content',
        #     'price',
        #     'sale_price', # you can directly use additional field (property) here
        #     'get_discount', # or any instance method as well
        # ]

        fields= [
            # 'url', 
            # 'email',
            # 'edit_url',
            'owner',
            'title',
            'content',
            'price',
            # 'user', we can directly fetch it from request 
            'sale_price',
            'my_discount',# now get_discount has changed to my_discount in response
            # 'name' 
        ]

    # validation using django serializers
    # def validate_title(self, value):
    #     q = Product.objects.filter(title__exact=value)

    #     if q.exists():
    #         raise ValidationError(f"{value} title already exists")

    #     return value

    # or you can achieve custome validation by using below method
    title = serializers.CharField(validators = [validate_title])

    # override the default model object create method
    # def create(self, validated_data):

    #     email = validated_data.pop('email') # get the email and pop it from data
    #     obj = super().create(validated_data)
    #     print(email, obj) # do whatever you want to do with this email
    #     return obj

    # def update(self, instance, validated_data):
    #     email = validated_data.pop('email') 
    #     # instance.title = validated_data.get('title')

    #     # return instance
    #     return super().update(instance, validated_data)
    
    def get_my_user_data(self, obj):
        return {
            "username": obj.user.username
        }
    
    def get_edit_url(self,obj):
        # return f"api/v2/products/{obj.pk}/" Not good s.t. we change v2 to v3 then need to change everywhere so better not to do it

        request = self.context.get('request')

        if request is None:
            return None

        # reverse function is used to return a fully qualified URL, using the request to determine the host and port. so it can be used as model field
        return reverse("product-update", kwargs={'pk': obj.pk}, request=request)
        # in model instance in response it shows http://127.0.0.1:8000/api/products/1/update/


    # to convert model field to other field in serializer and sent it in response : in model : get_discount in response : my_discount
    def get_my_discount(self,obj):
        # below two ways are to check if instance is not created return None for this field
        # if not hasattr(obj, 'id'):
        #     return None
        if not isinstance(obj, Product):
            return None

        #obj is instance of Product 
        return obj.get_discount()
        
