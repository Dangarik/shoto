from django.urls import path
from django.contrib import admin
from . import views
app_name= 'core'

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.training_list, name='home'),
    path('group/', lambda request: views.training_list(request, status='group'), name='home'),
    path('trainers/', lambda request: views.show_trainers_or_halls_or_sports(request, status='trainers'), name='trainers'),
    path('type/', lambda request: views.show_trainers_or_halls_or_sports(request, status='type'), name='type'),
    path('halls/', lambda request: views.show_trainers_or_halls_or_sports(request, status='halls'), name='halls'),
    path('training/<int:schedule_id>/', views.training_detail, name='training_detail'),
    path('training/<int:schedule_id>/record/', views.record_on_training, name='record_on_training'),
    path('training/<int:schedule_id>/delete/', views.delate_training, name='delete_training'),
    path('training/<int:schedule_id>/unrecord/', views.cancel_training_record, name='cancel_training_record'),
    path('training/create/', views.create_training, name='create_training'),
]