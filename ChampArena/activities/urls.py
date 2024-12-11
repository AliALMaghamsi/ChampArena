from django.urls import path
from . import views


app_name="activities"

urlpatterns=[
  path('new_activity/',views.new_activity_view,name='new_activity_view'),
  path('update_activity/<int:activity_id>/', views.update_activity_view, name='update_activity_view'),
  path('get-activities/<int:category_id>/', views.get_activities, name='get_activities'),
]
