from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from greenhavenapi.models import Order, ProductOrder, PaymentMethod, Product, User

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Orders"""
    payment_method = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = '__all__'
        
    def get_customer(self, obj):
        """Returns only certain values to represent the associated customer"""
        return {"first_name": obj.customer.first_name, "last_name": obj.customer.last_name, "email": obj.customer.email
    }
    def get_payment_method(self, obj):
        """Returns the payment method label only"""
        if obj.payment_method is None:
            return None
        label = obj.payment_method.label
        return {"label": label}
    
    def get_products(self, obj):
        """Get a list of products associated with the order object"""
        products_list = []
        for product in obj.products.all():
            try:
                product_order = ProductOrder.objects.get(order=obj, product=product)
                products_list.append({"name": product.name, "quantity": product_order.quantity, "price": product.price})
            except ProductOrder.DoesNotExist:
                pass
        return products_list
        
    def get_total(self, obj):
        """Calculates the total for the order"""
        total = 0
        for product in obj.products.all():
            try:
                product_order = ProductOrder.objects.get(order = obj, product = product)
                total += product_order.quantity * product.price
            except ProductOrder.DoesNotExist:
                pass
        return total
      
    def to_representation(self, instance):
        """Filter out fields with null or blank values."""
        # get the default serialized representation of the instance
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value is not None and value != ''}
      
      
class OrderView(ViewSet):
    """ViewSet for Order"""
    def list(self, request):
        """Returns a list of orders"""
        customer = request.query_params.get("customer")
        orders = Order.objects.all()
        if customer:
            orders = orders.filter(customer=customer)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
      
    def retrieve(self, request, pk):
        """Get a single order"""
        try:
            order = Order.objects.get(pk=pk)
            serialzer = OrderSerializer(order)
            return Response(serialzer.data)
        except Order.DoesNotExist:
            return Response({'message': 'No such order'}, status=status.HTTP_404_NOT_FOUND)
          
    def update(self, request, pk):
        """Update an existing order"""
        # Check if the order exists
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'message': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)
        # When the order's status is updated to 'completed', add the date to the ordered_on field  
        order.status = request.data["status"]
        if order.status == 'completed' and order.ordered_on is None:
            order.ordered_on = timezone.now().date()
        if request.data.get("payment_method"):
            try:
                payment_method = PaymentMethod.objects.get(id=request.data["payment_method"])
                order.payment_method = payment_method
            except PaymentMethod.DoesNotExist:
                return Response({'message': 'PaymentMethod does not exist'}, status=status.HTTP_404_NOT_FOUND)
        # If there is no payment_method in the request data, set the payment_method to None
        else:
            order.payment_method = None
        # Get the product ids from the order's product information and validate the field is a list
        product_ids = request.data["products"]
        if not isinstance(product_ids, list):
            raise ValidationError({"message": "products field must be a list"})
        # Loop through the product ids to get the quantity
        for product in product_ids:
            if 'id' not in product or 'quantity' not in product:
                raise ValidationError({"message": "products field must contain id and quantity"})
            try:
                product = Product.objects.get(id=product["id"])
            except Product.DoesNotExist:
                return Response({'message': f"Product {product['id']} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        products = Product.objects.filter(id__in=[product['id'] for product in product_ids])
        product_orders = ProductOrder.objects.filter(order=order)
        for product_order in product_orders:
        # Update the quantity of each product order
        # The next function is used to retrieve the first item from an iterable
            product_order.quantity = next((product['quantity'] for product in product_ids if product['id'] == product_order.product.id), 0)
            # If the updated quantity is None, delete the product order
            if product_order.quantity is None:
                product_order.delete()
            else:
            # Save the updated product order
                product_order.save()

        for product in products:
            # Get or create the product order associated with the order and product
            product_order, created = ProductOrder.objects.get_or_create(order=order, product=product)
            if not created:
                continue
            product_order.quantity = next((product['quantity'] for product in product_ids if product['id'] == product_order.product.id), 0)
            product_order.save()
        order.save()
        return Response({'message': 'Order Updated successfully', 'data': OrderSerializer(order).data})
      
    def create(self, request):
        """Create a new order"""
        products = request.data.get('products')
        customer = User.objects.get(id=request.data["customer"])
        payment_method = PaymentMethod.objects.get(pk=request.data["payment_method"])
        order_status = 'in-progress'
        if 'status' in request.data:
            order_status = request.data['status']
        if order_status != 'in-progress':
            try:
                payment_method = PaymentMethod.objects.get(pk=request.data["payment_method"])
            except PaymentMethod.DoesNotExist:
                return Response({"message": "Invalid payment_method id"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            payment_method = None
            
        order = Order.objects.create(customer=customer, payment_method=payment_method)
        total = 0
        product_list = []
        for product in products:
            try:
                product_obj = Product.objects.get(id=product["id"])
            except Product.DoesNotExist:
                return Response({"message": f"Product {product['id']} does not exist"})
            product_obj.deduct_from_inventory(product['quantity'])
            ProductOrder.objects.create(product=product_obj, order=order, quantity=product['quantity'])
            product_list.append(product_obj)
            total += product_obj.price * product['quantity']
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        """Delete order"""
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response({"status": status.HTTP_204_NO_CONTENT})
