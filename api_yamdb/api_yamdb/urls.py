from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView

)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/token/', 
        TokenObtainPairView.as_view(), 
        name='token_obtain_pair'),
    path('api/token/refresh/', 
        TokenRefreshView.as_view(), 
        name='token_refresh'),
    path('api/token/verify/', 
        TokenVerifyView.as_view(), 
        name='token_verify'),
]
