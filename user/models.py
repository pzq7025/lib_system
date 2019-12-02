from django.db import models

"""
系统管理员  对管理者操作  考虑是否加入其它
图书管理员  对书籍和浏览者  图书借阅信息表  图书借出状态表 管理者可以对书籍和借阅者进行操作
---------------------------------------------------------------------------------
书籍表  包括图书信息内容
浏览者  包括浏览信息者
书籍状态表  确定借书的状态
借阅者信息表  确定借阅者的借书状态
"""


# Create your models here.

class Browser(models.Model):
    """
    借阅者信息表
    """
    browser_id = models.CharField(max_length=20, primary_key=True, verbose_name="ID")  # 借书者的id
    browser_name = models.CharField(max_length=20, verbose_name="姓名")  # 借书者的姓名
    browser_password = models.CharField(max_length=20, verbose_name="密码")  # 借书者账号密码
    browser_status = models.BooleanField(default=True, verbose_name="借书状态")  # 借书状态
    browser_number = models.PositiveSmallIntegerField(default="0", verbose_name="已借量", blank=True)  # 借书的数量
    browser_number_max = models.PositiveSmallIntegerField(default="18", verbose_name="最大借书量", blank=True)  # 最大借书量
    overdraft = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="欠款金额", blank=True)  # 欠款金额
    browser_type = models.CharField(max_length=5, verbose_name='类型', choices=(('1', '本科生'), ('2', '研究生'), ('3', '其他')), default="1")  # 书籍类别

    objects = models.Manager()

    def __str__(self):
        return self.browser_name

    class Meta:
        db_table = 'BrowserInfo'
        verbose_name = "借阅者信息表"
        verbose_name_plural = verbose_name


class Book(models.Model):
    """
    图书表
    """
    book_id = models.CharField(max_length=20, primary_key=True, verbose_name="编号")  # 书的编号
    book_name = models.CharField(max_length=50, verbose_name="书名")  # 书名
    book_publish = models.CharField(max_length=50, verbose_name="出版社")  # 出版社
    book_author = models.CharField(max_length=20, verbose_name="作者")  # 作者
    book_year = models.DateField(verbose_name="出版时间")  # 出版时间
    book_number = models.PositiveSmallIntegerField(verbose_name="总量", default="5")  # 书的数量
    book_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="价格", blank=True)  # 价格
    book_status = models.BooleanField(default=True, verbose_name="是否可借")  # 书的状态
    book_describe = models.TextField(max_length=255, verbose_name='书籍描述', blank=True, default="")  # 书的描述内容  如年度最好的小说
    book_content = models.TextField(max_length=255, verbose_name='书籍内容', blank=True, default="")  # 书的内容
    book_type = models.CharField(max_length=2, verbose_name='书籍类型', choices=(('1', '杂志'), ('2', '书籍'), ('3', "其他")), default='2')  # 书籍类别
    book_url_pic = models.URLField(verbose_name="图片地址", blank=True)  # 图片地址

    objects = models.Manager()

    # browser = models.ManyToManyField(to=Browser, verbose_name='借书人', blank=True)

    def __str__(self):
        return self.book_name

    class Meta:
        db_table = 'BookInfo'
        verbose_name = "图书信息表"
        verbose_name_plural = verbose_name


class Manage(models.Model):
    """
    存在问题 需要在admin里面来写
    图书管理员表
    """
    manage_id = models.CharField(max_length=20, primary_key=True, db_index=True, verbose_name="图书管理员编号")  # 管理者编号
    manage_name = models.CharField(max_length=20, verbose_name="图书管理员姓名")  # 管理者姓名

    objects = models.Manager()

    def __str__(self):
        return self.manage_name

    class Meta:
        db_table = 'MangerInfo'
        verbose_name = "管理员信息表"
        verbose_name_plural = verbose_name


class BorrowBookInfo(models.Model):
    """
    书籍管理表  图书馆书籍的状态信息
    """
    book_id = models.CharField(max_length=20, primary_key=True, verbose_name="书的编号")  # 书的编号
    book_name = models.CharField(max_length=20, verbose_name="书名")  # 书名
    book_total = models.PositiveSmallIntegerField(verbose_name="书籍总数", blank=True, default="5")  # 总的书籍数
    browser_total = models.PositiveSmallIntegerField(verbose_name="借阅数", blank=True, default="0")  # 借阅总数
    back_time = models.DateField(auto_now_add=True, verbose_name="到馆时间")  # 到馆时间
    book_remain = models.PositiveSmallIntegerField(verbose_name="在馆数", blank=True, default="5")  # 剩余的数量

    objects = models.Manager()

    # book = models.ForeignKey(to=Book, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="书籍")

    # browser = models.ForeignKey(to=Browser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="借阅者")

    def __str__(self):
        return f"{self.book_id}-{self.book_name}"

    class Meta:
        db_table = 'BorrowBookInfo'
        verbose_name = "借阅书籍状态表"
        verbose_name_plural = verbose_name


class BorrowInfo(models.Model):
    """
    借书者信息管理  借书人的借书信息
    """
    borrow_info = models.DateTimeField(auto_created=True, primary_key=True, verbose_name="借阅记录创建时间")
    browser_id = models.CharField(max_length=20, verbose_name="借书者编号")  # 借书者的id
    browser_name = models.CharField(max_length=20, verbose_name="借书人姓名")  # 借书者的姓名
    book_id = models.CharField(max_length=20, verbose_name="书籍编号")  # 书的编号
    book_name = models.CharField(max_length=50, verbose_name="书名")  # 书名
    browser_time = models.DateField(auto_now=True, verbose_name="借书时间")  # 借出时间
    back_time = models.DateField(auto_now=True, verbose_name="还书时间")  # 还书时间

    objects = models.Manager()

    # book = models.ForeignKey(to=Book, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="书籍")
    # browser = models.ForeignKey(to=Browser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="借阅者")

    def __str__(self):
        return f"{self.browser_id}-{self.browser_name}"

    class Meta:
        db_table = 'BorrowInfo'
        verbose_name = "借阅信息记录表"
        verbose_name_plural = verbose_name