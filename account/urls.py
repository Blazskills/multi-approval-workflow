from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView,
# )
from . import views

urlpatterns = [
    path("test/", views.testaccount.as_view(), name="testme"),
    path("login/", views.LoginView.as_view(), name="login"),
    # path("profile/", views.ProfileView.as_view(), name="profile"),

]
