from django.urls import path
from . import views


app_name="activities"

urlpatterns=[
  path('all/',views.all_activities_view,name='all_activities_view'),
  path('new_activity/',views.new_activity_view,name='new_activity_view'),
  path('update_activity/<int:activity_id>/', views.update_activity_view, name='update_activity_view'),
  path('get-activities/<int:category_id>/', views.get_activities, name='get_activities'),
  path("detail/<activity_id>/",views.detail_activity_view,name="detail_activity_view"),
  path('book/<int:activity_id>/', views.book_activity, name='book_activity'),
  path('category/new/',views.new_category_view,name='new_category_view'),
  path('category/update/<int:category_id>/',views.update_category_view,name='update_category_view'),
  path('category/delete/<int:category_id>/',views.delete_category_view,name='delete_category_view'),
  path('activity_name/new/',views.new_activity_name_view,name='new_activity_name_view'),
  path('activity_name/update/<int:activity_id>/',views.update_activity_name_view,name='update_activity_name_view'),
  path('activity_name/delete/<int:activity_id>/',views.delete_activity_name_view,name='delete_activity_name_view'),
  path('status/<activity_id>/',views.activity_status,name='activity_status'),
  
]
