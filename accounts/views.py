from django.shortcuts import render,redirect
from django.contrib import auth

# Create your views here.
def login(request):
    if request.method == 'POST':
        usr = request.POST['username']
        pwd = request.POST['password']
        user = auth.authenticate(request,username=usr,password=pwd)
        if user is not None:
            auth.login(request,user)
            return redirect('main:showmain')
        else:
            return render(request,'login.html')
    elif request.method == 'GET':
        return render(request,'login.html')

def logout(requset):
    auth.logout(requset)
    return redirect('main:showmain')
