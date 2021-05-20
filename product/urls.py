from django.urls import path

from product.views import RecommendedView

urlpatterns = [
    path('/recommended', RecommendedView.as_view())
]