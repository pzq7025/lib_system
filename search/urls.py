from django.urls import path, include

from . import views

app_name = "search"
urlpatterns = [
    # path('searchAll/', views.show_all, name=app_name),
    path('home/', views.show_home_all, name=app_name),  # 显示所有的书籍
]
