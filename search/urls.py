from django.urls import path, include

from . import views

app_name = "search"
urlpatterns = [
    path('searchAll/', views.show_all, name=app_name),
]
