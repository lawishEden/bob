from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib.auth import authenticate, login, logout
from book.reg_login_form.register_form import Reg_Form
from book.reg_login_form.login import Login_Form
from book.models import BookUser, Book, hits


# Create your views here.

def index(request):
    book_list=Book.objects.alias()[:24]
    return render(request, "home/index.html",locals())

def detail(request,id):
    bk = Book.objects.get(id=id)
    currentuser =request.user.id
    if currentuser:
        try:
            hit=hits.objects.get(userid=currentuser,bookid=id)
            hit.hitnum +=1
            hit.save()
            print(hit)
        except hits.DoesNotExist:
            hit2=hits()
            hit2.userid=currentuser
            hit2.bookid=id
            hit2.hitnum +=1
            hit2.save()
            print(hit2)
        data =str(currentuser) + '\t' + str(id) + '\t' + str(1)
        from hdfs import Client
        from utils import tools
        hdfs_path='/book/hits.txt'
        client = Client('http://node1:9870')
        tools.append_to_hdfs(client,hdfs_path,data + '\n')
        return render(request,'home/detail.html',locals())
    else:
        return redirect(reverse('login'))


    # if not request.user.is_authenticated:
    #     return redirect(reverse('login'))
    # else:
    #     return render(request,'home/detail.html',locals())

from recommend import recommend
import redis
pool=redis.ConnectionPool(host='192.168.10.10',port=6379)
redis_client=redis.Redis(connection_pool=pool)
def recommend_book(request):
    if request.user.is_authenticated:
        userid=request.user.id
        recommend.getRecommendByUserID(userid,6)
        recommend_result=redis_client.get(userid)
        print("推荐的结果",recommend_result)
        booklist=str(recommend_result).split('|')
        print(booklist)
        if booklist[0] != 'None':
            bookset=[]
            for bk in booklist[:-1]:
                book_id=bk.split(",")[1]
                print("图书的ID为",book_id)
                bk_info=Book.objects.get(id=book_id)
                bookset.append(bk_info)
            print("推荐的图书信息",bookset)
            return render(request,'home/recommend.html',locals())
        else:
            bookset=Book.objects.order_by("rating")[:4]
            return render(request,'home/recommend.html',locals())
    else:
        return redirect(reverse('login'))

def log_in(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            forms_l = Login_Form()
            return render(request, 'auth/login.html', locals())
        elif request.method == 'POST':
            forms_l = Login_Form(request.POST)
            if forms_l.is_valid():
                user = forms_l.cleaned_data['user']
                pwd = forms_l.cleaned_data['pwd']
                user1 = authenticate(request, username=user, password=pwd)
                if user1:
                    login(request, user1)
                elif not user1:
                    pwderr = '用户名密码错误'
                    return render(request, 'auth/login.html', locals())
                return redirect(reverse('index'))
        else:
            return render(request,'home/index.html')

def register(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            forms = Reg_Form()
        elif request.method == 'POST':
            forms = Reg_Form(request.POST)
            if forms.is_valid():
                user = forms.cleaned_data['username']
                pwd = forms.cleaned_data['pwd']
                gender = forms.cleaned_data['gender']
                birthday = forms.cleaned_data['birthday']
                phone = forms.cleaned_data['phone']
                BookUser.objects.create_user(username=user, password=pwd, gender=gender, birthday=birthday, phone=phone)
                return redirect(reverse('login'))
            else:
                return render(request, 'auth/register.html', locals())
        return render(request, 'auth/register.html', locals())
    else:
        return HttpResponse("你已经登陆了")


def log_out(request):
    logout(request)
    return redirect(reverse('index'))
