# Registro de Personas en Situación de Calle - SMT

Este es un proyecto CRUD (Crear, Leer, Actualizar, Eliminar) desarrollado con **Flask** y **SQLite** para gestionar un registro de personas en situación de calle. Incluye la posibilidad de agregar múltiples problemáticas por persona, registrar ubicación y contacto de emergencia.

## 🚀 Demo Online

Ya puedes ver el proyecto funcionando aquí:
👉 [https://crud-personas-en-sitacion-de-calle-smt.onrender.com](https://crud-personas-en-sitacion-de-calle-smt.onrender.com)

---

## ⚙️ Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes)

---

## 🧰 Instalación Local

1. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
```

2. Crea un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecuta la app localmente:
```bash
python app.py
```

5. Abre tu navegador en:
```
http://127.0.0.1:5000/
```

---

## 📁 Estructura del Proyecto
```
├── app.py                  # Lógica principal de Flask
├── registro.db             # Base de datos SQLite
├── templates/              # Vistas HTML (index, agregar, editar)
├── static/                 # Archivos CSS, JS (opcional)
├── requirements.txt        # Dependencias del proyecto
├── README.md
└── .gitignore
```

---

## ✅ Funcionalidades
- Listado de personas con sus datos básicos
- Registro de múltiples problemáticas por persona
- Registro de dirección y coordenadas geográficas
- Edición y eliminación de registros
- Visualización online

---

## 🛰️ Hosting en Render

Este proyecto está alojado en **Render.com**, un servicio gratuito para apps web. Utiliza `gunicorn` como servidor de producción.

**Start Command:**
```bash
gunicorn app:app
```

**Build Command:**
```bash
pip install -r requirements.txt
```

---

## 📬 Contribuciones
¡Bienvenido a contribuir! Crea un issue o haz un pull request si querés mejorar algo.

---

## 🧾 Licencia
Este proyecto está bajo la Licencia MIT.
