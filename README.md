# Moda - E-commerce Backend

**Moda** es el backend para una aplicación de comercio electrónico (e-commerce) enfocada en la venta de ropa, calzado y accesorios. Proporciona toda la lógica de negocio, almacenamiento de datos y gestión de catálogo necesaria para alimentar una tienda online funcional.

## 🚀 Funcionalidades Principales

Este proyecto gestiona los elementos fundamentales de un e-commerce:

- **Gestión de Catálogo:** Administración de productos, asociándolos a categorías (camisetas, zapatillas, abrigos...) y marcas (Nike, Zara, Levi's...).
- **Sistema de Usuarios:** Gestión de cuentas de usuario, direcciones de envío y listas de favoritos.
- **Carrito de Compras:** Funcionalidad para que los usuarios puedan añadir, eliminar y modificar cantidades de ítems en su carrito de compras activo.
- **Gestión de Pedidos (Checkout):** Conversión de carritos en pedidos formales con seguimiento de estados (Pendiente, Pagado, Enviado, Entregado, Cancelado) y congelación de precios históricos.

## 🛠️ Tecnologías y Stack

- **Lenguaje:** Python 3
- **Framework:** Django 5.x
- **Base de Datos:** SQLite (por defecto para entorno de desarrollo)
- **Gestión de Medios:** Django Media Storage para imágenes de productos y logos de marcas.

## 📦 Arquitectura de Datos (Modelos Clave)

El sistema se apoya en los siguientes modelos relacionales principales (`Moda/models.py`):

- **`Marca` y `Categoria`**: Permiten organizar el inventario.
- **`Producto`**: Contiene nombre, descripción, precio, stock, imagen, y se relaciona con una Marca (`ForeignKey`) y múltiples Categorías (`ManyToManyField`).
- **`Carrito` e `ItemCarrito`**: Lógica temporal para los productos que el usuario desea comprar.
- **`Pedido` e `ItemPedido`**: Registros inmutables de las compras realizadas, guardando el precio en el momento de la compra para evitar discrepancias si el catálogo cambia.

## ⚙️ Instalación y Configuración Local

Si deseas correr este proyecto en tu entorno de desarrollo local, sigue estos pasos:

1. **Clona el repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd final-backend/Moda
   ```

2. **Crea y activa tu entorno virtual:**
   ```bash
   # En macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # En Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install django
   ```

4. **Inicia el servidor:**
   *Nota: La base de datos ya viene con un volcado de prueba (`seed`) que incluye productos y fotos para empezar a probar inmediatamente.*
   ```bash
   python manage.py runserver
   ```

5. **Acceso:**
   - App: `http://127.0.0.1:8000/`
   - Panel de Administración: `http://127.0.0.1:8000/admin/`

---
*Desarrollado como proyecto de backend.*
