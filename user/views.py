from django.contrib.auth import authenticate, login
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.template import RequestContext
from django import forms
from .forms import MyCustomUserForm, EditForm
from django.http.response import HttpResponse, JsonResponse
from .models import User, Follow
from django.views.decorators.csrf import csrf_exempt



def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'user/index.html')


def register(request):
    if request.method == 'POST':
        form = MyCustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            
            login(request, user)
            return redirect('index')
    else:
        form = MyCustomUserForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)

@csrf_exempt
def edit(request):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            user = User.objects.get(id=request.user.id)
            user.username = username
            user.email = email
            user.save()
            return JsonResponse({'status': 'ok'})
        else :
            return JsonResponse({'status': 'no'})

def show_profile(request, username, number_of_posts=2):
    nowUser = User.objects.get(id=request.user.id)
    try:
        user = User.objects.get(username=username)
    except:
        user = None
    if user is not None:
        followers = User.objects.filter(follow=user)
        if user.username == nowUser.username:
            return render(request, "user/profile.html",
                          {"user": nowUser, "owner": True, "other": user, "followers": followers,
                           "is_scroll": True})
        else:
            if user in nowUser.follow.all():
                return render(request, "user/profile.html",
                              {"user": nowUser, "owner": False, "follows": True, "other": user
                                  , "followers": followers, "is_scroll": True})
            else:
                return render(request, "user/profile.html",
                              {"user": nowUser, "owner": False, "follows": False, "other": user
                                  , "followers": followers, "is_scroll": True})
    else:
        return redirect("/home")

@csrf_exempt
def follow(request):
    if request.method == 'POST':
        currentUser = User.objects.get(id=request.user.id)
        username = request.POST.get('followed')
        user = User.objects.get(username=username)
        if len(Follow.objects.filter(follower=currentUser, followed=user)) == 0:
            Follow.objects.create(follower=currentUser, followed=user)
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'false': 'ok'})


@csrf_exempt
def unfollow(request):
    if request.method == 'POST':
        currentUser = User.objects.get(id=request.user.id)
        username = request.POST.get('followed', '')
        user = User.objects.get(username=username)
        # currentUser.follow.remove(user)
        if len(Follow.objects.filter(follower=currentUser, followed=user)) == 0:
            return
        f = Follow.objects.filter(follower=currentUser, followed=user)
        f.delete()
        return JsonResponse({'status': 'ok'})


def search_user(request):
    return render_to_response('user/list.html',{}, RequestContext(request))

def ajax_search(request):
    username = ''

    if request.method == 'GET':
        username = request.GET['username']

    return render_to_response('user/ajax_users.html', {'user_list': find_matching_users(username)}, RequestContext(request))

#helper method for AJAX search users, returns a list of the matching users based on search request
def find_matching_users(username=''):
    users = []

    if username :
        users = User.objects.filter(username__contains=username)

    return users