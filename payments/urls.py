from django.urls import path
from .views import ListOrders, paypalcheck, reset

urlpatterns = [
  path('orders/', ListOrders.as_view()),
  path('reset/', reset, name='reset'),
  path('get-paypal-transaction/', paypalcheck, name='paypalcheck'),
]