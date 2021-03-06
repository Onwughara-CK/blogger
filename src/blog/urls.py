"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from users import views as users_view
from api import views as api_views

from rest_framework import routers
from rest_framework.authtoken import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register('v1/posts', api_views.PostViewSet)
router.register('v1/users', api_views.UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('page.urls')),
    path('register/', users_view.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='page/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='page/logout.html'), name='logout'),
    path('profile/<str:username>', users_view.profile, name='profile'),
    path('api/', include(router.urls)),
    path('api/v1/token/', TokenObtainPairView.as_view()),
    path('api/v1/token/refresh/', TokenRefreshView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
