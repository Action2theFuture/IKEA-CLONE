from django.urls   import path

from order.views import OrderListView, OrderQuantityView

urlpatterns = [
    path('product', OrderListView.as_view()),
]