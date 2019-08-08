from django.urls import path, include
from . import views

app_name = 'social'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('profile/',views.profile,name='profile'),
    path('editprofile/',views.editProfile,name='editProfile'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
]
