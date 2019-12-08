import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Book, Browser, BorrowBookInfo, BorrowInfo
from django.db.models import Q
from django.db.models import F
import datetime

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
    ob = request.body.decode('utf-8')
    accept = json.loads(ob)
    user_id = accept['username']
    user_password = accept['password']
    # 登录验证  成功返回True
    result_user = Browser.objects.filter(Q(browser_id=user_id) & Q(browser_password=user_password)).values_list('browser_id', 'browser_name', 'browser_type')
    if result_user:
        data = {
            'code': 0,
            'data': [{
                'userId': result_user[0][0],
                'userName': result_user[0][1],
                'userType': result_user[0][2],
            }],
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
    ob = request.body.decode('utf-8')
    accept = json.loads(ob)
    user_id = accept['userId']
    money = accept['money']
    # 充钱 将增加余额数量
    result = Browser.objects.filter(Q(browser_id=user_id))
    if result:
        Browser.objects.filter(Q(browser_id=user_id)).update(overdraft=F('overdraft') + money)
        detail_result = Browser.objects.filter(Q(browser_id=user_id)).values('overdraft')
        # 当把钱还清了就可以继续借书了
        if detail_result >= 0:
            Browser.objects.filter(Q(browser_id=user_id)).update(browser_status=True)
        data = {
            'code': 0,
            'info': detail_result[0]['overdraft'],
        }
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
    ob = request.body.decode('utf-8')
    accept = json.loads(ob)
    user_id = accept['userId']
    # 个人信息
    result_person = Browser.objects.filter(Q(browser_id=user_id)).values_list(
        'browser_id',
        'browser_name',
        'overdraft',
        'browser_type',
    )
    # 获取用户的信息 输出需求
    if result_person:
        data = {
            'code': 0,
            'data': [{
                'userId': result_person[0][0],
                'userName': result_person[0][1],
                'leftMoney': result_person[0][2],
                'userType': result_person[0][3],
            }],
        }
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
    ob = request.body.decode('utf-8')
    accept = json.loads(ob)
    user_id = accept['userId']
    user_old_password = accept['oldPassword']
    user_new_password = accept['newPassword']
    # 获取前端传来的数据直接对数据进行修改
    operator = Browser.objects.filter(Q(browser_id=user_id) & Q(browser_password=user_old_password)).update(browser_password=user_new_password)
    if operator:
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
    ob = request.body.decode('utf-8')
    accept = json.loads(ob)
    user_id = accept['userId']
    book_id = accept['bookId']
    # 如果操作成功  说明数据库中含有此信息  注意同个人不能同时借多本书
    # operator = BorrowInfo.objects.filter(Q(borrow_browser_id=user_id) & Q(borrow_book_id=book_id)).order_by('-borrow_info').last().delete()
    # 因为不借阅就删除  所以不会出现冗余数据duplicate
    operator = BorrowInfo.objects.filter(Q(borrow_browser_id=user_id) & Q(borrow_book_id=book_id)).delete()
    if operator:
        # 对于存在数据  取消订阅  剩余数量+1 借阅量-1
        BorrowBookInfo.objects.filter(Q(borrow_book_id=book_id)).update(book_remain=F('book_remain') + 1)
        BorrowBookInfo.objects.filter(Q(borrow_book_id=book_id)).update(browser_total=F('browser_total') - 1)
        data = {
            'code': 0
        }
    else:
        data = {
            'code': 1
        }
    return JsonResponse(data)


def book_borrow(request):
    """
    userId
    bookId
    借阅书籍  每次借阅完成最后的图书系统也要插入数据插入借出去的书籍
    :param request:
    :return:
    """
    ob = request.body.decode('utf-8')
    accept = json.loads(ob)
    user_id = accept['userId']
    book_id = accept['bookId']
    result_user = Browser.objects.filter(Q(browser_id=user_id) & Q(browser_status=True) & (F('overdraft')) >= 0).values_list('browser_name')
    result_book = Book.objects.filter(Q(book_id=book_id) & Q(book_status=True)).values_list('book_name')
    borrow_book = BorrowInfo.objects.filter(Q(book_id=book_id) & Q(borrow_browser_id=user_id))
    if result_book and result_user and not borrow_book:
        # 判断借书人的记录直接创建 不存在一个人借两本书  多以borrow_book永远为真
        BorrowInfo.objects.create(
            browser_time=datetime.date.today(),
            back_time=datetime.date.today() + datetime.timedelta(days=3),
            borrow_browser_id=user_id,
            borrow_browser_name=result_user[0][0],
            borrow_book_id=book_id,
            borrow_book_name=result_book[0][0],
        )
        # 判断借书信息的记录是否存在 存在修改  不存在添加
        # 向BorrowBookInfo添加信息
        # 判断此书是不是第一次借阅
        judge_0 = BorrowBookInfo.objects.filter(Q(borrow_book_id=book_id)).update(book_remain=F('book_remain') - 1)
        judge_1 = BorrowBookInfo.objects.filter(Q(borrow_book_id=book_id)).update(browser_total=F('browser_total') + 1)
        # 借阅者的借阅量+1
        Browser.objects.filter(Q(browser_id=user_id)).update(browser_number=F('browser_number') + 1)
        if not judge_0 and not judge_1:
            # 两个为真说明有数据则不添加新的数据  如果为假就添加新的数据
            BorrowBookInfo.objects.create(
                borrow_book_id=book_id,
                borrow_book_name=result_book[0],
                book_remain=4,
                browser_total=1,
            )
        # 判断书是不是被借完了  如果书借完了  就是不可借的状态
        judge_remain = BorrowBookInfo.objects.filter(Q(borrow_book_id=book_id)).values_list('book_remain')
        if judge_remain[0][0] == 0:
            Book.objects.filter(Q(book_id=book_id)).update(book_status=False)
        # 判断借书量是不是上限了  上限了 就修改状态为False
        judge_browser = Browser.objects.filter(Q(browser_id=user_id)).values_list('browser_number')
        if judge_browser[0][0] == 18:
            Browser.objects.filter(Q(browser_id=user_id)).update(browser_status=False)
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
    ob = request.body.decode('utf-8')
    accept = json.loads(ob)
    user_id = accept['userId']
    page_size = accept['pageSize']  # 每个页面的数据
    skip_page = accept['skipPage']  # 翻页
    result_remain = BorrowInfo.objects.filter(Q(borrow_browser_id=user_id))
    if result_remain:
        # 图书信息
        # 由于图书表和借阅信息表分开，所以需要先获取id在获取书籍的剩余量
        remain_number_ids = BorrowInfo.objects.filter(Q(borrow_browser_id=user_id)).values_list('borrow_book_id')
        remain_result = []
        for i in remain_number_ids:
            remain_number = BorrowBookInfo.objects.filter(Q(borrow_book_id=i[0])).values_list('book_remain')
            remain_result.append(remain_number[0][0])
        # 获取用户的书籍信息  正向查询
        result_book = BorrowInfo.objects.filter(Q(borrow_browser_id=user_id)).values_list(
            'borrow_book_name__book_name',
            'borrow_book_name__book_id',
            'borrow_book_name__book_price',
            'borrow_book_name__book_type',
            'borrow_book_name__book_author',
            'borrow_book_name__book_describe',
            'borrow_book_name__book_content',
            'borrow_book_name__book_year',
            'borrow_book_name__book_status',
        )
        # 将所有的数据生成对象数组 返回给前端
        all_data = []
        area_judge = int(skip_page) * int(page_size)
        if len(result_book) > area_judge:
            for i in range(area_judge, area_judge + int(page_size)):
                one = {
                    'title': result_book[i][0],
                    'id': result_book[i][1],
                    'price': result_book[i][2],
                    'number': remain_result[i],
                    'type': result_book[i][3],
                    'author': result_book[i][4],
                    'description': result_book[i][5],
                    'content': result_book[i][6],
                    'time': result_book[i][7],
                    'isBorrow': result_book[i][8],
                }
                all_data.append(one)
        else:
            for i in range(area_judge, len(all_data)):
                one = {
                    'title': result_book[i][0],
                    'id': result_book[i][1],
                    'price': result_book[i][2],
                    'number': remain_result[i],
                    'type': result_book[i][3],
                    'author': result_book[i][4],
                    'description': result_book[i][5],
                    'content': result_book[i][6],
                    'time': result_book[i][7],
                    'isBorrow': result_book[i][8],
                }
                all_data.append(one)

        data = {
            'code': 0,
            'rows': all_data,
            'total': len(all_data),
        }
    else:
        data = {
            'code': 1
        }
    return JsonResponse(data)


def show_all(request):
    # 查询个人的借书信息  输出超时书籍和处理办法
    # if request.GET['userId']:
    ob = request.body.decode('utf-8')
    accept = json.loads(ob)
    user_id = accept['userId']
    # 超额时间应该以还书时间为准
    result = BorrowInfo.objects.filter(Q(borrow_browser_id=user_id)).values_list('back_time')
    if result:
        # 查询超出时间的书籍
        remain_number_ids = BorrowInfo.objects.filter(Q(borrow_browser_id=user_id)).values_list('borrow_book_id')
        remain_result = []
        for i in remain_number_ids:
            remain_number = BorrowBookInfo.objects.filter(Q(borrow_book_id=i[0])).values_list('book_remain')
            remain_result.append(remain_number[0][0])
        sub_time = (datetime.date.today() - result[0][0]).days
        # 将超出的书籍进行返回
        result_book = BorrowInfo.objects.filter(longtime__lt=sub_time).values_list(
            'borrow_book_name__book_name',
            'borrow_book_name__book_id',
            'borrow_book_name__book_price',
            'borrow_book_name__book_type',
            'borrow_book_name__book_author',
            'borrow_book_name__book_describe',
            'borrow_book_name__book_content',
            'borrow_book_name__book_year',
            'borrow_book_name__book_status',
        )

        # 欠费处理  一天一毛钱
        Browser.objects.filter(Q(browser_id=user_id)).update(overdraft=F('overdraft') - sub_time * 0.1)
        detail_result = Browser.objects.filter(Q(browser_id=user_id)).values('overdraft')
        if detail_result[0]['overdraft'] < 0:
            Browser.objects.filter(Q(browser_id=user_id)).update(browser_status=False)
        # 输出数据
        all_data = []
        for i in range(len(result_book)):
            one = {
                'title': result_book[i][0],
                'id': result_book[i][1],
                'price': result_book[i][2],
                'number': remain_result[i],
                'type': result_book[i][3],
                'author': result_book[i][4],
                'description': result_book[i][5],
                'content': result_book[i][6],
                'time': result_book[i][7],
                'isBorrow': result_book[i][8],
                'leftMoney': detail_result[0]['overdraft'],
            }
            all_data.append(one)

        data = {
            'code': 0,
            'data': all_data,
        }
    else:
        data = {
            'code': 1
        }
    return JsonResponse(data)


def continue_book(request):
    """
    续借此书
    :param request:
    :return:
    """
    ob = request.body.decode('utf-8')
    accept = json.loads(ob)
    user_id = accept['userId']
    book_id = accept['bookId']
    # 检测书籍是否可以续借
    result = BorrowInfo.objects.filter(Q(borrow_browser_id=user_id) & Q(borrow_book_id=book_id)).values_list('browser_time')
    # 借阅的时间
    sub_time = (datetime.date.today() - result[0][0]).days
    if sub_time < 30:
        BorrowInfo.objects.filter(Q(borrow_browser_id=user_id) & Q(borrow_book_id=book_id)).update(longtime=F('longtime') + 30)
        BorrowInfo.objects.filter(Q(borrow_browser_id=user_id) & Q(borrow_book_id=book_id)).update(back_time=F('back_time') + 30)
        data = {
            'code': 0,
        }
    else:
        Browser.objects.filter(Q(browser_id=user_id)).update(overdraft=F('overdraft') - sub_time * 0.1)
        detail_result = Browser.objects.filter(Q(browser_id=user_id)).values('overdraft')
        if detail_result[0]['overdraft'] < 0:
            Browser.objects.filter(Q(browser_id=user_id)).update(browser_status=False)
        data = {
            'code': 1
        }
    return JsonResponse(data)
