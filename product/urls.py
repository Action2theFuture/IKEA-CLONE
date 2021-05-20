from django.urls   import path

from product.views import ProductListView, RecommendedView, CategoryView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/category', CategoryView.as_view()), 
    path('/recommendation', RecommendedView.as_view()),
]