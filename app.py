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

# 1. Configuración inicial (ÚNICA VEZ)
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon="🔬", layout="wide")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# 2. Función de validación (El Guardián)
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

# 3. Función ejecutar_sivec (DEBES PEGAR TU LÓGICA AQUÍ)
def ejecutar_sivec(termino, pregunta):
    # Aquí va tu código original de OpenAlex + Gemini + Reportlab
    st.write("🔍 Escaneando literatura...")
    # ... tu código aquí ...
    st.success("✅ Análisis finalizado")

# 4. Interfaz Principal
st.title("🔬 SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.caption("Propiedad de Rubio Intelligence Systems.")
st.markdown("---")

st.sidebar.header("⚙️ Panel de Control")
try:
    st.sidebar.image("logo_rubio_is.png", width=250)
except: pass

rama_cientifica = st.sidebar.selectbox("Rama del Conocimiento:", [
    "🧬 Ciencias Médicas y de la Salud", "🌱 Biología, Agrobiociencias y Química",
    "🔋 Ingeniería, Tecnología y Nanomateriales", "🤖 Inteligencia Artificial y Computación Cuántica",
    "🌍 Ciencias de la Tierra, Astrofísica y Medio Ambiente", "📊 Matemáticas, Física y Ciencias Exactas",
    "⚖️ Ciencias Sociales, Economía y Derecho", "🎨 Humanidades, Filosofía y Estudios de Comportamiento",
    "✨ Personalizada / Otra Rama Científica"
])

max_papers = st.sidebar.slider("Lote de Documentos Analíticos:", 1, 3, 2)

# --- ENTRADAS ---
user_email = st.text_input("Correo electrónico registrado:")
termino_busqueda = st.text_input("Palabras clave:", placeholder="Ej. Autonomous weapons laws")
pregunta_usuario = st.text_area("Pregunta de investigación:", placeholder="Ej. ¿Qué vacíos legales existen?")

# 5. Lógica del Botón Único
if st.button("🚀 Lanzar Análisis de Vanguardia"):
    if not user_email:
        st.warning("⚠️ Debes ingresar tu correo electrónico.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning("⚠️ Completa todos los campos.")
    else:
        # Aquí el guardián actúa
        if validar_usuario_y_cuota(user_email):
            with st.status("🛸 Procesando...", expanded=True) as status:
                ejecutar_sivec(termino_busqueda, pregunta_usuario)
                status.update(label="✅ Análisis finalizado", state="complete")
        else:
            st.error("⚠️ **Congestión en Repositorios**: Límite de consultas diarias alcanzado. Intenta mañana.")
