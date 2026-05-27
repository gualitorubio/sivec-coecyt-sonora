import streamlit as st
import requests
from google import genai
import io
import datetime
from supabase import create_client

# Configuración y Clientes
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon="🔬", layout="wide")
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- Lógica de Supabase (Reforzada y silenciosa) ---
def registrar_consulta(user_id):
    try:
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
    except:
        return True # Si falla Supabase, el SIVEC sigue funcionando

# --- INTERFAZ (Igual que tu original) ---
st.title("🔬 SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.sidebar.header("⚙️ Panel de Control")
user_email = st.sidebar.text_input("Correo para registro de cuota:")
rama = st.sidebar.selectbox("Rama del Conocimiento:", ["Ciencias Médicas y de la Salud", "Biología, Agrobiociencias y Química", "Ingeniería, Tecnología y Nanomateriales", "Inteligencia Artificial y Computación Cuántica", "Ciencias de la Tierra, Astrofísica y Medio Ambiente", "Matemáticas, Física y Ciencias Exactas", "Ciencias Sociales, Economía y Derecho", "Humanidades, Filosofía y Estudios de Comportamiento", "Personalizada / Otra Rama Científica"])
termino = st.text_input("Palabras clave:")
pregunta = st.text_area("Pregunta de investigación:")

if st.button("🚀 Lanzar Análisis de Vanguardia"):
    if not user_email or not termino or not pregunta:
        st.warning("⚠️ Completa todos los campos.")
    elif not registrar_consulta(user_email):
        st.error("⚠️ Límite de 10 consultas alcanzado por hoy.")
    else:
        with st.status("🛸 Procesando peticiones...", expanded=True):
            # Aquí va tu motor de búsqueda y Gemini tal cual funciona en tu SIVEC original
            st.write("Conectando con repositorios...")
            # ... (Copia aquí tu lógica de ejecutar_sivec del PDF) ...
            st.success("Análisis finalizado")
