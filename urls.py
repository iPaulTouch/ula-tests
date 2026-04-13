from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('nuevo_ticket/', views.crear_ticket, name='crear_ticket'),
    path('actualizar_estado/<int:ticket_id>/', views.actualizar_estado, name='actualizar_estado'),
]