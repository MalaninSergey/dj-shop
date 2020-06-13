from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from loginsys import views

app_name = 'loginsys'

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('auth/', views.auth),
    path('logout/', views.profilelogout),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
]

