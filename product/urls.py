from django.urls import path

from product.views import RecommendedView, CategoryView

urlpatterns = [
    path('/category', CategoryView.as_view()), 
    path('/recommendation', RecommendedView.as_view())
]
