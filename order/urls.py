from django.urls   import path

from order.views import CartView

urlpatterns = [
    path('', CartView.as_view()),
]