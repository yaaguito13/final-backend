import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import Producto, Marca


@csrf_exempt  # Desactiva la protección CSRF web para permitir peticiones desde Android
def registro_usuario(request):
    """Endpoint para registrar un nuevo usuario (Método POST)"""
    if request.method == 'POST':
        try:
            # Leemos los datos en formato JSON que nos enviará la app (o Postman)
            datos = json.loads(request.body)
            username = datos.get('username')
            email = datos.get('email')
            password = datos.get('password')

            # Comprobamos si el usuario ya existe
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'El nombre de usuario ya está en uso'}, status=400)

            # Creamos el usuario de forma segura
            user = User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({'mensaje': 'Usuario creado con éxito', 'id': user.id}, status=201)

        except Exception as e:
            return JsonResponse({'error': f'Error en los datos: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Método no permitido, usa POST'}, status=405)


@csrf_exempt
def login_usuario(request):
    """Endpoint para iniciar sesión (Método POST)"""
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
            username = datos.get('username')
            password = datos.get('password')

            # Django comprueba si el usuario y la contraseña coinciden en la base de datos
            user = authenticate(username=username, password=password)

            if user is not None:
                # Login correcto
                return JsonResponse({
                    'mensaje': 'Login exitoso',
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }, status=200)
            else:
                # Credenciales inválidas
                return JsonResponse({'error': 'Usuario o contraseña incorrectos'}, status=401)

        except Exception as e:
            return JsonResponse({'error': f'Error en los datos: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Método no permitido, usa POST'}, status=405)


def lista_marcas(request):
    """Endpoint para obtener todas las marcas con su imagen (Método GET)"""
    if request.method == 'GET':
        marcas = Marca.objects.all()
        datos_marcas = []
        for m in marcas:
            # Comprobamos si la marca tiene imagen para no causar errores
            imagen_url = request.build_absolute_uri(m.imagen.url) if m.imagen else None

            datos_marcas.append({
                'id': m.id,
                'nombre': m.nombre,
                'imagen': imagen_url
            })

        return JsonResponse({'marcas': datos_marcas}, status=200)

    return JsonResponse({'error': 'Método no permitido, usa GET'}, status=405)


def catalogo_productos(request):
    """Endpoint para obtener los productos con sus imágenes (Método GET)"""
    if request.method == 'GET':
        marca_query = request.GET.get('marca', None)

        if marca_query:
            productos = Producto.objects.filter(marca__nombre__icontains=marca_query)
        else:
            productos = Producto.objects.all()

        datos_productos = []
        for p in productos:
            categorias = list(p.categorias.values_list('nombre', flat=True))
            imagen_url = request.build_absolute_uri(p.imagen.url) if p.imagen else None

            datos_productos.append({
                'id': p.id,
                'nombre': p.nombre,
                'precio': str(p.precio),
                'marca': p.marca.nombre,
                'categorias': categorias,
                'imagen': imagen_url  # Añadimos la URL de la foto al JSON
            })

        return JsonResponse({'productos': datos_productos}, status=200)

    return JsonResponse({'error': 'Método no permitido, usa GET'}, status=405)