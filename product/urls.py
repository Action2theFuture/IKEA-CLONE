from django.urls import path

from product.views import ProductMainView, SubCategoryView, ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductMainView.as_view()),
    path('/<str:category_name>', SubCategoryView.as_view()),
    path('/cat/<str:sub_category_name>', ProductListView.as_view()),
    path('/p/<str:product_name>', ProductDetailView.as_view()),
]