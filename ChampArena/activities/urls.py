from django.urls import path
from . import views


app_name="activities"

urlpatterns=[
  path('all/',views.all_activities_view,name='all_activities_view'),
  path('new_activity/',views.new_activity_view,name='new_activity_view'),
  path('update_activity/<int:activity_id>/', views.update_activity_view, name='update_activity_view'),
  path('get-activities/<int:category_id>/', views.get_activities, name='get_activities'),
  path("detail/<activity_id>/",views.detail_activity_view,name="detail_activity_view"),
  path('status/<activity_id>/',views.activity_status,name='activity_status'),
  path('category/new/',views.new_category_view,name='new_category_view'),
  
]
