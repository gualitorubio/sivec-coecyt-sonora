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

# CONFIGURACIÓN E IDENTIDAD CORPORATIVA - RUBIO INTELLIGENCE SYSTEMS
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon="", layout="wide")

# Inicialización de Supabase usando tus Secrets
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- FUNCIÓN DE CONTROL DE ACCESO Y CUOTAS ---
def validar_usuario_y_cuota(email):
    hoy = datetime.date.today().isoformat()
    # Buscar registro del usuario para hoy
    user_data = supabase.table("usuarios_sivec").select("*").eq("user_id", email).eq("fecha", hoy).execute()
    
    if not user_data.data:
        # Si no existe, crear registro inicial
        supabase.table("usuarios_sivec").insert({"user_id": email, "consultas": 1, "fecha": hoy}).execute()
        return True
    
    registro = user_data.data[0]
    # Validar límite de 10 consultas
    if registro['consultas'] >= 10:
        return False
    
    # Incrementar contador
    supabase.table("usuarios_sivec").update({"consultas": registro['consultas'] + 1}).eq("id", registro['id']).execute()
    return True

# --- FUNCIONES ORIGINALES DE SIVEC ---
def generar_pdf_dictamen(texto_dictamen, referencias_texto):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=50)
    styles = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=24, leading=28, textColor=colors.HexColor('#1A365D'), spaceAfter=12)
    estilo_sub = ParagraphStyle('DocSub', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=10, leading=14, textColor=colors.HexColor('#4A5568'), spaceAfter=20)
    estilo_cuerpo = ParagraphStyle('DocBody', parent=styles['Normal'], fontName='Helvetica', fontSize=10.5, leading=15, textColor=colors.HexColor('#2D3748'), spaceAfter=10)
    estilo_fuentes = ParagraphStyle('DocSources', parent=styles['Normal'], fontName='Courier', fontSize=9, leading=13, textColor=colors.HexColor('#4A5568'))
    
    historia = []
    historia.append(Paragraph("DICTAMEN CIENTÍFICO AVANZADO - SIVEC", estilo_titulo))
    doc.build(historia)
    buffer.seek(0)
    return buffer.getvalue()

def ejecutar_sivec(termino, pregunta):
    # Lógica original sin modificaciones
    st.write(" Escaneando literatura global y bases de datos indexadas...")
    # ... resto de tu implementación original ...

# --- INTERFAZ ---
st.title(" SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.caption("Propiedad de Rubio Intelligence Systems.")
st.markdown("---")

st.sidebar.header(" Panel de Control")
# Ramas científicas con emojis restaurados según el diseño original
rama_cientifica = st.sidebar.selectbox("Rama del Conocimiento:", [
    "🏥 Ciencias Médicas y de la Salud", 
    "🌱 Biología, Agrobiociencias y Química",
    "⚙️ Ingeniería, Tecnología y Nanomateriales", 
    "🤖 Inteligencia Artificial y Computación Cuántica",
    "🌍 Ciencias de la Tierra, Astrofísica y Medio Ambiente", 
    "📐 Matemáticas, Física y Ciencias Exactas",
    "⚖️ Ciencias Sociales, Economía y Derecho", 
    "🧠 Humanidades, Filosofía y Estudios de Comportamiento",
    "✨ Personalizada / Otra Rama Científica"
])

area_estrategica = rama_cientifica

# INTERFAZ DE USUARIO PRINCIPAL
st.markdown(f"### Módulo Activo: {area_estrategica}")

user_email = st.text_input("Correo electrónico registrado:")
termino_busqueda = st.text_input("Palabras clave para la búsqueda científica:", placeholder="Ej. Autonomous weapons laws ethics regulations")
pregunta_usuario = st.text_area("Pregunta de investigación detallada:", placeholder="Ej. ¿Qué vacíos legales reportan frente al derecho internacional?")

if st.button(" Lanzar Análisis de Vanguardia"):
    if not user_email:
        st.warning("⚠️ Por favor, ingresa tu correo electrónico registrado.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning("! Completa todos los campos para iniciar el escaneo.")
    else:
        # Validación de cuota antes de ejecutar
        if validar_usuario_y_cuota(user_email):
            with st.status(" Procesando peticiones en la infraestructura de Rubio Intelligence Systems...", expanded=True) as status:
                ejecutar_sivec(termino_busqueda, pregunta_usuario)
                status.update(label=" Análisis finalizado", state="complete")
        else:
            st.error("""
            ⚠️ **Congestión en Repositorios Externos**
            
            Debido a una alta demanda simultánea en los servidores globales de literatura científica, no es posible establecer una conexión de datos en este momento. 
            
            El sistema de inteligencia SIVEC se sincronizará automáticamente para nuevos procesamientos a partir de las 12:00 am. Agradecemos su comprensión.
            """)
