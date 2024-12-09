from . import views
from django.urls import path


app_name="main"

urlpatterns=[
   path("",views.home_page_view,name="home_page_view"),
   path("about/",views.about_page_view,name="about_page_view"),
   path("contact/",views.contact_page_view,name="contact_page_view"),

]
