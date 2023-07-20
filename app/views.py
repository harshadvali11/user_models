from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.core.mail import send_mail
from app.forms import *
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






