import json

from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from user.models import Book
from user.models import BorrowBookInfo
from user.models import BorrowInfo
from django.db.models import Q
from django.db.models import F


# Create your views here.


# def search_book(request):
#     book_name = request.GET['bookname']
#     data = {}
#     serialize_data = serializers.serialize('json', Book.objects.all())  # 序列化
#     if book_name == 'java' or book_name == 'python':
#         data = {
#             'result_name': 'java or python',
#             'status': 200,
#         }
#     else:
#         data = {
#             'status': 404,
#         }
#     return JsonResponse(data)


def show_all(request):
    # if request.GET['userId']:
    print(request.body)
    accept = json.loads(request)
    user_id = accept['userId']
    print(user_id)
    # 外键__要查询的字段
    # 查询成功 用Q查询加快查询速度  F查询加快逻辑处理速度
    result = BorrowInfo.objects.filter(Q(borrow_browser_id=user_id)).values_list('borrow_book_name__book_id')
    # result = BorrowInfo.objects.all(borrow_browser_id_id=user_id).borrow_book_id.all()
    print(result)
    if user_id:
        # pin = serializers.serialize("json", result)
        data = {str(user_id): 2}
        return JsonResponse(data)
    else:
        data = {
            'code': 1
        }
        return JsonResponse(data)
    # x = request.GET
    # print(x)
    # return JsonResponse({1: 2})


# book_queryset = Book.objects.all().order_by('book_number')
# book_browser_queryset = BorrowBookInfo.objects.all().order_by('-browser_total')
# result_book = []
# result_book_browser = []
# for i in book_queryset[:10]:
#     result_book.append({
#         'id': i.book_id,
#         'title': i.book_name,
#         'description': i.book_publish,
#         'content': i.book_author
#     })
#
# for i in book_browser_queryset[:10]:
#     result_book_browser.append({
#         'id': i.book_id,
#         'title': i.book_name,
#         'description': i.browser_total,
#         'content': i.book_remain,
#     })
# return_result = {
#     'code': 0,
#     'listGood': result_book,
#     'listBorrow': result_book_browser,
# }


# else:
#     return_result = {
#         'result': None
#     }
#
# return JsonResponse(return_result)
def show_home_all(request):
    user_id = request.GET['query']
    if user_id:
        result_total = BorrowBookInfo.objects.all().order_by('-browser_total')
        result_remain = BorrowInfo.objects.all().order_by('-book_remain')
        pin = serializers.serialize("json", result_remain)
        return JsonResponse(pin, safe=False)
    else:
        data = {
            'code': 1
        }
        return JsonResponse(data)
