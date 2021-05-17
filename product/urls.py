from django.urls   import path

from product.views import ProductListView

urlpatterns = [
    path('/cat/<str:sub_category_name>', ProductListView.as_view()),
]    