from django.urls   import path

from product.views import ProductListView

urlpatterns = [
    path('', ProductListView.as_view()),
]    