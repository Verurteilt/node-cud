# Create your views here.
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
##################################################################
User = get_user_model()
#################################
from .forms import LoginForm, RegisterForm, TweetForm, EditForm
from .utils import twitters, tweetit
from .models import Tweet


def index(request):
    tweets = Tweet.objects.all().order_by('-id')[:20]
    print request.META['HTTP_USER_AGENT']
    print dir(request.META['HTTP_USER_AGENT'])
    return render(request, 'nodejs/home.html', locals())


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    mensaje = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            usuario = authenticate(username=email, password=password)
            if usuario is not None and usuario.is_active:
                login(request, usuario)
                return HttpResponseRedirect('/profile/' + usuario.email)
            else:
                mensaje = "<span class='alert alert-error'>User or password incorrect!</span>"
    else:
        form = LoginForm()
    return render(request, 'nodejs/login.html', locals())


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_view(request):
    mensaje = ""
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password_confirmation']
            user = User()
            user.email = email
            user.set_password(password)
            user.save()
            return HttpResponseRedirect('/profile/' + user.email)
        else:
            mensaje = "<span class='alert alert-error'>Something was wrong please try again</span>"
    else:
        form = RegisterForm()
    return render(request, 'nodejs/register.html', locals())


def profile_view(request, email):
    try:
        usuario = User.objects.get(email=email)
    except:
        raise Http404
    else:
        if request.method == "GET":
            tweets = twitters(usuario.consumer_key, usuario.consumer_secret, usuario.access_token, usuario.access_token_secret, 5)
            return render(request, 'nodejs/profile.html', locals())
        else:
            raise Http404


def edit_profile(request, email):
    if request.user.is_authenticated():
        pass
    else:
        return HttpResponseRedirect('/login')
    try:
        usuario = User.objects.get(email=email)
    except:
        raise Http404
    else:
        if request.method == "POST":
            form = EditForm(request.POST, request.FILES, instance=usuario)
            if 'profile_picture' in form.errors.keys():
                picture = usuario.profile_picture
            else:
                picture = form.cleaned_data['profile_picture']
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
        else:
            form = EditForm(instance=usuario)
        return render(request, 'nodejs/edit.html', locals())


def tweet_(request):
    if request.user.is_authenticated():
        usuario = request.user
    else:
        return HttpResponseRedirect('/login')
    form = TweetForm()
    return render(request, 'nodejs/tweet.html', locals())


@csrf_exempt
def new_tweet(request):
    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            usuario = User.objects.get(email=request.POST['author'])
            try:
                msg = tweetit(usuario, form.cleaned_data['tweet'])
                mes = "<span class='alert alert-success'>Succesfully Updated!</span>"
            except:
                mes = "<span class='alert alert-error'>Ooops Something wa Wrong!</span>"
            t = Tweet.objects.create(user=usuario, message=form.cleaned_data['tweet'])
            t.save()
            return HttpResponse(json.dumps({'user': t.user.first_name + ' ' + t.user.last_name, 'message': t.message, 'mes': mes, 'email': t.user.email}), mimetype="application/json")
    else:
        raise Http404
