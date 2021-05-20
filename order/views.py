import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import F, Sum

from order.models   import OrderList
from user.utils     import authorize

class OrderListView(View):
    @authorize
    def get(self,request):
        user       = request.user
        orders     = user.order.all()
        order_list = OrderList.objects.filter(order__in=orders)
        
        order_products = [
            {
                'order_id'    : order.id,
                'id'          : order.product.id,
                'english_name': order.product.english_name,
                'korean_name' : order.product.korean_name,
                'sub_category': order.product.sub_category.korean_name,
                'price'       : int(order.product.price),
                'url'         : order.product.image.all().first().url,
                'quantity'    : order.quantity
            }
            for order in order_list]

        order_list_qs     = order_list.annotate(price=F('product__price')*F('quantity'))
        total_order_price = order_list_qs.aggregate(total_price=Sum('price'))['total_price']

        return JsonResponse({'order_list':order_products , 'total_order_price':total_order_price}, status=200)

    def fetch(self, request):
        data = json.loads(request.body)
        try:
            order_id               = data['order_id']
            quantity               = data['quantity']
            order_product          = OrderList.objects.get(id=order_id)
            order_product.quantity = quantity
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)