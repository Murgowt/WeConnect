from django.shortcuts import render,redirect
from .forms import UserCreateForm,UserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import  UserProfile
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def HomePage(request):
    profile=UserProfile.objects.get(user=request.user)
    friends=profile.friends.all()
    context={'friends':friends}
    return(render(request,'home.html',context))

def LoginPage(request):
    if(request.user.is_authenticated):
        return redirect('home')
    if(request.method=="POST"):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    return(render(request,'Login.html'))

def RegisterPage(request):
    if(request.user.is_authenticated):
        return redirect('home')
    if(request.method=="POST"):
        form=UserCreateForm(request.POST)
        profile_form=UserProfileForm(request.POST)
        print('ezwrxctfvg')

        if(form.is_valid() and profile_form.is_valid()):
            print('poll')
            user=form.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()
            return redirect('login')

    form = UserCreateForm()
    user_profile_form=UserProfileForm()
    return(render(request,'Register.html',{'form':form,'userprofile':user_profile_form}))

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('login')
