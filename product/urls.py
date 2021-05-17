from django.urls   import path

from product.views import CategoryView

urlpatterns = [
   path('/category', CategoryView.as_view()), 
]
