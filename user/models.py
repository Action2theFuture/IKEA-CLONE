from django.db import models

class User(models.Model):
    email        = models.EmailField(max_length=128, unique=True)
    first_name   = models.CharField(max_length=32)
    last_name    = models.CharField(max_length=32)
    password     = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=32, unique=True)
    birthday     = models.CharField(max_length=32)
    create_at    = models.DateTimeField(auto_now_add=True)
    update_at    = models.DateTimeField(auto_now=True)
    wish_list    = models.ManyToManyField("product.Product", through="WishList", related_name="user")

    class Meta:
        db_table = "users"

class WishList(models.Model):
    user    = models.ForeignKey("User", on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    
    class Meta:
        db_table = "wish_list"