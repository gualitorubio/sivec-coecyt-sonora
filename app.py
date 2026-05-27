import streamlit as st
import requests
from google import genai
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from supabase import create_client
from datetime import datetime

# ==============================================================================
# CONFIGURACIÓN E IDENTIDAD CORPORATIVA - RUBIO INTELLIGENCE SYSTEMS
# ==============================================================================
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon=" 🔬 ", layout="wide")

# --- LÓGICA SUPABASE PARA CONTROL DE CUOTAS ---
# Nota: Asegúrate de tener los secretos configurados en Streamlit
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def validar_cuota(email):
    hoy = datetime.now().strftime("%Y-%m-%d")
    res = supabase.table("usuarios_sivec").select("*").eq("email", email).execute()
    
    if not res.data:
        supabase.table("usuarios_sivec").insert({"email": email, "peticiones_hoy": 1, "ultima_fecha": hoy}).execute()
        return True
    
    usuario = res.data[0]
    if usuario['ultima_fecha'] != hoy:
        supabase.table("usuarios_sivec").update({"peticiones_hoy": 1, "ultima_fecha": hoy}).eq("email", email).execute()
        return True
    
    if usuario['peticiones_hoy'] < 10:
        supabase.table("usuarios_sivec").update({"peticiones_hoy": usuario['peticiones_hoy'] + 1}).eq("email", email).execute()
        return True
    return False

# --- CÓDIGO ORIGINAL SIN MODIFICAR (Funciones principales) ---
# [Aquí insertarías todas tus funciones: generar_pdf_dictamen, ejecutar_sivec, etc.]

# ==============================================================================
# INTERFAZ DE USUARIO PRINCIPAL (Estructura respetada)
# ==============================================================================
# [Insertar aquí tu código original del sidebar, logo, etc.]
# ... asegúrate de que 'area_estrategica' se defina aquí ...

# AHORA SÍ, colocamos el título usando la variable ya definida:
st.markdown(f"###  📑  Módulo Activo: {area_estrategica}")

# Campo para identificar al usuario
email_usuario = st.sidebar.text_input("Correo Institucional COECyT:")

termino_busqueda = st.text_input("Palabras clave para la búsqueda científica:", placeholder="Ej. Autonomous weapons laws ethics regulations")
pregunta_usuario = st.text_area("Pregunta de investigación detallada:", placeholder="Ej. ¿Qué vacíos legales reportan frente al derecho internacional?")

if st.button(" 🚀  Lanzar Análisis de Vanguardia"):
    if not email_usuario:
        st.warning("⚠️ Por favor ingresa tu correo institucional para continuar.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning(" ⚠️  Completa ambos campos para iniciar el escaneo.")
    else:
        # Validación de cuota antes de ejecutar
        if validar_cuota(email_usuario):
            with st.status(" 🛸  Procesando peticiones en la infraestructura de Rubio Intelligence Systems...", expanded=True) as status:
                ejecutar_sivec(termino_busqueda, pregunta_usuario)
                status.update(label=" ✅  Análisis finalizado", state="complete")
        else:
            st.error("""
            ⚠️ **Congestión en Repositorios Externos**
            
            Debido a una alta demanda simultánea en los servidores globales de literatura científica, no es posible establecer una conexión de datos en este momento. 
            
            El sistema de inteligencia SIVEC se sincronizará automáticamente para nuevos procesamientos a partir de las 12:00 am. Agradecemos su comprensión.
            """)
