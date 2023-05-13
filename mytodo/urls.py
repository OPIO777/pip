from mytodo import views
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    register,
    login_view,
    logout_view,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    todo_list,
)

urlpatterns = [
    path('home/', views.show, name='home'),
    path('register/', register, name='register'),
    path('task_delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('task_complete/<int:pk>/', views.task_complete, name='task_complete'),
    path('task_skip/<int:pk>/', views.task_skip, name='task_skip'),
    path('task_list/', views.task_list, name='task_list'),
    path('task_update/<int:pk>/', views.task_update, name='task_update'),
    path('task_create/', views.task_create, name='task_create'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', views.todo_list, name='todo_list'),
]
