from django.urls   import path

from product.views import NewListView, RecommendedView, CategoryView

urlpatterns = [
    path('/newlist', NewListView.as_view()),
    path('/category', CategoryView.as_view()), 
    path('/recommendation', RecommendedView.as_view())
]

