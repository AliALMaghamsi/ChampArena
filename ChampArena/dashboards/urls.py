from django.urls import path
from . import views


app_name="dashboards"

urlpatterns=[
    path('admin/',views.admin_dashboard_view,name='admin_dashboard_view'),
    path('user/',views.user_dashboard_view,name="user_dashboard_view"),
    path('notification/<int:notification_id>/delete/', views.delete_notification_view, name='delete_notification_view'),
    
    
]
