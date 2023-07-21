from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
# Create your views here.
from django.core.mail import send_mail
from app.forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required



def registration(request):
    usfo=UserForm()
    pfo=ProfileForm()
    d={'usfo':usfo,'pfo':pfo}

    if request.method=='POST' and request.FILES:
        usfd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if usfd.is_valid() and pfd.is_valid():

            NSUFO=usfd.save(commit=False)
            submittedPW=usfd.cleaned_data['password']
            NSUFO.set_password(submittedPW)
            NSUFO.save()

            NSPO=pfd.save(commit=False)
            NSPO.username=NSUFO
            NSPO.save()

            send_mail('Registration',
                    'Ur Registration is Successfull',
                      'shaikharshadvali79@gmail.com',
                      [NSUFO.email],
                      fail_silently=False
                          )



            return HttpResponse('Registration is Succeffully check in admin')



    return render(request,'registration.html',d)

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Not a Active User')
        else:
            return HttpResponse('Invalid Details')
    return render(request,'user_login.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))








