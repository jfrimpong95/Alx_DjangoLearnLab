from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Login
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Register
    path('register/', views.register, name='register'),

    # Profile (optional)
    path('profile/', views.profile, name='profile'),
]
from django.urls import path
from . import views

urlpatterns = [
    # Other auth URLs...
    path('profile/', views.profile, name='profile'),
]
