from django.urls   import path

from order.views import OrderListView, OrderQuantityView

urlpatterns = [
    path('', OrderListView.as_view()),
]