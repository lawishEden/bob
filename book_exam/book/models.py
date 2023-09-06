from django.db import models
from django.contrib.auth.models import AbstractUser
from book.Storage import ImageStorage
# Create your models here.

class BookUser(AbstractUser):
    phone = models.CharField(verbose_name='手机号', max_length=11)
    choice_gender = (
        (0, '女'),
        (1, '男'),
        (2, '未知')
    )
    gender = models.IntegerField(verbose_name='性别', choices=choice_gender, default=2)
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)

class Book(models.Model):
    name = models.CharField(verbose_name='书名', max_length=50, blank=False, default='')
    rating = models.CharField(verbose_name='评分', max_length=5, default='0')
    price = models.FloatField(verbose_name='价格', blank=False, default=0)
    cover = models.ImageField(verbose_name='封面', upload_to='upload/%Y/%m/%d',
                              default='img/default.png', storage=ImageStorage())
    introduction = models.CharField(verbose_name='介绍', max_length=200, blank=True, default='')
    publish = models.CharField(verbose_name='出版社', max_length=50, default='', blank=True)
    url = models.URLField(verbose_name='URL', blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '图书管理'
        verbose_name_plural = '图书管理'


class hits(models.Model):
    userid=models.IntegerField(verbose_name='用户ID',default=0)
    bookid=models.IntegerField(verbose_name='图书ID',default=0)
    hitnum=models.IntegerField(verbose_name='点击次数',default=0)

    def __str__(self):
        return str(self.userid)

    class Meta:
        verbose_name='点击量'
        verbose_name_plural='点击量'
