from django.db      import models

from product.models import Product
from user.models    import User

class Order(models.Model):
    first_name   = models.CharField(max_length=32, default="")
    last_name    = models.CharField(max_length=32, default="")
    address      = models.CharField(max_length=128, default="")
    sub_address  = models.CharField(max_length=128, default="")
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    status       = models.ForeignKey("OrderStatus", default=1 ,on_delete=models.CASCADE)
    order_list   = models.ManyToManyField(Product, through="OrderList", related_name='order')
    
    class Meta:
        db_table = "orders"

class OrderStatus(models.Model):
    status = models.CharField(max_length=32)
    
    class Meta:
        db_table = "order_status"

class OrderList(models.Model):
    quantity = models.IntegerField(default=1)
    order    = models.ForeignKey("Order", on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "order_lists"