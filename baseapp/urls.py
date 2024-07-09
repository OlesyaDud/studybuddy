from django.urls import path
from . import views



urlpatterns = [
    # takes 3 params
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('', views.home, name='home'),

    path('room/<str:id>/', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:id>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:id>/', views.deleteRoom, name='delete-room'),

]
