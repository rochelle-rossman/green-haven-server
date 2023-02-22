from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from greenhavenapi.models import Design, Product, ProductDesign

class DesignSerializer(serializers.ModelSerializer):
    """JSON serializer for design"""
    products = serializers.SerializerMethodField()
    class Meta:
        model = Design
        fields = '__all__'
        
    def to_representation(self, instance):
        """Return the human readable choice"""
        # get the default serialized representation of the instance
        data = super().to_representation(instance)
        data['room'] = dict(Design.ROOM_CHOICES).get(data['room'])
        data['style'] = dict(Design.STYLE_CHOICES).get(data['style'])
        return data
    
    def get_products(self, obj):
        """Get a list of products associated with the design object"""
        products_list = []
        for product in obj.products.all():
            try:
                ProductDesign.objects.get(design=obj, product=product)
                products_list.append({"id": product.id,"name": product.name, "price": product.price})
            except ProductDesign.DoesNotExist:
                pass
        return products_list
          
        
class DesignView(ViewSet):
    """ViewSet for design"""
    def list(self, request):
        """GET list of designs"""
        style = request.query_params.get('style')
        room = request.query_params.get('room')
        designs = Design.objects.all()
        if style:
            designs = designs.filter(style=style)
        elif room:
            designs = designs.filter(room=room)
        elif style and room:
            designs = designs.filter(Q(style=style) & Q(room=room))
        serializer = DesignSerializer(designs, many=True)
        return Response(serializer.data)
      
    def retrieve(self, request, pk):
        """GET single design"""
        try:
            design = Design.objects.get(pk=pk)
            serializer = DesignSerializer(design)
            return Response(serializer.data)
        except Design.DoesNotExist:
            return Response({'message': 'No such design'}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk):
        """Update design"""
        design = Design.objects.get(pk=pk)
        design.room = request.data["room"]
        design.style = request.data["style"]
        design.image_url = request.data["image_url"]
        product_ids = request.data["products"]
        if not isinstance(product_ids, list):
            raise ValidationError({"message": "products field must be a list"})
          
        for product in product_ids:
            if 'id' not in product:
                raise ValidationError({"message": "products field must contain id"})
            try:
                product = Product.objects.get(id=product["id"])
            except Product.DoesNotExist:
                return Response({'message': f"Product {product['id']} does not exist"}, status=status.HTTP_404_NOT_FOUND)
              
        products = Product.objects.filter(id__in=[product['id'] for product in product_ids])
        product_design = ProductDesign.objects.filter(design=design)
        
        for product in products:
            product_design, created = ProductDesign.objects.get_or_create(design=design, product=product)
            if not created:
                continue
            product_design.save()
        design.save()
        return Response({'message': 'Design updated'}, status=status.HTTP_202_ACCEPTED)
      
    def create(self, request):
        """Create a new Design"""
        style = request.data["style"]
        room = request.data["room"]
        products = request.data["products"]
        image_url = request.data["image_url"]
        
        design = Design.objects.create(style=style, room=room, image_url=image_url)
        
        product_list = []
        for product in products:
            try:
                product_obj = Product.objects.get(id=product['id'])
            except Product.DoesNotExist:
                return Response({"message": f"Product {product['id']} does not exist"})
            ProductDesign.objects.create(product=product_obj, design=design)
            product_list.append(product_obj)
            serializer = DesignSerializer(design)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
      
    def destroy(self, request, pk):
        """Delete a Design"""
        design = Design.objects.get(pk=pk)
        design.delete()
        return Response({'message': 'Design deleted'}, status=status.HTTP_204_NO_CONTENT)
      
      
        
        
