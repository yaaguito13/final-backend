import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import Producto, Marca, Favorito, Carrito, ItemCarrito # <-- Añade Carrito e ItemCarrito



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


def detalle_producto(request, producto_id):
    """
    Endpoint para ver un solo producto (Método GET).
    Usa Path Params (producto_id en la URL). Ej: /api/productos/1/
    """
    if request.method == 'GET':
        try:
            # Buscamos el producto exacto por su ID
            p = Producto.objects.get(id=producto_id)

            # Preparamos los datos extra (categorías e imagen)
            categorias = list(p.categorias.values_list('nombre', flat=True))
            imagen_url = request.build_absolute_uri(p.imagen.url) if p.imagen else None

            # Construimos el diccionario con los detalles
            datos_producto = {
                'id': p.id,
                'nombre': p.nombre,
                'precio': str(p.precio),
                'marca': p.marca.nombre,
                'categorias': categorias,
                'imagen': imagen_url
            }

            return JsonResponse(datos_producto, status=200)

        except Producto.DoesNotExist:
            # Si nos piden un ID que no existe, devolvemos error 404 (Not Found)
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)

    return JsonResponse({'error': 'Método no permitido, usa GET'}, status=405)


@csrf_exempt
def gestionar_favoritos(request):
    """
    Endpoint para ver (GET) y añadir (POST) favoritos.
    """
    if request.method == 'GET':
        # Leemos el ID del usuario desde la URL (Ej: /api/favoritos/?usuario_id=2)
        usuario_id = request.GET.get('usuario_id')

        if not usuario_id:
            return JsonResponse({'error': 'Falta el parámetro usuario_id'}, status=400)

        favoritos = Favorito.objects.filter(usuario_id=usuario_id)
        datos_favoritos = []

        for fav in favoritos:
            p = fav.producto
            imagen_url = request.build_absolute_uri(p.imagen.url) if p.imagen else None
            datos_favoritos.append({
                'favorito_id': fav.id,
                'producto_id': p.id,
                'nombre': p.nombre,
                'precio': str(p.precio),
                'marca': p.marca.nombre,
                'imagen': imagen_url
            })

        return JsonResponse({'favoritos': datos_favoritos}, status=200)

    elif request.method == 'POST':
        # Añadir un producto a favoritos
        try:
            datos = json.loads(request.body)
            usuario_id = datos.get('usuario_id')
            producto_id = datos.get('producto_id')

            usuario = User.objects.get(id=usuario_id)
            producto = Producto.objects.get(id=producto_id)

            # Comprobamos si ya lo tenía en favoritos para no duplicarlo
            if Favorito.objects.filter(usuario=usuario, producto=producto).exists():
                return JsonResponse({'mensaje': 'El producto ya está en favoritos'}, status=200)

            Favorito.objects.create(usuario=usuario, producto=producto)
            return JsonResponse({'mensaje': 'Añadido a favoritos correctamente'}, status=201)

        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Error: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def eliminar_favorito(request, producto_id):
    """
    Endpoint para quitar un producto de favoritos (Método DELETE).
    Usa el producto_id en la ruta y el usuario_id en la query.
    Ej: DELETE /api/favoritos/1/?usuario_id=2
    """
    if request.method == 'DELETE':
        usuario_id = request.GET.get('usuario_id')

        if not usuario_id:
            return JsonResponse({'error': 'Falta el parámetro usuario_id'}, status=400)

        try:
            # Buscamos el favorito exacto de ese usuario y ese producto
            favorito = Favorito.objects.get(usuario_id=usuario_id, producto_id=producto_id)
            favorito.delete()
            return JsonResponse({'mensaje': 'Producto eliminado de favoritos'}, status=200)

        except Favorito.DoesNotExist:
            return JsonResponse({'error': 'El producto no estaba en favoritos'}, status=404)

    return JsonResponse({'error': 'Método no permitido, usa DELETE'}, status=405)


@csrf_exempt
def gestionar_carrito(request):
    """
    Endpoint para ver el carrito (GET) y añadir productos (POST).
    """
    if request.method == 'GET':
        usuario_id = request.GET.get('usuario_id')
        if not usuario_id:
            return JsonResponse({'error': 'Falta usuario_id'}, status=400)

        try:
            usuario = User.objects.get(id=usuario_id)
            # get_or_create es magia pura: si el usuario no tiene carrito, se lo crea automáticamente.
            carrito, created = Carrito.objects.get_or_create(usuario=usuario)

            items = carrito.items.all()
            datos_items = []
            total_carrito = 0.0  # Aquí iremos sumando el dinero

            for item in items:
                p = item.producto
                imagen_url = request.build_absolute_uri(p.imagen.url) if p.imagen else None
                # Calculamos el subtotal de este artículo (precio x cantidad)
                subtotal = float(p.precio) * item.cantidad
                total_carrito += subtotal

                datos_items.append({
                    'item_id': item.id,
                    'producto_id': p.id,
                    'nombre': p.nombre,
                    'precio_unitario': str(p.precio),
                    'cantidad': item.cantidad,
                    'talla': item.talla,
                    'color': item.color,
                    'subtotal': str(subtotal),
                    'imagen': imagen_url
                })

            return JsonResponse({
                'carrito_id': carrito.id,
                'items': datos_items,
                'total_carrito': str(total_carrito)
            }, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    elif request.method == 'POST':
        try:
            datos = json.loads(request.body)
            usuario_id = datos.get('usuario_id')
            producto_id = datos.get('producto_id')
            cantidad = datos.get('cantidad', 1)  # Si no nos envían cantidad, asumimos que es 1
            talla = datos.get('talla', '')
            color = datos.get('color', '')

            usuario = User.objects.get(id=usuario_id)
            producto = Producto.objects.get(id=producto_id)

            # Buscamos o creamos el carrito del usuario
            carrito, created = Carrito.objects.get_or_create(usuario=usuario)

            # Comprobamos si EXACTAMENTE este producto (misma talla y color) ya está en la cesta
            item_existente = ItemCarrito.objects.filter(
                carrito=carrito, producto=producto, talla=talla, color=color
            ).first()

            if item_existente:
                # Si ya existe, solo sumamos la cantidad
                item_existente.cantidad += cantidad
                item_existente.save()
                mensaje = 'Cantidad actualizada en el carrito'
            else:
                # Si no existe, creamos el nuevo artículo en la cesta
                ItemCarrito.objects.create(
                    carrito=carrito, producto=producto,
                    cantidad=cantidad, talla=talla, color=color
                )
                mensaje = 'Producto añadido al carrito'

            return JsonResponse({'mensaje': mensaje}, status=201)

        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)