from django.db              import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    korean_name   = models.CharField(max_length=128)
    english_name  = models.CharField(max_length=128)
    stock         = models.IntegerField(default=0)
    price         = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    special_price = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    is_new        = models.BooleanField(default=False)
    is_online     = models.BooleanField(default=False)
    series        = models.ForeignKey("Series", on_delete=models.CASCADE)
    sub_category  = models.ForeignKey("SubCategory", on_delete=models.CASCADE)
    comment       = models.ManyToManyField("user.User", through="Comment")
    color         = models.ManyToManyField("Color", through="ProductColor", related_name="product")
    backgorund_image = models.ForeignKey("BackgroundImage", on_delete=models.CASCADE, default=1)
    class Meta:
        db_table = "products"

class BackgroundImange(models.Model):
    url     = models.CharField(max_length=2000)

    class Meta:
        db_table = "backgorund_images"


class Series(models.Model):
    korean_name  = models.CharField(max_length=64)
    english_name = models.CharField(max_length=64)

    class Meta:
        db_table = "series"

class Category(models.Model):
    korean_name  = models.CharField(max_length=64)
    english_name = models.CharField(max_length=64)

    class Meta:
        db_table = "category"

class SubCategory(models.Model):
    korean_name  = models.CharField(max_length=64)
    english_name = models.CharField(max_length=64)
    content      = models.TextField(default=None)
    category     = models.ForeignKey("Category", on_delete=models.CASCADE)
    
    class Meta:
        db_table = "sub_category"

class Comment(models.Model):
    content = models.TextField(blank=True, null=True)
    user    = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="user") 
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product")
    rating  = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)], default=0)

    class Meta:
        db_table = "comments"

class Color(models.Model):
    korean_name  = models.CharField(max_length=32)
    english_name = models.CharField(max_length=32)
    
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

class Description(models.Model):
    content   = models.TextField()
    package   = models.TextField()
    material  = models.TextField()
    recycling = models.TextField()
    product   = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "descriptions"