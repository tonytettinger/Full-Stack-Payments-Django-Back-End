from django.shortcuts import render
from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer
import json, requests, datetime

from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

from .paypal import PayPalClient
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from paypalcheckoutsdk.orders import OrdersGetRequest

from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


def reset(query):
    Order.objects.all().delete()
    return HttpResponse('success')

class ListOrders(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class GetOrder(PayPalClient): 
  #2. Set up your server to receive a call from the client
  """You can use this function to retrieve an order by passing order ID as an argument"""   
  def get_order(self, order_id):
    """Method to get order"""
    request = OrdersGetRequest(order_id)
    #3. Call PayPal to get the transaction
    response = self.client.execute(request)
    amount = response.result.purchase_units[0].amount.value
    time = response.result.create_time
    time = datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%SZ")
    new_time_format = "%m/%d/%Y, %H:%M:%S"
    time = time.strftime(new_time_format)
    
    orderid = response.result.id
    #4. Get quote from API
    quote_request = requests.get('https://api.chucknorris.io/jokes/random')
    quote = quote_request.json()['value']
    #4. Save the transaction in your database. Implement logic to save transaction to your database for future reference.
    new_order = Order(quote = quote, time = time, amount = amount, orderid = orderid)
    new_order.save()
    all_orders = Order.objects.all().values()
    orders_list = list(all_orders)
    return orders_list
"""This driver function invokes the get_order function with
   order ID to retrieve sample order details. """
if __name__ == '__main__':
  GetOrder().get_order('REPLACE-WITH-VALID-ORDER-ID')

@api_view(['POST'])
@parser_classes([JSONParser])
def paypalcheck(request, format=None):
    """
    A view that can accept POST requests with JSON content.
    """
    req_data = request.data['data']
    req_json = json.loads(req_data)
    order_id = req_json['orderID']
    order = GetOrder().get_order(order_id)
    print(order)
    print(type(order))
    return JsonResponse({'orders': order})