from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import SignUpForm
from .models import UserProfile
from django.contrib.auth.models import User

def home(request):
    return render(request, 'transactions/home.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # replace with your actual home URL name
        else:
            return render(request, 'transactions/login.html', {'error': 'Invalid credentials'})

    return render(request, 'transactions/login.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            UserProfile.objects.create(
                user=user,
                mobile_number=form.cleaned_data['mobile_number'],
                city=form.cleaned_data['city']
            )
            return redirect('login')  # or whatever your login URL name is
    else:
        form = SignUpForm()  # ✅ This line is essential

    return render(request, 'transactions/signup.html', {'form': form})

    
def signup_view(request):
    if request.method == 'POST':
        form = YourSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered!')
            return redirect('login')  # or redirect back to the same page
    else:
        form = YourSignUpForm()
    return render(request, 'signup.html', {'form': form})

