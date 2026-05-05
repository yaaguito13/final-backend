import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import Categoria, Producto, Marca, Favorito, Carrito, ItemCarrito, Direccion, Pedido, ItemPedido



@csrf_exempt  # Desactiva la protección CSRF web para permitir peticiones desde Android
def registro_usuario(request):
    """Endpoint para registrar un nuevo usuario (Metodo POST)"""
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
    """Endpoint para iniciar sesión (Metodo POST)"""
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
    """Endpoint para obtener todas las marcas con su imagen (Metodo GET)"""
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
    """Endpoint para obtener los productos con sus imágenes (Metodo GET)"""
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
    Endpoint para ver un solo producto (Metodo GET).
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
    Endpoint para quitar un producto de favoritos (Metodo DELETE).
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


@csrf_exempt
def gestionar_direcciones(request):
    """
    Endpoint para ver (GET) y añadir (POST) direcciones de envío.
    """
    if request.method == 'GET':
        usuario_id = request.GET.get('usuario_id')
        if not usuario_id:
            return JsonResponse({'error': 'Falta el parámetro usuario_id'}, status=400)

        direcciones = Direccion.objects.filter(usuario_id=usuario_id)
        datos_direcciones = []

        for d in direcciones:
            datos_direcciones.append({
                'id': d.id,
                'titulo': d.titulo,
                'calle': d.calle,
                'ciudad': d.ciudad,
                'codigo_postal': d.codigo_postal
            })

        return JsonResponse({'direcciones': datos_direcciones}, status=200)

    elif request.method == 'POST':
        try:
            datos = json.loads(request.body)
            usuario_id = datos.get('usuario_id')
            titulo = datos.get('titulo')  # Ej: "Casa" o "Trabajo"
            calle = datos.get('calle')
            ciudad = datos.get('ciudad')
            codigo_postal = datos.get('codigo_postal')

            usuario = User.objects.get(id=usuario_id)

            # Creamos la nueva dirección en la base de datos
            Direccion.objects.create(
                usuario=usuario,
                titulo=titulo,
                calle=calle,
                ciudad=ciudad,
                codigo_postal=codigo_postal
            )
            return JsonResponse({'mensaje': 'Dirección guardada correctamente'}, status=201)

        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Error al guardar: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


def lista_categorias(request):
    """
    Endpoint para obtener todas las categorías con su imagen (Metodo GET)
    """
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        datos_categorias = []

        for c in categorias:
            # Preparamos la URL de la imagen si existe
            imagen_url = request.build_absolute_uri(c.imagen.url) if c.imagen else None

            datos_categorias.append({
                'id': c.id,
                'nombre': c.nombre,
                'imagen': imagen_url
            })

        return JsonResponse({'categorias': datos_categorias}, status=200)

    return JsonResponse({'error': 'Método no permitido, usa GET'}, status=405)


