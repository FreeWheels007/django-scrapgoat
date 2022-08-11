from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.set_user_info, name='profile_info'),
    path('logout/', views.logout, name='logout'),
    path('pickups/<select>/', views.view_pickups, name='view_pickups'),
]