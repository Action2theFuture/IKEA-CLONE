import json

from django.views import View
from django.http  import JsonResponse
from django.http  import HttpResponseRedirect

from order.models   import OrderList, Order
from product.models import Product

class OrderListView(View):
    def get(self,request):
        user           = request.user
        orders         = Order.objects.filter(user=user)
        order_products = []
        total_order_price = 0
        for order in orders: 
            order_list = OrderList.objects.filter(order=order)
            for order_product in order_list: 
                product = order_product.product
                order_products.append(
                    order_product.id,
                    product.english_name,
                    product.korean_name,
                    product.sub_category,
                    product.price
                )
                total_order_price += product.price * order_product.quantity
        return JsonResponse({'order_list':order_list , 'total_order_price':total_order_price}, status=200)

class OrderQuantityView(View):
    def post(self,request):
        try:
            data           = json.loads(request.body)
            orderlist_id   = data['order_product_id']
            quantity       = data['quantity']
            order          = OrderList.objects.get(id = orderlist_id)
            order.quantity = quantity
            return HttpResponseRedirect('/orderlist')
        except KeyError:
            JsonResponse({'message':'KEY_ERROR'}, status=400)

    