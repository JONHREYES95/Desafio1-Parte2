# Sistema de Servicios Empresariales — Prototipo Funcional

**Asignatura:** Desarrollo de Sotware Empresarial  
**Institución:** Universidad Don Bosco  
**Entrega:** Desafío 1 — Parte 2

---

## Equipo de Desarrollo

| Nombre | Carnét |
|--------|-------|
| Reyes Jonathan Rafael | SR232918 |
| Zelaya Ramírez Jordán Ismael | ZR170168 |
| Aguillón González Ricardo José | AG242725 |
| Berdugo Artiga Lisandro Rafael | BA131462 |
| Barahona García Miguel Ángel | BG191322 |

---

## Descripción General

Este repositorio contiene el prototipo funcional de un **sistema de gestión de servicios empresariales** construido sobre una **arquitectura de tres capas (3-Tier Architecture)**. El objetivo del prototipo es demostrar el flujo completo de datos entre la capa de presentación, la capa de lógica de negocio y la capa de persistencia, utilizando un stack tecnológico liviano y de rápida configuración, adecuado para el contexto de desarrollo empresarial interno.

---

## Arquitectura del Sistema

El prototipo implementa el patrón de **arquitectura de tres capas**, separando responsabilidades de la siguiente manera:

```
┌─────────────────────────────────────────────────────┐
│              CAPA DE PRESENTACIÓN                   │
│   Jinja2 Templates + Bootstrap 5 (CDN)              │
│   base.html · clientes.html · solicitudes.html      │
└──────────────────────┬──────────────────────────────┘
                       │  HTTP (GET / POST)
┌──────────────────────▼──────────────────────────────┐
│            CAPA DE LÓGICA DE NEGOCIO                │
│   Python 3 + Flask (app.py)                         │
│   Rutas, validaciones y coordinación de datos       │
└──────────────────────┬──────────────────────────────┘
                       │  sqlite3 (Python stdlib)
┌──────────────────────▼──────────────────────────────┐
│             CAPA DE PERSISTENCIA DE DATOS           │
│   SQLite 3 — archivo local: empresa.db              │
│   Tablas: clientes · servicios · solicitudes        │
└─────────────────────────────────────────────────────┘
```

### Capa 1 — Presentación

Implementada con el motor de plantillas **Jinja2** integrado en Flask, utilizando herencia de plantillas mediante un archivo base (`base.html`) que provee la estructura HTML común y el navbar de navegación. Los estilos y componentes interactivos se cargan directamente desde el CDN oficial de **Bootstrap 5**, eliminando dependencias de archivos estáticos locales.

### Capa 2 — Lógica de Negocio

Concentrada íntegramente en `app.py`. Flask gestiona el ciclo de vida HTTP, el enrutamiento y la lógica de validación de formularios. No se emplea ORM; la interacción con la base de datos se realiza mediante la librería estándar `sqlite3`, lo que reduce la complejidad de configuración y permite un control directo sobre las sentencias SQL.

### Capa 3 — Persistencia

Base de datos **SQLite 3** almacenada en un único archivo (`empresa.db`) generado automáticamente en el directorio raíz del proyecto al primer arranque. Las tablas se crean mediante DDL ejecutado desde la función `init_db()` en `app.py`.

---

## Modelo de Datos

```
┌──────────────┐       ┌──────────────────┐       ┌─────────────┐
│   clientes   │       │   solicitudes    │       │  servicios  │
├──────────────┤       ├──────────────────┤       ├─────────────┤
│ id (PK)      │◄──┐   │ id (PK)          │  ┌───►│ id (PK)     │
│ nombre       │   └───│ cliente_id (FK)  │  │   │ nombre      │
│ telefono     │       │ servicio_id (FK) │──┘   └─────────────┘
│ correo       │       │ estado           │
└──────────────┘       └──────────────────┘
```

### Tabla `clientes`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER PK AUTOINCREMENT | Identificador único del cliente |
| `nombre` | TEXT NOT NULL | Nombre completo |
| `telefono` | TEXT | Número de contacto |
| `correo` | TEXT | Dirección de correo electrónico |

