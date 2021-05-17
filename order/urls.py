from django.urls   import path

from order.views import OrderListView, OrderQuantityView

urlpatterns = [
    path('/orderlist', OrderListView.as_view()),
    path('/quantity', OrderQuantityView.as_view())
]