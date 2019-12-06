from django.urls import path, include

from . import views

app_name = "user"
urlpatterns = [
    path('login/', views.login, name=app_name),  # 登录
    path('addMoney/', views.add_money, name=app_name),  # 增加金额
    path('searchInfo/', views.search_info, name=app_name),  # 查询个人的信息
    path('changePassword/', views.change_password, name=app_name),  # 修改密码
    path('bookCancelBorrow’/', views.book_cancel_borrow, name=app_name),  # 取消借阅
    path('searchOwnBook/', views.search_own_book, name=app_name),  # 查询自己的书籍
    path('bookBorrow/', views.book_borrow, name=app_name),  # 借阅书籍
    path('searchAll/', views.show_all, name=app_name),  # 查询个人的借书信息
]
