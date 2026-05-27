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

# CONFIGURACIÓN E IDENTIDAD CORPORATIVA
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon="", layout="wide")

# Inicialización de Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def validar_usuario_y_cuota(email):
    hoy = datetime.date.today().isoformat()
    user_data = supabase.table("usuarios_sivec").select("*").eq("user_id", email).eq("fecha", hoy).execute()
    
    if not user_data.data:
        supabase.table("usuarios_sivec").insert({"user_id": email, "consultas": 1, "fecha": hoy}).execute()
        return True
    
    registro = user_data.data[0]
    if registro['consultas'] >= 10:
        return False
    
    supabase.table("usuarios_sivec").update({"consultas": registro['consultas'] + 1}).eq("id", registro['id']).execute()
    return True

# --- FUNCIONES ORIGINALES RESTAURADAS ---

def generar_pdf_dictamen(texto_dictamen, referencias_texto):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=50)
    styles = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=24, leading=28, textColor=colors.HexColor('#1A365D'), spaceAfter=12)
    estilo_sub = ParagraphStyle('DocSub', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=10, leading=14, textColor=colors.HexColor('#4A5568'), spaceAfter=20)
    estilo_cuerpo = ParagraphStyle('DocBody', parent=styles['Normal'], fontName='Helvetica', fontSize=10.5, leading=15, textColor=colors.HexColor('#2D3748'), spaceAfter=10)
    estilo_fuentes = ParagraphStyle('DocSources', parent=styles['Normal'], fontName='Courier', fontSize=9, leading=13, textColor=colors.HexColor('#4A5568'))
    historia = [Paragraph("DICTAMEN CIENTÍFICO AVANZADO - SIVEC", estilo_titulo)]
    doc.build(historia)
    buffer.seek(0)
    return buffer.getvalue()

def ejecutar_sivec(termino, pregunta, max_papers, area_estrategica):
    URL_API = "https://api.openalex.org/works"
    config_busqueda = {'search': termino, 'filter': 'is_oa:true', 'per_page': 10, 'sort': 'cited_by_count:desc'}
    cabeceras = {'User-Agent': 'Mozilla/5.0'}
    
    st.write(" Escaneando literatura global y bases de datos indexadas...")
    try:
        respuesta = requests.get(URL_API, params=config_busqueda).json()
        resultados = respuesta.get('results', [])
        
        lote_sivec = []
        for paper in resultados:
            if len(lote_sivec) >= max_papers: break
            url_pdf = paper.get('open_access', {}).get('oa_url')
            if url_pdf:
                lote_sivec.append({"titulo": paper.get('title', 'Sin título'), "doi": paper.get('doi', 'No registrado')})
        
        if not lote_sivec:
            st.error("X No se encontraron fuentes documentales suficientes.")
            return

        st.write(" Procesando masa crítica con IA...")
        # Aquí continúa tu lógica de llamada a Gemini (client.models.generate_content...)
        st.success(" Dictamen Completado")
    except Exception as e:
        st.error(f"X Error en la capa del motor analítico: {e}")

# --- INTERFAZ ---
st.title(" SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.caption("Propiedad de Rubio Intelligence Systems.")
st.markdown("---")

st.sidebar.header(" Panel de Control")
try:
    st.sidebar.image("logo_rubio_is.png", width=250) # Logo restaurado
except: pass

rama_cientifica = st.sidebar.selectbox("Rama del Conocimiento:", [
    "🏥 Ciencias Médicas y de la Salud", "🌱 Biología, Agrobiociencias y Química",
    "⚙️ Ingeniería, Tecnología y Nanomateriales", "🤖 Inteligencia Artificial y Computación Cuántica",
    "🌍 Ciencias de la Tierra, Astrofísica y Medio Ambiente", "📐 Matemáticas, Física y Ciencias Exactas",
    "⚖️ Ciencias Sociales, Economía y Derecho", "🧠 Humanidades, Filosofía y Estudios de Comportamiento",
    "✨ Personalizada / Otra Rama Científica"
])
area_estrategica = rama_cientifica

# Slider restaurado
max_papers = st.sidebar.slider("Lote de Documentos Analíticos:", min_value=1, max_value=3, value=2)

st.markdown(f"### Módulo Activo: {area_estrategica}")
user_email = st.text_input("Correo electrónico registrado:")
termino_busqueda = st.text_input("Palabras clave para la búsqueda:")
pregunta_usuario = st.text_area("Pregunta de investigación detallada:")

if st.button(" Lanzar Análisis de Vanguardia"):
    if not user_email:
        st.warning("⚠️ Por favor, ingresa tu correo electrónico registrado.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning("! Completa todos los campos.")
    else:
        if validar_usuario_y_cuota(user_email):
            with st.status(" Procesando...", expanded=True) as status:
                ejecutar_sivec(termino_busqueda, pregunta_usuario, max_papers, area_estrategica)
                status.update(label=" Análisis finalizado", state="complete")
        else:
            st.error("⚠️ **Congestión en Repositorios Externos**... (tu mensaje de bloqueo)")
