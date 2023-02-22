"""greenhaven URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from greenhavenapi.views import check_user, register_user, UserView, ProductView, ProductTypeView, OrderView, DesignView, PaymentMethodView, ProductOrderView, ProductDesignView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, 'user')
router.register(r'products', ProductView, 'product')
router.register(r'product_types', ProductTypeView, 'product_type')
router.register(r'orders', OrderView, 'order')
router.register(r'designs', DesignView, 'design')
router.register(r'payment_methods', PaymentMethodView, 'payment_method')
router.register(r'product_orders', ProductOrderView, 'product_orders')
router.register(r'product_designs', ProductDesignView, 'product_design')

urlpatterns = [
    path('register', register_user),
    path('checkuser', check_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
