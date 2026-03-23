import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt


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