from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Book, Browser, Manage, BorrowBookInfo, BorrowInfo
from django.db.models import Q
from django.db.models import F
from django.core import serializers

"""
0: successful
1: fail
"""


# Create your views here.
def login(request):
    """
    userName
    password
    登录处理
    :param request:
    :return:
    """
    user_id = request.GET['userId']
    user_password = request.GET['passWord']
    result_user = Browser.objects.filter(Q(browser_id=user_id) & Q(browser_password=user_password))
    if result_user:
        data = {
            'code': 0
        }
    else:
        data = {
            'code': 1
        }
    return JsonResponse(data)


def add_money(request):
    """
    加钱处理
    userId
    money
    :param request:
    :return:
    """
    user_id = request.GET['userId']
    money = request.GET['money']
    result = Browser.objects.filter(Q(browser_id=user_id))
    print(result.values_list())
    if result:
        Browser.objects.filter(Q(browser_id=user_id)).update(overdraft=F('overdraft') + money)
        browser_info = Browser.objects.filter(Q(browser_id=user_id))
        print(browser_info)
        pin = serializers.serialize("json", browser_info)
        return JsonResponse(pin, safe=False)
    else:
        data = {
            'code': 1
        }
        return JsonResponse(data)


def search_info(request):
    """
    个人信息查询
    :param request:
    :return:
    """
    user_id = request.GET['userId']
    user_password = request.GET['passWord']
    result = Browser.objects.filter(Q(browser_id=user_id) & Q(browser_password=user_password))
    if result:
        pin = serializers.serialize("json", result)
        return JsonResponse(pin, safe=False)
    else:
        data = {
            'code': 1
        }
    return JsonResponse(data)


def change_password(request):
    """
    修改密码
    :param request:
    :return:
    """
    user_id = request.GET['userId']
    user_password = request.GET['passWord']
    result_user = Browser.objects.filter(Q(browser_id=user_id)).update(browser_password=user_password)
    if result_user:
        data = {
            'code': 0
        }
    else:
        data = {
            'code': 1
        }
    return JsonResponse(data)


def book_cancel_borrow(request):
    """
    取消订阅
    :param request:
    :return:
    """
    user_id = request.GET['userId']
    book_id = request.GET['bookId']
    operator = BorrowInfo.objects.filter(Q(borrow_info=user_id) & Q(book_id=book_id)).delete()
    if operator:
        data = {
            'code': 0
        }
    else:
        data = {
            'code': 1
        }
    return JsonResponse(data)


def book_borrow(request):
    # 未完成
    """
    userId
    bookId
    借阅书籍
    :param request:
    :return:
    """
    user_id = request.GET['userId']
    book_id = request.GET['bookId']
    result_user = Browser.objects.filter(Q(browser_id=user_id) & F('overdraft') >= 0)
    result_book = Book.objects.filter(Q(book_id=book_id) & Q(book_status=True))
    if result_book and result_user:
        BorrowInfo.objects.create()
        data = {
            'code': 0
        }
    else:
        data = {
            'code': 1
        }
    return JsonResponse(data)


def search_own_book(request):
    """
    查询自己借阅的书籍
    :param request:
    :return:
    """
    user_id = request.GET['userId']
    result = BorrowInfo.objects.filter(Q(browser_id=user_id))
    if result:
        pin = serializers.serialize("json", result)
        return JsonResponse(pin, safe=False)
    else:
        data = {
            'code': 1
        }
        return JsonResponse(data)
