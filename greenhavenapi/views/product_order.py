from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from greenhavenapi.models import ProductOrder, Product, Order, User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for users"""
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'street_address', 'city', 'state', 'zipcode')

class ProductSerializer(serializers.ModelSerializer):
    """JSON serializer for Product"""
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'image_url', 'product_type')
        
        
class OrderSerializer(serializers.ModelSerializer):
    """JSON serializer for Order"""
    customer = UserSerializer()
    class Meta:
        model = Order
        fields = '__all__'

class ProductOrderSerializer(serializers.ModelSerializer):
    """Serializer for ProductOrder"""
    product = ProductSerializer()
    order = OrderSerializer()
    class Meta:
        model = ProductOrder
        fields = ('id', 'product', 'order', 'quantity')
        
class ProductOrderView(ViewSet):
    """Viewsets for ProductOrder"""
    def list(self, request):
        """GET product orders"""
        product = request.query_params.get('product')
        order = request.query_params.get('order')
        customer = request.query_params.get('customer')
        order_status = request.query_params.get('status')
        product_orders = ProductOrder.objects.all()
        if order_status is not None:
            product_orders = product_orders.filter(order__status=order_status)
        if product is not None:
            product_orders = product_orders.filter(product=product)
        if order is not None:
            product_orders = product_orders.filter(order=order)
        if customer is not None:
            product_orders = product_orders.filter(order__customer=customer)
        serializer = ProductOrderSerializer(product_orders, many=True)
        return Response(serializer.data)  

    def update(self, request, pk):
        """Update a productOrder"""
        product_order = ProductOrder.objects.get(pk=pk)
        product_order.product = Product.objects.get(pk=request.data["product"])
        product_order.order = Order.objects.get(pk=request.data['order'])
        product_order.quantity = request.data["quantity"]
        product_order.save()
        return Response({'success': True}, status=status.HTTP_202_ACCEPTED)
      
    def destroy(self, request, pk):
        """Delete a productOrder"""
        product_order = ProductOrder.objects.get(pk=pk)
        product_order.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
