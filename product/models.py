from django.db import models
from user.models import User

class Product(models.Model):
    price         = models.DecimalField(10,2, default=0)
    special_price = models.DecimalField(10,2, default=None)
    is_new        = models.BooleanField(default=False)
    is_online     = models.BooleanField(default=False)
    description   = models.TextField()
    series        = models.ForeignKey("Series", on_delete=models.CASCADE)
    sub_category  = models.ForeignKey("SubCategory", on_delete=models.CASCADE)
    comment       = models.ManyToManyField(User, through="Comment")
    color         = models.ManyToManyField("Color", through="ProductColor")
    
    class Meta:
        db_table = "products"

class Series(models.Model):
    name = models.CharField(max_length=64)
    
    class Meta:
        db_table = "series"

class SubCategory(models.Model):
    name     = models.CharField(max_length=64)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    
    class Meta:
        db_table = "sub_category"

class Comment(models.Model):
    content  = models.TextField()
    user     = models.ForeignKey(User, on_delete=models.CASCADE) 
    product  = models.ForeignKey("Product", on_delete=models.CASCADE)
    
    class Meta:
        db_table = "comments"

class Color(models.Model):
    name  = models.CharField(max_length=32)
    
    class Meta:
        db_table = "colors"

class ProductColor(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    color   = models.ForeignKey("Color", on_delete=models.CASCADE)
    
    class Meta:
        db_table = "product_color"

class Image(models.Model):
    url     = models.CharField(max_length=2000)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    
    class Meta:
        db_table = "images"