import streamlit as st
import google.generativeai as genai
import datetime
from supabase import create_client
import io
from reportlab.pdfgen import canvas

# Configuración
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", layout="wide")

# Inicialización
try:
    # Configuración de la librería clásica
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error(f"Error de inicialización: {e}")
    st.stop()

def verificar_limite_y_sumar(user_id):
    hoy = str(datetime.date.today())
    try:
        res = supabase.table("uso_sivec").select("consultas").eq("user_id", user_id).eq("fecha", hoy).execute()
        if not res.data:
            supabase.table("uso_sivec").insert({"user_id": user_id, "fecha": hoy, "consultas": 1}).execute()
            return True
        if res.data[0]['consultas'] < 10:
            supabase.table("uso_sivec").update({"consultas": res.data[0]['consultas'] + 1}).eq("user_id", user_id).eq("fecha", hoy).execute()
            return True
        return False
    except Exception as e:
        st.error(f"Error BD: {e}")
        return False

# Interfaz
st.title(" 🔬 SIVEC")
user_email = st.sidebar.text_input("Correo Institucional (Acceso):")
rama_cientifica = st.sidebar.selectbox("Rama del Conocimiento:", ["Ciencias Médicas", "Física", "IA"])
pregunta_usuario = st.text_area("Pregunta de investigación:")

if st.button(" 🚀 Lanzar Análisis de Vanguardia"):
    if verificar_limite_y_sumar(user_email):
        with st.status("Procesando...", expanded=True) as status:
            try:
                # Llamada al modelo con la librería clásica
                response = model.generate_content(f"Rama: {rama_cientifica}. Pregunta: {pregunta_usuario}")
                st.markdown(response.text)
                
                # Generación de PDF
                buffer = io.BytesIO()
                c = canvas.Canvas(buffer)
                c.drawString(100, 750, "Reporte SIVEC")
                c.drawString(100, 730, response.text[:200])
                c.save()
                buffer.seek(0)
                
                st.download_button("Descargar PDF", buffer, "informe.pdf", "application/pdf")
                status.update(label=" ✅ Finalizado", state="complete")
            except Exception as e:
                status.update(label=" ❌ Error de IA", state="error")
                st.error(f"Detalle: {str(e)}")
    else:
        st.error("Límite diario alcanzado o error de autenticación.")
