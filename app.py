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

# --- CÓDIGO ORIGINAL (Tu lógica de funciones) ---
# [Aquí mantienes tus funciones: generar_pdf_dictamen, ejecutar_sivec, etc.]

# ==============================================================================
# INTERFAZ DE USUARIO (Orden corregido)
# ==============================================================================
# 1. Definimos primero el Sidebar y la lógica que asigna 'area_estrategica'
st.sidebar.header(" ⚙️  Panel de Control")
rama_cientifica = st.sidebar.selectbox("Rama del Conocimiento:", [...]) # Tu lista original
if rama_cientifica == " ✨  Personalizada / Otra Rama Científica":
    rama_personalizada = st.sidebar.text_input("Especifica la disciplina:")
    area_estrategica = rama_personalizada if rama_personalizada else "Disciplina Personalizada"
else:
    area_estrategica = rama_cientifica

# 2. AHORA, tras definir la variable, podemos usarla
st.markdown(f"###  📑  Módulo Activo: {area_estrategica}")

# Campo para identificar al usuario
email_usuario = st.sidebar.text_input("Correo Institucional COECyT:")

termino_busqueda = st.text_input("Palabras clave para la búsqueda científica:")
pregunta_usuario = st.text_area("Pregunta de investigación detallada:")

if st.button(" 🚀  Lanzar Análisis de Vanguardia"):
    if not email_usuario:
        st.warning("⚠️ Por favor ingresa tu correo institucional.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning(" ⚠️  Completa todos los campos.")
    else:
        if validar_cuota(email_usuario):
            with st.status(" 🛸  Procesando...", expanded=True) as status:
                ejecutar_sivec(termino_busqueda, pregunta_usuario)
                status.update(label=" ✅  Análisis finalizado", state="complete")
        else:
            st.error("""
            ⚠️ **Congestión en Repositorios Externos**
            
            Debido a una alta demanda... (tu mensaje original)
            """)
