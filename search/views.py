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
    # # else:
    # #     return_result = {
    # #         'result': None
    # #     }
    #
    # return JsonResponse(return_result)
