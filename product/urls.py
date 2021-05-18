from django.urls   import path

from product.views import NewListView

urlpatterns = [
    path('/newlist', NewListView.as_view())
]