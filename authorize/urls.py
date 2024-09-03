from django.urls import path, include
from authorize.views import register_user, login_user, logout_user

urlpatterns = [
                     # it is the function name
    path("register/", register_user, name="register-user"),
    path("login/", login_user, name="login-user"),
    path("logout/", logout_user, name="logout-user"),
]