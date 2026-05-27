import streamlit as st
import requests
from google import genai
import io
import os
import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- LÓGICA DE CONTROL (Persistente en CSV) ---
def verificar_acceso(email):
    if not os.path.exists("usuarios_autorizados.txt"):
        with open("usuarios_autorizados.txt", "w") as f: f.write("admin@rubio.com")
    with open("usuarios_autorizados.txt", "r") as f:
        autorizados = [line.strip() for line in f.readlines()]
    if email not in autorizados: return False, "No autorizado"

    archivo = "cuotas.csv"
    hoy = datetime.date.today().isoformat()
    if not os.path.exists(archivo): pd.DataFrame(columns=["email", "fecha", "consultas"]).to_csv(archivo, index=False)
    df = pd.read_csv(archivo)
    mask = (df["email"] == email) & (df["fecha"] == hoy)
    
    if mask.any() and df.loc[mask, "consultas"].values[0] >= 10: return False, "Límite"
    
    if mask.any(): df.loc[mask, "consultas"] += 1
    else: df = pd.concat([df, pd.DataFrame({"email": [email], "fecha": [hoy], "consultas": [1]})], ignore_index=True)
    df.to_csv(archivo, index=False)
    return True, "Ok"

# --- CONFIGURACIÓN E IDENTIDAD (Igual a tu PDF) ---
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon="🔬", layout="wide")
st.title("🔬 SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.caption("Propiedad de Rubio Intelligence Systems.")
st.markdown("---")
st.sidebar.header("⚙️ Panel de Control")

# --- ENTRADAS DE USUARIO ---
user_email = st.text_input("Correo electrónico registrado:")
rama_cientifica = st.sidebar.selectbox("Rama del Conocimiento:", ["Ciencias Médicas y de la Salud", "IA", "Otras"])
max_papers = st.sidebar.slider("Lote de Documentos:", 1, 3, 2)
termino_busqueda = st.text_input("Palabras clave:")
pregunta_usuario = st.text_area("Pregunta de investigación:")

# --- BOTÓN DE EJECUCIÓN (Lógica integrada) ---
if st.button("🚀 Lanzar Análisis de Vanguardia"):
    if not user_email or not termino_busqueda or not pregunta_usuario:
        st.warning("⚠️ Completa todos los campos.")
    else:
        acceso, estado = verificar_acceso(user_email)
        if estado == "Límite":
            st.error("""
            ⚠️ **Congestión en Repositorios Externos**
            
            Debido a una alta demanda simultánea en los servidores globales de literatura científica, no es posible establecer una conexión de datos en este momento. 
            
            El sistema de inteligencia SIVEC se sincronizará automáticamente para nuevos procesamientos a partir de las 12:00 am. Agradecemos su comprensión.""")
        elif not acceso:
            st.error("Usuario no autorizado.")
        else:
            with st.status("🛸 Procesando peticiones en la infraestructura de Rubio Intelligence Systems...", expanded=True) as status:
                # --- AQUÍ VA TU LÓGICA ORIGINAL ---
                st.write("Conectando con repositorios...")
                # PEGA AQUÍ TODO TU BLOQUE DE CÓDIGO ORIGINAL (requests.get, Gemini, Reportlab...)
                # ...
                status.update(label="✅ Análisis finalizado", state="complete")
