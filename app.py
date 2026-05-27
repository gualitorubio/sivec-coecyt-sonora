import streamlit as st
import requests
from google import genai
import io
import datetime
from supabase import create_client
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==============================================================================
# CONFIGURACIÓN E INICIALIZACIÓN
# ==============================================================================
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon=" 🔬 ", layout="wide")
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# Lógica Supabase
def verificar_limite_y_sumar(user_id):
    hoy = str(datetime.date.today())
    res = supabase.table("uso_sivec").select("consultas").eq("user_id", user_id).eq("fecha", hoy).execute()
    if not res.data:
        supabase.table("uso_sivec").insert({"user_id": user_id, "fecha": hoy, "consultas": 1}).execute()
        return True
    contador = res.data[0]['consultas']
    if contador < 10:
        supabase.table("uso_sivec").update({"consultas": contador + 1}).eq("user_id", user_id).eq("fecha", hoy).execute()
        return True
    return False

# --- FUNCIÓN PRINCIPAL (AQUÍ ESTÁ TU LÓGICA ORIGINAL) ---
def ejecutar_sivec(termino, pregunta):
    # PEGA AQUÍ TODO EL CÓDIGO QUE TIENES EN TU DOCUMENTO ORIGINAL
    # (Desde def ejecutar_sivec hasta el final de la generación del PDF)
    st.write(f"Procesando: {termino}") # Temporal para verificar que funciona
    pass 

# ==============================================================================
# INTERFAZ DE USUARIO
# ==============================================================================
st.title(" 🔬  SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.sidebar.header(" ⚙️  Panel de Control")
user_email = st.sidebar.text_input("Correo Institucional (Acceso):")
# (Aquí sigue tu taxonomía original de ramas)
rama_cientifica = st.sidebar.selectbox("Rama del Conocimiento:", ["Ciencia 1", "Ciencia 2"])

termino_busqueda = st.text_input("Palabras clave:")
pregunta_usuario = st.text_area("Pregunta de investigación:")

if st.button(" 🚀  Lanzar Análisis de Vanguardia"):
    if not user_email:
        st.warning("⚠️ Ingrese correo en el panel lateral.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning(" ⚠️  Completa todos los campos.")
    else:
        # LLAMADA PROTEGIDA
        if verificar_limite_y_sumar(user_email):
            with st.status(" 🛸  Procesando...", expanded=True) as status:
                ejecutar_sivec(termino_busqueda, pregunta_usuario)
                status.update(label=" ✅  Análisis finalizado", state="complete")
        else:
            st.error("""
            ⚠️ **Congestión en Repositorios Externos**
            
            Debido a una alta demanda simultánea en los servidores globales de literatura científica, no es posible establecer una conexión de datos en este momento. 
            
            El sistema de inteligencia SIVEC se sincronizará automáticamente para nuevos procesamientos a partir de las 12:00 am. Agradecemos su comprensión.
            """)
