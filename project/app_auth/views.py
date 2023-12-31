from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

def login(request):
    return render(request, 'app_auth/login.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=request.POST['password1'])
            login(request, user=user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'app_auth/register.html', {'form': form})

def login_view(request):
    redirect_url = reverse('profile')
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(redirect_url)
        else:
            return render(request, 'app_auth/login.html')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        return redirect(redirect_url)
    return render(request, 'app_auth/login.html',{'error':'Пользователь не найден'})

@login_required(login_url=reverse_lazy('login'))
def profile(request):
    return render(request, 'app_auth/profile.html')

# Create your views here.
