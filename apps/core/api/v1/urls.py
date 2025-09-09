from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from apps.core.api.v1.views import ComplaintAV, DropdownAV, LoginAV, RegisterAV

# Write your urls here

urlpatterns = [
    path(
        "login/",
        LoginAV.as_view(),
    ),
    path(
        "register/",
        RegisterAV.as_view(),
    ),
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
    ),
    path(
        "complaint/",
        ComplaintAV.as_view(),
    ),
    path(
        "dropdown/",
        DropdownAV.as_view(),
    ),
]
