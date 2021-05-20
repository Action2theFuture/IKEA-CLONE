from django.urls   import path

from order.views import OrderListView

urlpatterns = [
    path('', OrderListView.as_view()),
]