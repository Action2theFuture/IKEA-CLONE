from django.views     import View
from django.http      import JsonResponse
from django.db.models import F, Sum


from order.models   import OrderList
from user.models    import User
from user.utils     import authorize

class OrderListView(View):
    @authorize
    def get(self,request):
        user          = request.user
        order_list_id = request.GET.get('order_id', None)
        quantity      = request.GET.get('quantity', 1)
        if order_list_id and quantity:
            order_product          = OrderList.objects.get(id=order_list_id)
            order_product.quantity = quantity
        
        orders            = user.order.all()
        order_list        = [OrderList.objects.get(order=order) for order in orders]
        order_products    = []
        total_order_price = 0

        for order in order_list:
            product = order.product
            order_products.append(
                    {
                        'id'          : product.id,
                        'english_name': product.english_name,
                        'korean_name' : product.korean_name,
                        'sub_category': product.sub_category.korean_name,
                        'price'       : product.price,
                        'url'         : product.image.all().first().url
                    }
                )
            total_order_price += product.price * order.quantity
        
        return JsonResponse({'order_list':order_products , 'total_order_price':total_order_price}, status=200)
    