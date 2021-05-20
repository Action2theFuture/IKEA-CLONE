from django.urls   import path

from order.views import OrderListView

urlpatterns = [
    path('cart', OrderListView.as_view()),
]