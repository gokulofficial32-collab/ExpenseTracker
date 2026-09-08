from django.contrib import admin
from django.urls import path
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('login/', views.signin, name='login'),

    path('signup/', views.signup, name='signup'),

    path(
        'delete/<int:expense_id>/',
        views.delete_expense,
        name='delete_expense'
    ),

    path(
        'edit/<int:expense_id>/',
        views.edit_expense,
        name='edit_expense'
    ),
]