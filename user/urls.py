from django.urls import path

from user.views import LogIn

urlpatterns = [
    path('/login', LogIn.as_view()),
]