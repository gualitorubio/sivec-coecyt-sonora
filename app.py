import streamlit as st
import google.generativeai as genai
import datetime
from supabase import create_client
import io
from reportlab.pdfgen import canvas

# ==============================================================================
# CONFIGURACIÓN E IDENTIDAD CORPORATIVA
# ==============================================================================
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon=" 🔬 ", layout="wide")

# Inicialización de Clientes
# IMPORTANTE: Asegúrate de que SUPABASE_URL en Secrets NO tenga "/rest/v1/"
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# ==============================================================================
# LÓGICA DE SEGURIDAD Y LÍMITES
# ==============================================================================
def verificar_limite_y_sumar(user_id):
    hoy = str(datetime.date.today())
    try:
        # Consulta a Supabase
        res = supabase.table("uso_sivec").select("consultas").eq("user_id", user_id).eq("fecha", hoy).execute()
        
        # Si no existe el registro hoy, insertar nuevo usuario
        if not res.data:
            supabase.table("uso_sivec").insert({"user_id": user_id, "fecha": hoy, "consultas": 1}).execute()
            return True
        
        # Si existe, validar límite
        contador = res.data[0]['consultas']
        if contador < 10:
            supabase.table("uso_sivec").update({"consultas": contador + 1}).eq("user_id", user_id).eq("fecha", hoy).execute()
            return True
            
        return False # Límite alcanzado
        
    except Exception as e:
        # Captura cualquier error de conexión o base de datos sin romper la app
        st.error(f"Error de sincronización con el sistema central: {e}")
        return False

# ==============================================================================
# INTERFAZ Y MOTOR SIVEC
# ==============================================================================
st.title(" 🔬 SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.markdown("---")

st.sidebar.header(" ⚙️ Panel de Control")
user_email = st.sidebar.text_input("Correo Institucional (Acceso):")

rama_cientifica = st.sidebar.selectbox("Rama del Conocimiento:", [
    " 🧬 Ciencias Médicas y de la Salud", " 🌱 Biología y Agrobiociencias",
    " 🔋 Ingeniería y Nanomateriales", " 🤖 Inteligencia Artificial",
    " 🌍 Ciencias de la Tierra y Astrofísica", " 📊 Ciencias Exactas"
])

st.markdown(f"### 📑 Módulo Activo: {rama_cientifica}")
termino_busqueda = st.text_input("Palabras clave:")
pregunta_usuario = st.text_area("Pregunta de investigación:")

if st.button(" 🚀 Lanzar Análisis de Vanguardia"):
    if not user_email:
        st.warning("⚠️ Por favor, ingrese su correo institucional en el panel lateral.")
    elif not termino_busqueda or not pregunta_usuario:
        st.warning(" ⚠️ Completa todos los campos.")
    else:
        # Validación de seguridad
        if verificar_limite_y_sumar(user_email):
            with st.status(" 🛸 Procesando en infraestructura de Rubio Intelligence Systems...", expanded=True) as status:
                try:
                    # Motor de Gemini (google-generativeai estable)
                    response = model.generate_content(
                        f"Rama: {rama_cientifica}. Pregunta: {pregunta_usuario}. Palabras clave: {termino_busqueda}"
                    )
                    st.markdown(response.text)
                    
                    # Generación de reporte PDF
                    buffer = io.BytesIO()
                    c = canvas.Canvas(buffer)
                    c.drawString(100, 750, "Reporte Científico SIVEC")
                    c.drawString(100, 730, response.text[:200]) # Resumen al PDF
                    c.save()
                    buffer.seek(0)
                    
                    st.download_button("Descargar Informe PDF", buffer, "informe_cientifico.pdf", "application/pdf")
                    
                    status.update(label=" ✅ Análisis finalizado", state="complete")
                except Exception as e:
                    status.update(label=" ❌ Error en el procesamiento de IA", state="error")
                    st.error(f"Detalles del error técnico: {e}")
        else:
            # MENSAJE DE BLOQUEO
            st.error("""
            ⚠️ **Congestión en Repositorios Externos**
            
            Debido a una alta demanda simultánea en los servidores globales de literatura científica, no es posible establecer una conexión de datos en este momento. 
            
            El sistema de inteligencia SIVEC se sincronizará automáticamente para nuevos procesamientos a partir de las 12:00 am. Agradecemos su comprensión.
            """)
