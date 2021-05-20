import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import F, Sum

from order.models   import OrderList
from user.utils     import authorize

class CartView(View):
    @authorize
    def get(self,request):
        cart_list = OrderList.objects.filter(order__status__status="결제대기", order__user=request.user)
        
        order_products = [
            {
                'cart_id'    : cart.id,
                'id'          : cart.product.id,
                'english_name': cart.product.english_name,
                'korean_name' : cart.product.korean_name,
                'sub_category': cart.product.sub_category.korean_name,
                'price'       : int(cart.product.price),
                'url'         : cart.product.image.all().first().url,
                'quantity'    : cart.quantity
            }
            for cart in cart_list]

        cart_list_query_set = cart_list.annotate(price=F('product__price')*F('quantity'))
        total_order_price   = cart_list_query_set.aggregate(total_price=Sum('price'))['total_price']

        return JsonResponse({'order_list':order_products , 'total_order_price':total_order_price}, status=200)

    def petch(self, request):
        data = json.loads(request.body)
        try:
            cart_id               = data['cart_id']
            quantity              = data['quantity']
            cart_product          = OrderList.objects.get(id=cart_id)
            cart_product.quantity = quantity
            cart_product.save()
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except OrderList.DoesNotExist:
            return JsonResponse({'message': 'NOT_FOUND'}, status=404)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)