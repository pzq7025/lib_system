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


def search_book(request):
    """
    进行模糊查询
    :param request:
    :return:
    """
    ob = request.body.decode('utf-8')
    accept = json.loads(ob)
    book_name = accept['bookName']
    result_book = Book.objects.filter(book_name__icontains=book_name).values_list(
        'book_name',
        'book_id',
        'book_author',
        'book_describe',
        'book_content',
        'book_status',
        'book_price',
        'book_type',
        'book_year',
        'book_url_pic',
    )
    if result_book:
        all_data = []
        for i in range(len(result_book)):
            one = {
                'title': result_book[i][0],
                'id': result_book[i][1],
                'author': result_book[i][2],
                'description': result_book[i][3],
                'content': result_book[i][4],
                'isBorrow': result_book[i][5],
                'money': result_book[i][6],
                'type': result_book[i][7],
                'year': result_book[i][8],
                'picUrl': result_book[i][9],
            }
            all_data.append(one)
        data = {
            'code': 0,
            'info': all_data,
        }
    else:
        data = {
            'code': 1
        }
    return JsonResponse(data)


def every_book(request):
    """
    查询每一本书籍
    :param request:
    :return:
    """
    ob = request.body.decode('utf-8')
    accept = json.loads(ob)
    get_book_id = accept['bookId']
    get_user_id = accept['userId']
    borrow_book = BorrowInfo.objects.filter(Q(borrow_browser_id=get_user_id) & Q(borrow_book_id=get_book_id)).values_list()
    result_book = Book.objects.filter(Q(book_id=get_book_id)).values_list(
        'book_name',
        'book_id',
        'book_author',
        'book_describe',
        'book_content',
        'book_status',
        'book_price',
        'book_type',
        'book_year',
        'book_url_pic',
    )
    try:
        if borrow_book:
            data = {
                'info': [
                    {
                        'title': result_book[0][0],
                        'id': result_book[0][1],
                        'author': result_book[0][2],
                        'description': result_book[0][3],
                        'content': result_book[0][4],
                        'isBorrow': False,
                        'money': result_book[0][6],
                        'type': result_book[0][7],
                        'year': result_book[0][8],
                        'picUrl': result_book[0][9],
                    }
                ],
                'code': 0,
            }
        else:
            data = {
                'info': [
                    {
                        'title': result_book[0][0],
                        'id': result_book[0][1],
                        'author': result_book[0][2],
                        'description': result_book[0][3],
                        'content': result_book[0][4],
                        'isBorrow': result_book[0][5],
                        'money': result_book[0][6],
                        'type': result_book[0][7],
                        'year': result_book[0][8],
                        'picUrl': result_book[0][9],
                    }
                ],
                'code': 0,
            }
    except Exception as e:
        print(e)
        data = {
            'code': 1,
        }
    return JsonResponse(data)


def show_home_all(request):
    """
    按照查询排行  分别将剩余量和借阅量前10的数据返回
    :param request:
    :return:
    """
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
            'borrow_book_name__book_url_pic',
            'book_remain',
        ).order_by('-hot_statistics')[:10]
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
            'borrow_book_name__book_url_pic',
            'book_remain',
        ).order_by('-totals_statistics')[:10]
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
                'picUrl': result_book[i][10],
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
                'picUrl': result_book_1[i][10],
            }
            # 好书  热评书籍
            all_data.append(one)
            # 总借阅的书籍  质量书籍
            all_data_1.append(one_1)
        data = {
            'code': 0,
            'listGood': all_data,
            'listBorrow': all_data_1,
        }
    else:
        data = {
            'code': 1
        }
    return JsonResponse(data)
