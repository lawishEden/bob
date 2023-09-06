from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, reverse, HttpResponse
from book_exam import settings
from book.models import Book
import os

def handle_upload_file(name,file):
    path = os.path.join(settings.BASE_DIR, 'uploads')
    fileName = path+'/' + name
    print(fileName)
    with open(fileName, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    insertToSQL(fileName)


def insertToSQL(fileName):
    txtfile = open(fileName, 'r', encoding='utf-8')
    for line in txtfile.readlines():
        try:
            bookinfo = line.split(',')
            id = bookinfo[0]
            name = bookinfo[1]
            rating = bookinfo[2]
            price = bookinfo[3]
            publish = bookinfo[4]
            url = bookinfo[5]

            try:
                # bk_entry = book(name=name, price=price, url=url, publish=publish, rating=rating)
                # bk_entry.save()
                Book.objects.create(name=name, rating=rating, price=price, publish=publish, url=url)
            except:
                print('save error' + id)
        except:
            print('read error ')



def importBookData(request):
    if request.method == 'POST' :
        file = request.FILES.get('file', None)
        if not file:
            return HttpResponse('None File uploads !')
        else:
            name = file.name
            handle_upload_file(name, file)
            return redirect(reverse('index'))
    return render(request, 'utils/upload.html')




if __name__ == '__main__':
    pass
