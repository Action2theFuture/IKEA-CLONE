from django.urls import path, include

from user.views import LogIn
urlpatterns = [
    path('/signin', Signin.as_view())
]