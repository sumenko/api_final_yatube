from django.contrib import admin
from django.urls import include, path, re_path


from django.views.generic import TemplateView, RedirectView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/v1/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
