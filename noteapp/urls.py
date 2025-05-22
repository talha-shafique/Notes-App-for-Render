from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.note_list, name='note_list'),
    path('add/',views.add_note, name='add_note'),
    path('edit/<int:id>/', views.edit_note, name='edit_note'),
    path('delete/<int:id>/', views.delete_note, name='delete_note'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
        ]
