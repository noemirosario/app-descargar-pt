import os
import requests
import json
import base64
import time
import streamlit as st

# Directorio de descargas (se puede usar temporalmente en Render)
DIRECTORIO = "archivos_descargados"
os.makedirs(DIRECTORIO, exist_ok=True)

# Renombrar archivos PDF en el directorio
def renombrar_archivos():
    archivos = os.listdir(DIRECTORIO)
    nuevos_nombres = []
    for archivo in archivos:
        if archivo.endswith('.pdf'):
            partes = archivo.split('_')
            if len(partes) >= 2:
                nuevo_nombre = f'{partes[0]}_{partes[1]}.pdf'
                ruta_vieja = os.path.join(DIRECTORIO, archivo)
                ruta_nueva = os.path.join(DIRECTORIO, nuevo_nombre)
                os.rename(ruta_vieja, ruta_nueva)
                st.success(f"Renombrado: {archivo} -> {nuevo_nombre}")
                nuevos_nombres.append(nuevo_nombre)
            else:
                nuevos_nombres.append(archivo)
    st.info("✅ Renombrado completo.")
    return nuevos_nombres

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
            # Verificar tamaño del archivo
            if os.path.getsize(file_path) <= 1024:  # 1 KB o menos
                st.error(f"❌ No pudimos descargar el plan: {file_name} (verifica el nombre del archivo)")
                os.remove(file_path)  # Opcional: borrar archivo inválido
            else:
                st.success(f"✅ PDF descargado: {file_name}.pdf")
                archivos_descargados.append(file_path)
        else:
            st.error(f"❌ Error al descargar {file_name}: {response.status_code}")
        time.sleep(1.5)
    return archivos_descargados

# Interfaz Streamlit
st.title("📥 Descarga masiva de Planes De Trabajo")

nombres_input = st.text_area("Ingresa los nombres de los archivos (uno por línea):")
if st.button("Descargar PDFs"):
    if nombres_input.strip():
        nombres_lista = [line.strip() for line in nombres_input.strip().splitlines() if line.strip()]
        archivos_descargados = descargar_pdfs(nombres_lista)
        nuevos_nombres = renombrar_archivos()

        # Mostrar botones para descargar los PDFs desde la app
        st.header("Descarga tus archivos PDF:")
        for archivo in nuevos_nombres:
            file_path = os.path.join(DIRECTORIO, archivo)
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    st.download_button(
                        label=f"Descargar {archivo}",
                        data=f,
                        file_name=archivo,
                        mime="application/pdf"
                    )
    else:
        st.warning("⚠️ Por favor, ingresa al menos un nombre de archivo.")
