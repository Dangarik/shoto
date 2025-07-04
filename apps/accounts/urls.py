from django.urls import path
from . import views


app_name= 'accounts'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('changedetails/', views.change_account_details, name='change_account_details'),

]