from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, UserJsonUploadForm
from .models import UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserJsonUploadSerializer
from .models import UserJsonUpload



def home(request):
    return render(request, 'transactions/home.html')


# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('upload')  # Ensure 'upload' is defined in urls.py
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'transactions/login.html')

    return render(request, 'transactions/login.html')


# Signup View
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully registered!')
            form = SignUpForm()  # Clear form after success
    else:
        form = SignUpForm()
    return render(request, 'transactions/signup.html', {'form': form})


# Upload JSON Data View
def upload_user_data(request):
    if request.method == 'POST':
        form = UserJsonUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data submitted successfully!')
            return redirect('login')
    else:
        form = UserJsonUploadForm()

    return render(request, 'transactions/upload_form.html', {'form': form})


class UserJsonUploadAPI(APIView):
    def post(self, request):
        serializer = UserJsonUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Data uploaded successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
