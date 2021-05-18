from django.urls import path

from product.views import RecommendList

urlpatterns = [
    path('/recommendlist', RecommendList.as_view())
]