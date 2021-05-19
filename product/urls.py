from django.urls import path

from product.views import RecommendList

urlpatterns = [
    path('/recommend', RecommendList.as_view())
]