def perfil_usuario(request):
    """
    Endpoint para obtener los datos del perfil del usuario (Metodo GET)
    Ejemplo de uso: /api/perfil/?usuario_id=2
    """
    if request.method == 'GET':
        usuario_id = request.GET.get('usuario_id')

        if not usuario_id:
            return JsonResponse({'error': 'Falta el parámetro usuario_id'}, status=400)

        try:
            usuario = User.objects.get(id=usuario_id)

            # Formateamos los datos del usuario para enviarlos
            datos_usuario = {
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
                # Convertimos la fecha de registro a un formato legible de texto
                'fecha_registro': usuario.date_joined.strftime("%Y-%m-%d")
            }

            return JsonResponse({'perfil': datos_usuario}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    return JsonResponse({'error': 'Método no permitido, usa GET'}, status=405)


@csrf_exempt
def checkout_pedido(request):
    """
    Endpoint para convertir el Carrito en un Pedido definitivo (Metodo POST).
    """
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
            usuario_id = datos.get('usuario_id')

            usuario = User.objects.get(id=usuario_id)
            carrito = Carrito.objects.get(usuario=usuario)
            items_carrito = carrito.items.all()

            # 1. Comprobamos que el carrito no esté vacío
            if not items_carrito.exists():
                return JsonResponse({'error': 'El carrito está vacío'}, status=400)

            # 2. Creamos el ticket de compra (Pedido)
            nuevo_pedido = Pedido.objects.create(usuario=usuario, total=0)
            total_pedido = 0.0

            # 3. Copiamos los artículos del carrito al pedido
            for item in items_carrito:
                precio_historico = item.producto.precio  # Guardamos el precio que tiene HOY

                ItemPedido.objects.create(
                    pedido=nuevo_pedido,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio_unitario=precio_historico,
                    talla=item.talla,
                    color=item.color
                )
                total_pedido += float(precio_historico) * item.cantidad

            # 4. Actualizamos el total del ticket
            nuevo_pedido.total = total_pedido
            nuevo_pedido.save()

            # 5. ¡Vaciamos el carrito!
            items_carrito.delete()

            return JsonResponse({
                'mensaje': '¡Pedido realizado con éxito!',
                'pedido_id': nuevo_pedido.id
            }, status=201)

        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except Carrito.DoesNotExist:
            return JsonResponse({'error': 'El usuario no tiene carrito activo'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Error al procesar el pago: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


def historial_pedidos(request):
    """
    Endpoint para ver la pantalla de "Mis Pedidos" (Metodo GET).
    Ejemplo: /api/pedidos/?usuario_id=2
    """
    if request.method == 'GET':
        usuario_id = request.GET.get('usuario_id')
        if not usuario_id:
            return JsonResponse({'error': 'Falta el parámetro usuario_id'}, status=400)

        pedidos = Pedido.objects.filter(usuario_id=usuario_id).order_by('-fecha_creacion')
        datos_pedidos = []

        for pedido in pedidos:
            # Sacamos los artículos de este pedido en concreto
            items = pedido.items.all()
            datos_items = []

            for item in items:
                nombre_prod = item.producto.nombre if item.producto else 'Producto descatalogado'
                imagen_url = request.build_absolute_uri(
                    item.producto.imagen.url) if item.producto and item.producto.imagen else None

                datos_items.append({
                    'nombre': nombre_prod,
                    'cantidad': item.cantidad,
                    'talla': item.talla,
                    'color': item.color,
                    'precio_unitario': str(item.precio_unitario),
                    'imagen': imagen_url
                })

            datos_pedidos.append({
                'pedido_id': pedido.id,
                'fecha': pedido.fecha_creacion.strftime("%d-%m-%Y %H:%M"),
                'estado': pedido.estado,  # "Procesando", "Enviado"...
                'total': str(pedido.total),
                'articulos': datos_items
            })

        return JsonResponse({'pedidos': datos_pedidos}, status=200)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def modificar_item_carrito(request, item_id):
    """
    Endpoint para modificar la cantidad (PUT) o borrar un artículo del carrito (DELETE).
    Usa Path Params (item_id en la URL). Ej: /api/carrito/1/
    """
    try:
        # Buscamos el artículo específico dentro del carrito
        item = ItemCarrito.objects.get(id=item_id)
    except ItemCarrito.DoesNotExist:
        return JsonResponse({'error': 'El artículo no existe en el carrito'}, status=404)

    if request.method == 'PUT':
        try:
            # Leemos la nueva cantidad que nos envía la app
            datos = json.loads(request.body)
            nueva_cantidad = datos.get('cantidad')

            if nueva_cantidad is not None and int(nueva_cantidad) > 0:
                item.cantidad = int(nueva_cantidad)
                item.save()
                return JsonResponse({'mensaje': 'Cantidad actualizada correctamente'}, status=200)
            else:
                return JsonResponse({'error': 'La cantidad debe ser un número mayor que 0'}, status=400)

        except Exception as e:
            return JsonResponse({'error': f'Error en los datos: {str(e)}'}, status=400)

    elif request.method == 'DELETE':
        # Borramos el artículo de la base de datos
        item.delete()
        return JsonResponse({'mensaje': 'Artículo eliminado del carrito'}, status=200)

    return JsonResponse({'error': 'Método no permitido, usa PUT o DELETE'}, status=405)