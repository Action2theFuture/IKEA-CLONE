from django.views     import View
from django.http      import JsonResponse
from django.db.models import F, Sum


from order.models   import OrderList, Order, User
from user.utils     import authorize

class OrderListView(View):
    @authorize
    def get(self,request):
        user          = request.user
        order_list_id = request.GET.get('order_id', None)
        quantity      = request.GET.get('quantity', 1)

        if order_list_id and quantity:
            order_product          = OrderList.objects.get(id
            =order_list_id)
            order_product.quantity = quantity

        orders            = user.order.all()
        order_list        = OrderList.objects.filter(order__in=orders)

        order_products = [
            {
                'id'          : order.product.id,
                'english_name': order.product.english_name,
                'korean_name' : order.product.korean_name,
                'sub_category': order.product.sub_category.korean_name,
                'price'       : order.product.price,
                'url'         : order.product.image.all().first().url
            }
            for order in order_list]

        order_list_qs     = order_list.annotate(price=F('product__price')*F('quantity'))
        total_order_price = order_list_qs.aggregate(total_price=Sum('price'))['total_price']

        return JsonResponse({'order_list':order_products , 'total_order_price':total_order_price}, status=200)
    