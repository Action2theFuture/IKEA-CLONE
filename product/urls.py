from django.urls   import path

from product.views import ProductDetailView

urlpatterns = [
    path('/<int:product_id>', ProductDetailView.as_view()),
]