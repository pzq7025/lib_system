from django.contrib import admin
# from django.contrib.auth.models import Group, User
# from django.contrib.auth.admin import UserAdmin
from .models import Browser, Book, BorrowInfo, BorrowBookInfo

"""
superuser:
图书管理者
    user:pzq
    password: pengzuquan

系统管理者
    user:system
    password: yeqinglan

"""

# Register your models here.
# class ManageSurper(admin.ModelAdmin):
#     date_hierarchy = 'pub_date'


admin.site.site_header = '图书管理系统'
admin.site.site_title = '登录系统后台'
admin.site.index_title = '后台管理'


#
# # user = User.objects.get(is_superuser=True)
#
# admin.site.unregister(Group)
# admin.site.unregister(User)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # 这个的作用是给出一个筛选机制，一般按照时间比较好
    date_hierarchy = 'book_year'

    # 不显示的字段  修改界面的不显示添加界面不显示
    exclude = ('book_url_pic',)

    # 在查看修改的时候显示的属性，第一个字段带有<a>标签，所以最好放标题  在外浏览界面的不显示
    list_display = ('book_id', 'book_name', 'book_author', 'book_status', 'book_number', 'book_url_pic')

    # 设置需要添加<a>标签的字段
    list_display_links = ('book_id',)

    # 激活过滤器，这个很有用，按照什么分类
    list_filter = ('book_status', 'book_type')

    list_per_page = 20  # 控制每页显示的对象数量，默认是100

    # filter_horizontal = ('book_type',)  # 给多选增加一个左右添加的框 必须是多对多后面尝试一下能不能和book 和browser连接在一起

    # 限制用户权限，只能看到自己编辑的文章
    # def get_queryset(self, request):
    #     qs = super(BookAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(author=request.user)


@admin.register(Browser)
class BrowserAdmin(admin.ModelAdmin):
    # 这个的作用是给出一个筛选机制，一般按照时间比较好
    # date_hierarchy = 'browser_id'

    # 不显示的字段
    # exclude = ('browser_password',)

    # 在查看修改的时候显示的属性，第一个字段带有<a>标签，所以最好放标题
    list_display = ('browser_id', 'browser_name', 'browser_status', 'browser_number', 'overdraft', 'browser_type')

    # 设置需要添加<a>标签的字段
    # list_display_links = ('title',)

    # 激活过滤器，这个很有用
    list_filter = ('browser_type', 'browser_status')

    list_per_page = 20  # 控制每页显示的对象数量，默认是100

    # filter_horizontal = ('browser_type',)  # 给多选增加一个左右添加的框

    # 限制用户权限，只能看到自己编辑的文章
    # def get_queryset(self, request):
    #     qs = super(BrowserAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(author=request.user)


# @admin.register(Manage)
# class ManageAdmin(admin.ModelAdmin):
#     # 这个的作用是给出一个筛选机制，一般按照时间比较好
#     # date_hierarchy = 'manage_id'
#
#     # 不显示的字段
#     # exclude = ('borrow_info',)
#
#     # 在查看修改的时候显示的属性，第一个字段带有<a>标签，所以最好放标题
#     list_display = ('manage_id', 'manage_name')
#
#     # 设置需要添加<a>标签的字段
#     # list_display_links = ('title',)
#
#     # 激活过滤器，这个很有用
#     list_filter = ('manage_id',)
#
#     list_per_page = 10  # 控制每页显示的对象数量，默认是100
#
#     # filter_horizontal = ('tags', 'keywords')  # 给多选增加一个左右添加的框
#
#     # 限制用户权限，只能看到自己编辑的文章
#     # def get_queryset(self, request):
#     #     qs = super(ManageAdmin, self).get_queryset(request)
#     #     if request.user.is_superuser:
#     #         return qs
#     #     return qs.filter(author=request.user)


@admin.register(BorrowInfo)
class BorrowInfoAdmin(admin.ModelAdmin):
    # 这个的作用是给出一个筛选机制，一般按照时间比较好
    date_hierarchy = 'browser_time'

    # 不显示的字段
    # exclude = ('borrow_info',)

    # 在查看修改的时候显示的属性，第一个字段带有<a>标签，所以最好放标题
    list_display = ('borrow_browser_name', 'borrow_book_name', 'browser_time', 'longtime', 'back_time',)

    # 设置需要添加<a>标签的字段
    # list_display_links = ('title',)

    # 激活过滤器，这个很有用
    list_filter = ('browser_time', 'back_time')

    list_per_page = 20  # 控制每页显示的对象数量，默认是100

    # filter_horizontal = ('borrow_browser_id', 'borrow_browser_name', 'borrow_book_id', 'borrow_book_name')  # 给多选增加一个左右添加的框

    # 限制用户权限，只能看到自己编辑的文章
    # def get_queryset(self, request):
    #     qs = super(BorrowInfoAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(author=request.user)


@admin.register(BorrowBookInfo)
class BorrowBookInfoAdmin(admin.ModelAdmin):
    # 这个的作用是给出一个筛选机制，一般按照时间比较好
    date_hierarchy = 'back_time'

    # 不显示的字段
    # exclude = ('borrow_info',)

    # 在查看修改的时候显示的属性，第一个字段带有<a>标签，所以最好放标题
    list_display = ('borrow_book_id', 'borrow_book_name', 'browser_total', 'borrow_book_number', 'book_remain', 'totals_statistics', 'hot_statistics', 'back_time')

    # 设置需要添加<a>标签的字段
    # list_display_links = ('title',)

    # 激活过滤器，这个很有用
    list_filter = ('back_time', 'browser_total',)

    list_per_page = 20  # 控制每页显示的对象数量，默认是100

    # filter_horizontal = ('borrow_book_id', 'borrow_book_name')  # 给多选增加一个左右添加的框

    # 限制用户权限，只能看到自己编辑的文章
    # def get_queryset(self, request):
    #     qs = super(BorrowBookInfoAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(author=request.user)
