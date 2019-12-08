from django.urls import path, include

from . import views

app_name = "search"
urlpatterns = [
    # path('searchAll/', views.show_all, name=app_name),
    path('home/', views.show_home_all, name=app_name),  # 显示所有的书籍
    path('searchBook/', views.search_book, name=app_name),  # 搜索书籍
    path('searchQuery/', views.every_book, name=app_name),  # 详情页具体的某一本书的所有信息
]
