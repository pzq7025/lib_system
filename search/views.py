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
#
#
# def show_all(request):
#     # if request.GET['userId']:
#     ob = request.body.decode('utf-8')
#     accept = json.loads(ob)
#     user_id = accept['userId']
#     print(user_id)
#     # 外键__要查询的字段
#     # 查询成功 用Q查询加快查询速度  F查询加快逻辑处理速度
#     result = BorrowInfo.objects.filter(Q(borrow_browser_id=user_id)).values_list('borrow_book_name__book_id', 'borrow_book_name__book_name')
#     # result = BorrowInfo.objects.all(borrow_browser_id_id=user_id).borrow_book_id.all()
#     print(result)
#     if user_id:
#         # pin = serializers.serialize("json", result)
#         data = {str(user_id): 2}
#         return JsonResponse(data)
#     else:
#         data = {
#             'code': 1
#         }
#         return JsonResponse(data)
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
    ob = request.body.decode('utf-8')
    accept = json.loads(ob)
    user_id = accept['userId']
    if user_id:
        result_book = BorrowBookInfo.objects.all().values_list(
            'borrow_book_name__book_name',
            'borrow_book_name__book_id',
            'borrow_book_name__book_price',
            'borrow_book_name__book_type',
            'borrow_book_name__book_author',
            'borrow_book_name__book_describe',
            'borrow_book_name__book_content',
            'borrow_book_name__book_year',
            'borrow_book_name__book_status',
            'book_remain',
        ).order_by('-book_remain')[:10]
        result_book_1 = BorrowBookInfo.objects.all().values_list(
            'borrow_book_name__book_name',
            'borrow_book_name__book_id',
            'borrow_book_name__book_price',
            'borrow_book_name__book_type',
            'borrow_book_name__book_author',
            'borrow_book_name__book_describe',
            'borrow_book_name__book_content',
            'borrow_book_name__book_year',
            'borrow_book_name__book_status',
            'book_remain',
        ).order_by('-browser_total')[:10]
        # 剩余量
        all_data = []
        # 借阅量
        all_data_1 = []
        for i in range(len(result_book)):
            one = {
                'title': result_book[i][0],
                'id': result_book[i][1],
                'price': result_book[i][2],
                'type': result_book[i][3],
                'author': result_book[i][4],
                'description': result_book[i][5],
                'content': result_book[i][6],
                'time': result_book[i][7],
                'isBorrow': result_book[i][8],
                'number': result_book[i][9],
            }
            one_1 = {
                'title': result_book_1[i][0],
                'id': result_book_1[i][1],
                'price': result_book_1[i][2],
                'type': result_book_1[i][3],
                'author': result_book_1[i][4],
                'description': result_book_1[i][5],
                'content': result_book_1[i][6],
                'time': result_book_1[i][7],
                'isBorrow': result_book_1[i][8],
                'number': result_book_1[i][9],
            }
            # 剩余量
            all_data.append(one)
            # 借阅量
            all_data_1.append(one_1)
        data = {
            'code': 0,
            'data': all_data,
            'data1': all_data_1,
        }
    else:
        data = {
            'code': 1
        }
    return JsonResponse(data)
