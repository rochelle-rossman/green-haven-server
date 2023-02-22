from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Q
from greenhavenapi.models import ProductDesign, Product, Design

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product"""
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description')
        
class DesignSerializer(serializers.ModelSerializer):
    """Serializer for Design"""
    class Meta:
        model = Design
        fields = ('id', 'room', 'style')
        
    def to_representation(self, instance):
        # get the default serialized representation of the instance
        data = super().to_representation(instance)
        data['style'] = dict(Design.STYLE_CHOICES).get(data['style'])
        data['room'] = dict(Design.ROOM_CHOICES).get(data['room'])
        return data
        
class ProductDesignSerializer(serializers.ModelSerializer):
    """Serializer for ProductDesign"""
    design = DesignSerializer()
    product = ProductSerializer()
    class Meta:
        model = ProductDesign
        fields = '__all__'
        
class ProductDesignView(ViewSet):
    """Viewset for ProductDesign"""
    def list(self, request):
        """GET ProductDesigns"""
        style = request.query_params.get('style')
        room = request.query_params.get('room')
        product_designs = ProductDesign.objects.all()
        if room is not None:
            product_designs = ProductDesign.objects.filter(design__room=room)
        if style is not None:
            product_designs = ProductDesign.objects.filter(design__style=style)
        if style and room:
            product_designs = ProductDesign.objects.filter(Q(design__style=style) & Q(design__room=room))
        serializer = ProductDesignSerializer(product_designs, many=True)
        return Response(serializer.data)
      
    def retrieve(self, request, pk):
        """Get single product design"""
        product_design = ProductDesign.objects.get(pk=pk)
        serializer = ProductDesignSerializer(product_design)
        return Response(serializer.data)
      
    def update(self, request, pk):
        """Update single product design"""
        product_design = ProductDesign.objects.get(pk=pk)
        product_design.design = Design.objects.get(pk=request.data["design"])
        product_design.product = Product.objects.get(pk=request.data["product"])
        product_design.save()
        return Response({'success': True}, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk):
        """Delete a product_design from the database"""
        product_design = ProductDesign.objects.get(pk=pk)
        product_design.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
