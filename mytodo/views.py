from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import TaskingForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserLoginForm, UserResetPasswordForm
from .models import Tasking


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('todo_list')
            else:
                messages.warning(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

class CustomPasswordResetView(PasswordResetView):
    form_class = UserResetPasswordForm
    template_name = 'todo/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'todo/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'todo/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'todo/password_reset_complete.html'

def show(request):
    return render(request, 'home.html')




@login_required
def todo_list(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        Tasking.objects.create(user=request.user, task=task)
        return redirect('task_list')
    else:
        todos = Tasking.objects.filter(user=request.user)
        return render(request, 'task_list.html', {'todos': todos})

@login_required
def task_list(request):
    tasks = Tasking.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskingForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskingForm()
    return render(request, 'task_form.html', {'form': form, 'form_title': 'form_title'})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Tasking, pk=pk)
    if request.method == 'POST':
        form = TaskingForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return redirect('task_list')
    else:
        form = TaskingForm(instance=task)
    return render(request, 'task_form.html', {'form': form, 'form_title': 'Update Task'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Tasking, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})

@login_required
def task_complete(request, pk):
    task = get_object_or_404(Tasking, pk=pk)
    task.completed = True
    task.save()
    return redirect('task_list')

@login_required
def task_skip(request, pk):
    task = get_object_or_404(Tasking, pk=pk)
    task.skipped = True
    task.save()
    return redirect('task_list')

