from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistroForm
from .models import Profile
from .models import Event
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from .matematicas import combinaciones, permutaciones

def event_list(request):
    # Trae los eventos del usuario logueado
    eventos = Event.objects.filter(creador=request.user).order_by('fecha', 'hora')

    calc = None
    calc_error = None

    # Si el usuario envió el formulario de la calculadora
    if request.method == 'POST' and request.POST.get('calc') == '1':
        try:
            n = int(request.POST.get('n', ''))
            r = int(request.POST.get('r', ''))
            tipo = request.POST.get('tipo')

            # Validaciones
            if n < 0 or r < 0:
                calc_error = "N y R deben ser no negativos."
            elif r > n:
                calc_error = "R no puede ser mayor que N."
            else:
                valor = combinaciones(n, r) if tipo == 'combinacion' else permutaciones(n, r)
                calc = {
                    'n': n,
                    'r': r,
                    'tipo': tipo,
                    'valor': valor
                }
        except (TypeError, ValueError):
            calc_error = "Ingresa números enteros válidos."

    context = {
        'eventos': eventos,
        'calc': calc,
        'calc_error': calc_error
    }
    return render(request, 'events.html', context)


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def events(request):
    return render(request, "events.html")


@login_required
def create_event(request):
    return render(request, "create_event.html")


@login_required
def profile(request):
    return render(request, "profile.html")


def register(request):
    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            telefono = formulario.cleaned_data['telefono']
            Profile.objects.create(user=usuario, telefono=telefono)
            return redirect('login')  # Redirige al login
    else:
        formulario = RegistroForm()
    return render(request, 'register.html', {'form': formulario})

def dashboard_view(request):
    perfil = request.user.profile
    return render(request, 'dashboard.html', {'perfil': perfil})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Si usas email como username, necesitas buscar el usuario
        from django.contrib.auth.models import User
        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Correo no registrado'})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Asegúrate que esta URL existe
        else:
            return render(request, 'login.html', {'error': 'Contraseña incorrecta'})
    
    return render(request, 'login.html')

def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def create_event(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        ubicacion = request.POST.get('ubicacion')

        # Crear y guardar evento
        Event.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            fecha=fecha,
            hora=hora,
            ubicacion=ubicacion,
            creador=request.user  
        )
        return redirect('events')  

    return render(request, 'create_event.html')

@login_required
@login_required
def event_list(request):
    eventos = Event.objects.filter(creador=request.user).order_by('fecha', 'hora')

    calc = None
    calc_error = None

    if request.method == 'POST' and request.POST.get('calc') == '1':
        try:
            n = int(request.POST.get('n', ''))
            r = int(request.POST.get('r', ''))
            tipo = request.POST.get('tipo')
            if n < 0 or r < 0:
                calc_error = "N y R deben ser no negativos."
            elif r > n:
                calc_error = "R no puede ser mayor que N."
            else:
                valor = combinaciones(n, r) if tipo == 'combinacion' else permutaciones(n, r)
                calc = {'n': n, 'r': r, 'tipo': tipo, 'valor': valor}
        except (TypeError, ValueError):
            calc_error = "Ingresa números enteros válidos."

    context = {
        'eventos': eventos,
        'calc': calc,
        'calc_error': calc_error,
    }
    return render(request, 'events.html', context)

@login_required
def dashboard(request):
    hoy = timezone.now().date()
    primer_dia_mes = hoy.replace(day=1)
    proximo_mes = (hoy.replace(day=28) + timedelta(days=4)).replace(day=1)

    eventos_usuario = Event.objects.filter(creador=request.user)
    total_eventos = eventos_usuario.count()
    eventos_mes = eventos_usuario.filter(fecha__month=hoy.month, fecha__year=hoy.year).count()
    eventos_proximo_mes = eventos_usuario.filter(fecha__month=proximo_mes.month, fecha__year=proximo_mes.year).count()

    context = {
        'total_eventos': total_eventos,
        'eventos_mes': eventos_mes,
        'eventos_proximo_mes': eventos_proximo_mes,
        'eventos': eventos_usuario.order_by('fecha')[:5]  
    }
    return render(request, 'dashboard.html', context)

def detalle_evento(request, evento_id):
    evento = get_object_or_404(Event, id=evento_id)
    participantes = evento.participantes.count()

    # Ejemplo: grupos de 2 personas
    grupos_de_dos = combinaciones(participantes, 2)
    ordenamientos_de_tres = permutaciones(participantes, 3)

    return render(request, "detalle_evento.html", {
        "evento": evento,
        "grupos_de_dos": grupos_de_dos,
        "ordenamientos_de_tres": ordenamientos_de_tres,
    })