from django.urls   import path

from product.views import Main, Category

urlpatterns = [
   path('/category', Category.as_view()), 
]
