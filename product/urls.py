from django.urls   import path

from product.views import MainView, SubCategoryView, ProductListView, ProductDetailView, FilterSortView

urlpatterns = [
    path('/p/<str:product_name>', ProductDetailView.as_view()),
]