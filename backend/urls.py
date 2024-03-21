"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from main_app import views


router = routers.DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'swaps', views.SwapViewSet)
router.register(r'profiles', views.ProfileViewSet)

from main_app.views import ItemViewSet, user_items, create_swap, about_me, get_swaps

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login-signup/', views.login_view, name='login'),
    path('signup/', views.SignupView.as_view(), name='authregister'),
    path('items/<int:item_id>/', views.item_view, name='item_view'),
    path('profile/<int:user_id>/items/', user_items, name='user_items'),
    path('items/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('items/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('create_swap/<int:item_id>/', create_swap, name='create_swap'),
    path('items/<int:item_id>/swaps/', get_swaps, name='create_swap'),
    path('about/', views.about_me, name='about_me'),
    path('', include(router.urls)),
]
