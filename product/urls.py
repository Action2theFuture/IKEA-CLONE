from django.urls   import path

from product.views import ProductDetailView

urlpatterns = [
    path('/detail/', ProductDetailView.as_view()),
]