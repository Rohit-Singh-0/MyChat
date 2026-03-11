from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),

    path('', views.lobby, name='lobby'),
    path('room/', views.room, name='room'),

    path('get_token/', views.getToken),

    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
]
