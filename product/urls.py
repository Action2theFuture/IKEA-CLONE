from django.urls   import path

from product.views import MainView

urlpatterns = [
   path('/main', MainView.as_view()), 
]
