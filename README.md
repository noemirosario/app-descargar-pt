# 📥 PlanesDeTrabajo Downloader & Renamer






> **Automatiza la descarga y renombrado de archivos PDF de planes de trabajo**  


> con una interfaz sencilla en Streamlit. Perfecto para gestionar tus documentos sin complicaciones.

---



## 🚀 Características

- 📄 Descarga masiva de PDFs desde URLs generadas con datos codificados en base64  


- 🔄 Renombrado automático y ordenado de archivos descargados  


- ⚠️ Validación para detectar descargas incompletas o inválidas (archivos ≤ 1 KB)  


- 🎨 Interfaz interactiva y amigable con Streamlit para ingresar nombres y controlar la descarga  





---

## 🛠️ Instalación


1. Clona el repositorio:


2. Instala las dependencias:


   pip install -r requirements.txt


Si no tienes el archivo requirements.txt, instala manualmente:


  pip install streamlit requests





# ⚡ Uso

Ejecuta la aplicación con:


  streamlit run app.py


Luego abre tu navegador en http://localhost:8501 y sigue estos pasos:


  Ingresa los nombres de los archivos que deseas descargar, uno por línea.


  Presiona el botón "Descargar PDFs".


  Espera a que la app descargue y renombre automáticamente los archivos.


  Si algún archivo tiene tamaño ≤ 1 KB, recibirás una alerta indicando que no se pudo descargar correctamente.
