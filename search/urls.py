from django.urls import path, include

from . import views

app_name = "search"
urlpatterns = [
    path('searchAll/1.html', views.show_all, name=app_name),
    path('home/', views.show_home_all, name=app_name),
]