### Tabla `servicios`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER PK AUTOINCREMENT | Identificador único |
| `nombre` | TEXT NOT NULL | Descripción del servicio |

> Se inicializa con tres registros fijos al primer arranque: **Mantenimiento Preventivo**, **Reparación**, **Limpieza**.

### Tabla `solicitudes`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER PK AUTOINCREMENT | Identificador único |
| `cliente_id` | INTEGER FK | Referencia a `clientes.id` |
| `servicio_id` | INTEGER FK | Referencia a `servicios.id` |
| `estado` | TEXT DEFAULT 'Pendiente' | Estado del ciclo de vida: `Pendiente` / `En Proceso` / `Terminado` |

---

## Stack Tecnológico

| Componente | Tecnología | Versión |
|------------|-----------|---------|
| Lenguaje de backend | Python | 3.x |
| Framework web | Flask | ≥ 3.0.0 |
| Motor de plantillas | Jinja2 | (incluido en Flask) |
| Base de datos | SQLite 3 | (stdlib Python) |
| Estilos e interfaz | Bootstrap 5 | 5.3.2 (CDN) |
| Frontend markup | HTML5 | — |

---

## Estructura del Proyecto

```
Desafio1-Parte2/
├── app.py                  # Backend completo: rutas, lógica y acceso a datos
├── requirements.txt        # Dependencias Python del proyecto
├── empresa.db              # Base de datos SQLite (generada en tiempo de ejecución)
└── templates/
    ├── base.html           # Plantilla base con Navbar Bootstrap 5
    ├── clientes.html       # Vista: gestión de clientes
    └── solicitudes.html    # Vista: gestión de solicitudes de servicio
```

> **Nota:** `empresa.db` se genera automáticamente al ejecutar `app.py` por primera vez. No se incluye en el repositorio (ver `.gitignore`).

---

## Rutas HTTP Implementadas

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Redirige a `/clientes` |
| GET | `/clientes` | Muestra formulario + listado de clientes |
| POST | `/clientes` | Registra un nuevo cliente en la base de datos |
| GET | `/solicitudes` | Muestra formulario + listado de solicitudes |
| POST | `/solicitudes` | Crea una nueva solicitud de servicio |
| POST | `/solicitudes/actualizar-estado` | Actualiza el estado de una solicitud existente |

---

## Instalación y Ejecución

### Prerequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/JONHREYES95/Desafio1-Parte2.git
cd Desafio1-Parte2

# 2. (Opcional) Crear y activar entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python app.py
```

La aplicación estará disponible en: **http://127.0.0.1:5000**

> Al iniciar, `app.py` crea automáticamente `empresa.db` y las tablas requeridas si no existen.

---

## Funcionalidades del Prototipo

- **Registro de clientes:** formulario con validación HTML5 (campo nombre requerido).
- **Listado de clientes:** tabla dinámica renderizada desde la base de datos vía Jinja2.
- **Creación de solicitudes:** selección dinámica de cliente y servicio desde registros de la BD.
- **Listado de solicitudes:** tabla con JOIN entre `solicitudes`, `clientes` y `servicios`.
- **Actualización de estado en línea:** `<select>` con envío automático (`onchange`) para cambiar el estado de `Pendiente` → `En Proceso` → `Terminado` sin recargar manualmente la página.

---

## Consideraciones Técnicas

- **Sin ORM:** se utiliza `sqlite3` de la librería estándar de Python para mantener el prototipo ligero y sin dependencias adicionales.
- **Sin blueprints:** toda la lógica reside en `app.py` para simplificar la estructura del prototipo. En un sistema productivo se recomienda modularizar con blueprints o una arquitectura basada en capas de servicios.
- **Sin archivos estáticos locales:** Bootstrap 5 se consume desde CDN para evitar gestión de assets en este prototipo.
- **Modo debug:** activado para facilitar el desarrollo. En un entorno de producción debe desactivarse y usarse un servidor WSGI como Gunicorn.
- **Base de datos local:** SQLite es adecuado para prototipos y aplicaciones de bajo tráfico. Para escalar a producción se recomienda migrar a PostgreSQL o MySQL con un ORM como SQLAlchemy.
