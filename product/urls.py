from django.urls   import path

from product.views import ProductDetailView, RecommendedView, CategoryView

urlpatterns = [
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/category', CategoryView.as_view()), 
    path('/recommendation', RecommendedView.as_view())
]
