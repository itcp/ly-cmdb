from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse('<h1>Page was found</h1>')

#def confnginx(request):
#    #return HttpResponse('<h1>nginx was found</h1>')
#    return render(request, 'onlineconfig/conf_nginx.html')