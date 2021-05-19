from django.urls   import path

from order.views import OrderListView, OrderQuantityView

urlpatterns = [
    path('cart', OrderListView.as_view()),
]