import os
import requests
import json
import base64
import time
import streamlit as st
import zipfile
from io import BytesIO

# Directorio temporal de archivos
DIRECTORIO = "archivos_descargados"
os.makedirs(DIRECTORIO, exist_ok=True)

# Descargar archivos PDF desde la URL base
def descargar_pdfs(file_names):
    BASE_URL = "http://odc.portalweb.priceshoes.com/fsw/pdgn/repo/getPtPDF?encodedData="
    archivos_descargados = []
    for file_name in file_names:
        data = {
            "nombreArchivo": f"{file_name}.pdf",
            "fileType": 1,
            "attachment": True
        }
        encoded_data = base64.b64encode(json.dumps(data).encode()).decode()
        pdf_url = f"{BASE_URL}{encoded_data}"
        response = requests.get(pdf_url)
        if response.status_code == 200:
            file_path = os.path.join(DIRECTORIO, f"{file_name}.pdf")
            with open(file_path, "wb") as file:
                file.write(response.content)
            if os.path.getsize(file_path) <= 1024:
                st.error(f"❌ No se pudo descargar: {file_name} (verifica el nombre)")
                os.remove(file_path)
            else:
                st.success(f"✅ PDF descargado: {file_name}.pdf")
                archivos_descargados.append(file_path)
        else:
            st.error(f"❌ Error al descargar {file_name}: {response.status_code}")
        time.sleep(1.5)
    return archivos_descargados

# Crear archivo ZIP con los PDFs
def crear_zip(archivos):
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipf:
        for archivo in archivos:
            nombre = os.path.basename(archivo)
            zipf.write(archivo, arcname=nombre)
    buffer.seek(0)
    return buffer

# Interfaz Streamlit
st.title("📥 Descarga MASIVA de Planes de Trabajo")

nombres_input = st.text_area("🔤 Ingresa los nombres de los archivos (uno por línea):")

if st.button("⬇️ Descargar todos"):
    if nombres_input.strip():
        nombres_lista = [line.strip() for line in nombres_input.strip().splitlines() if line.strip()]
        archivos = descargar_pdfs(nombres_lista)

        if archivos:
            zip_buffer = crear_zip(archivos)
            st.download_button(
                label="📦 Descargar ZIP con todos los PDFs",
                data=zip_buffer,
                file_name="planes_trabajo.zip",
                mime="application/zip"
            )
        else:
            st.warning("⚠️ No hay archivos válidos para comprimir.")
    else:
        st.warning("⚠️ Por favor, ingresa al menos un nombre de archivo.")
