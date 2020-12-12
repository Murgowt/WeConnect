from django.shortcuts import render,redirect
from .forms import UserCreateForm,UserProfileForm,FriendRequestForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import  UserProfile,FriendRequest
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def HomePage(request):
    profile=UserProfile.objects.get(user=request.user)
    friends=profile.friends.all()
    frs=[]
    try :
        frr=FriendRequest.objects.filter(receiver=request.user,is_active=True)
        frs=[]
        for i in frr:
            frs.append(i.sender.username)
    except:
        frs=['No Friends']
    context={'friends':friends,'frs':frs}

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


@login_required(login_url='login')
def SendFrReq(request):
    frf = FriendRequestForm()
    msg=''
    if (request.method == "POST"):
        fr = FriendRequestForm(request.POST)
        if(fr.is_valid()):
            freq=fr.save(commit=False)
            freq.sender=request.user
            freq.save()
            msg="Friend Request Sent"
        fr.sender = request.user

    return (render(request, 'SendFriendReq.html', {'friendRF': frf,'msg':msg}))



def RegisterPage(request):
    if(request.user.is_authenticated):
        return redirect('home')
    if(request.method=="POST"):
        form=UserCreateForm(request.POST)
        profile_form=UserProfileForm(request.POST)

        if(form.is_valid() and profile_form.is_valid()):
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


def SearchChat(request):

    return(render(request,'ChatSearch.html'))

@login_required(login_url='login')
def AcceptFR(request,username):
    usr=User.objects.get(username=username)
    frr=FriendRequest.objects.get(sender=usr,receiver=request.user)
    frr.accept()
    frr.save()
    return redirect('SendFR')
