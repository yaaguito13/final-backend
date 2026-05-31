<h1 align="center"> Backend E-commerce Moda </h1>

<p align="center">
<img src="https://img.shields.io/badge/STATUS-EN%20DESARROLLO-green">
<img src="https://img.shields.io/badge/Python-3-blue">
<img src="https://img.shields.io/badge/Django-Framework-red">
</p>

## Índice
* [Descripción del proyecto](#descripción-del-proyecto)
* [Estado del proyecto](#estado-del-proyecto)
* [Características de la aplicación](#características-de-la-aplicación)
* [Acceso al proyecto](#acceso-al-proyecto)
* [Tecnologías utilizadas](#tecnologías-utilizadas)
* [Personas desarrolladoras del proyecto](#personas-desarrolladoras-del-proyecto)

## Descripción del Proyecto
Este es el proyecto de backend para la aplicación de e-commerce "Moda". Está desarrollado en Python utilizando el framework **Django**. Gestiona de forma centralizada todo el catálogo de la tienda (categorías, marcas y productos), así como la lógica de usuarios, carritos de compra y pedidos (checkout). El objetivo principal es ofrecer un backend robusto y un panel de administración estructurado para gestionar la tienda online de forma eficiente.

## Estado del proyecto
<h4 align="center">
:construction: Proyecto en construcción :construction:
</h4>

## Características de la aplicación
- `Gestión de Catálogo`: Funcionalidades completas (CRUD) de Categorías, Marcas y Productos con soporte para imágenes.
- `Múltiples Categorías`: Organización de productos en Hombre, Mujer, Tops, Bañadores, Vestidos, etc.
- `Gestión de Carrito`: Manejo de carritos activos de usuarios (ItemCarrito) incluyendo tallas y colores.
- `Gestión de Pedidos`: Historial de compras y estados de entrega (Procesando, Enviado, Entregado).
- `Panel de Administración`: Configurado a través del admin nativo de Django, con la base de datos ya poblada de pruebas (`db.sqlite3`).

## Acceso al proyecto

### 📁 Descarga
Puedes descargar el proyecto clonando el repositorio directamente desde tu terminal:
```bash
git clone <URL_DEL_REPOSITORIO>
cd final-backend
```

### 🛠️ Abre y ejecuta el proyecto
1. **Activa el entorno virtual** que ya viene configurado:
   ```bash
   source .venv/bin/activate
   ```
2. **Navega a la carpeta principal de Django** (donde está el `manage.py`):
   ```bash
   cd Moda
   ```
3. **Ejecuta el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```
4. **Accede al Panel de Administrador:**
   Abre tu navegador en `http://localhost:8000/admin/`.  
   (Las credenciales actuales de superusuario para desarrollo son: Usuario: `admin` / Contraseña: `password123`).

## Tecnologías utilizadas
* `Python` (Lenguaje principal)
* `Django` (Framework Backend y ORM)
* `SQLite3` (Base de datos de desarrollo)

## Personas desarrolladoras del proyecto
| [<img src="https://github.com/identicons/yago.png" width=115><br><sub>Yago Pazos Lema</sub>](https://github.com/yagopazoslema) |
| :---: |
