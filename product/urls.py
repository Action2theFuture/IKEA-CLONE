from django.urls   import path

from product.views import ProductDetailView

urlpatterns = [
    path('/<int:pk>', ProductDetailView.as_view()),
]