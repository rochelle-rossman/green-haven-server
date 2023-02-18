from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
# from django.db.models import Q
from greenhavenapi.models import Product, ProductType

class ProductTypeSerializer(serializers.ModelSerializer):
    """Serializer for Product Types"""
    class Meta:
        model = ProductType
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product"""
    product_type = serializers.SlugRelatedField(
        many=True,
        slug_field='id',
        queryset=ProductType.objects.all()
    )
    
    class Meta:
        model = Product
        fields = '__all__'
        

    def to_representation(self, instance):
        """Filter out fields with null or blank values."""
        # get the default serialized representation of the instance
        data = super().to_representation(instance)
        product_types = instance.product_type.all()
        # return a serialized representation of each related ProductType object that includes both its id and name.
        data['product_type'] = [{'id': pt.id, 'name': pt.name} for pt in product_types]
        # return the human-readable version of the fields with choices based on the Product model
        data['light_level'] = dict(Product.LEVEL_CHOICES).get(data['light_level'])
        data['water_needs'] = dict(Product.LEVEL_CHOICES).get(data['water_needs'])
        data['care_level'] = dict(Product.CARE_CHOICES).get(data['care_level'])
        data['style'] = dict(Product.STYLE_CHOICES).get(data['style'])

        # iterate over each field and only return if the value is not None or blank
        return {key: value for key, value in data.items() if value is not None and value != ''}
      
class ProductView(ViewSet): 
    """ViewSet for Product"""
    def list(self, request):
        """List all products"""
        product_type = request.query_params.get('type')
        queryset = Product.objects.all()
        if product_type:
            queryset = queryset.filter(product_type__name=product_type)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """GET single product"""
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
          
    def update(self, request, pk):
        """Update single product"""
        # Check if product_type field is present in request data
        if 'product_type' not in request.data:
            raise ValidationError({'message': 'product_type is required'})

        # Get the list of primary keys of selected ProductType instances
        product_type= request.data['product_type']
        # Set the product's product_type field to the list of primary keys
        product = Product.objects.get(pk=pk)
        product.product_type.set(product_type)

        # Check for required fields based on product_type
        if 'Houseplants' in request.data.get('product_type', []):
            required_plant_fields = ['care_level', 'water_needs', 'light_level', 'pet_friendly']
            for field in required_plant_fields:
                if field not in request.data:
                    raise ValidationError({'message': f"{field} is required for houseplants"})

        if 'Home/Decor' in request.data.get('product_type', []):
            if 'style' not in request.data or not request.data['style']:
                raise ValidationError({'message': "style is required for home decor"})

        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Creat a new product"""
        try:
            required_fields = ['name', 'description', 'price', 'product_type', 'inventory', 'image_url']
            for field in required_fields:
                if field not in request.data:
                    raise ValidationError({'message': f"{field} is required"})
        
                if request.data["product_type"] == "Houseplant":
                    required_plant_fields = ['care_level', 'water_needs', 'light_level', 'pet_friendly']
                    for field in required_plant_fields:
                        if field not in request.data:
                            raise ValidationError({'message': f"{field} is required for houseplants"})
                
                if request.data["product_type"] == "Home/Decor":
                    if "style" not in request.data or not request.data["style"]:
                        raise ValidationError({'message': "style is required for home decor"})
        
                serializer = ProductSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        """Delete a product"""
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class ProductTypeView(ViewSet):
    """Viewsets for a product type"""
    def list(self, request):
        """List all product types"""
        product_types = ProductType.objects.all()
        serializer = ProductTypeSerializer(product_types, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """GET single product type"""
        product_type = ProductType.objects.get(pk=pk)
        serializer = ProductTypeSerializer(product_type)
        return Response(serializer.data)
