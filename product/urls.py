from django.urls   import path

from product.views import ProductListView

urlpatterns = [
    path('/list/', ProductListView.as_view()),
]    