from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Ticket, Cliente, Dispositivo
from .forms import NuevoTicketForm, CambiarEstadoForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'crm/login.html')

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('login')

# RNF1: El decorador exige autenticación para acceder al Dashboard
@login_required(login_url='/login/')
def dashboard(request):
    # Obtenemos todos los tickets ordenados por fecha de actualización
    tickets = Ticket.objects.all().order_by('-fecha_actualizacion')
    return render(request, 'crm/dashboard.html', {'tickets': tickets})

@login_required(login_url='/login/')
def crear_ticket(request):
    if request.method == 'POST':
        form = NuevoTicketForm(request.POST)
        if form.is_valid():
            # 1. Crear o buscar al Cliente (RF1)
            cliente, created = Cliente.objects.get_or_create(
                correo=form.cleaned_data['correo'],
                defaults={
                    'nombre': form.cleaned_data['nombre_cliente'],
                    'telefono': form.cleaned_data['telefono']
                }
            )
            
            # 2. Registrar el Dispositivo (RF2)
            dispositivo, created = Dispositivo.objects.get_or_create(
                serie=form.cleaned_data['serie'],
                defaults={
                    'cliente': cliente,
                    'marca': form.cleaned_data['marca'],
                    'modelo': form.cleaned_data['modelo']
                }
            )
            
            # 3. Crear el Ticket
            Ticket.objects.create(dispositivo=dispositivo, estado='Ingreso')
            
            return redirect('dashboard')
    else:
        form = NuevoTicketForm()
        
    return render(request, 'crm/nuevo_ticket.html', {'form': form})

@login_required(login_url='/login/')
def actualizar_estado(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = CambiarEstadoForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save() # Se actualiza el estado (RF3)
            return redirect('dashboard')
            
    return redirect('dashboard')