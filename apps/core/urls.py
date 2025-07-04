from django.urls import path
from django.contrib import admin
from . import views
app_name= 'core'

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.all_section_view, name='home'),

]