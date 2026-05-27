import streamlit as st
import requests
from google import genai
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==============================================================================
# CONFIGURACIÓN E IDENTIDAD CORPORATIVA - RUBIO INTELLIGENCE SYSTEMS
# ==============================================================================
st.set_page_config(page_title="SIVEC - Rubio Intelligence Systems", page_icon="🔬", layout="wide")

st.title("🔬 SIVEC")
st.subheader("Sistema de Inteligencia para la Vanguardia Experimental y Científica")
st.caption("Propiedad de Rubio Intelligence Systems.")
st.markdown("---")

st.sidebar.header("⚙️ Panel de Control")

try:
    st.sidebar.image("logo_rubio_is.png", width=250)
except Exception:
    pass

# Taxonomía Científica Universal
rama_cientifica = st.sidebar.selectbox(
    "Rama del Conocimiento:",
    [
        "🧬 Ciencias Médicas y de la Salud",
        "🌱 Biología, Agrobiociencias y Química",
        "🔋 Ingeniería, Tecnología y Nanomateriales",
        "🤖 Inteligencia Artificial y Computación Cuántica",
        "🌍 Ciencias de la Tierra, Astrofísica y Medio Ambiente",
        "📊 Matemáticas, Física y Ciencias Exactas",
        "⚖️ Ciencias Sociales, Economía y Derecho",
        "🎨 Humanidades, Filosofía y Estudios de Comportamiento",
        "✨ Personalizada / Otra Rama Científica"
    ]
)

if rama_cientifica == "✨ Personalizada / Otra Rama Científica":
    rama_personalizada = st.sidebar.text_input("Especifica la disciplina o subrama:", placeholder="Ej. Paleontología Marina")
    area_estrategica = rama_personalizada if rama_personalizada else "Disciplina Personalizada"
else:
    area_estrategica = rama_cientifica

# 🔒 OPTIMIZACIÓN DE TOKENS: Limitado estrictamente de 1 a 3 papers maximo
max_papers = st.sidebar.slider("Lote de Documentos Analíticos:", min_value=1, max_value=3, value=2)

# ==============================================================================
# FUNCIÓN COMPAÑERA: GENERADOR DE ENTREGABLES EN PDF
# ==============================================================================
def generar_pdf_dictamen(texto_dictamen, referencias_texto):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    
    # Estilos Personalizados del Reporte
    estilo_titulo = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=24, leading=28,
        textColor=colors.HexColor('#1A365D'), spaceAfter=12
    )
    estilo_sub = ParagraphStyle(
        'DocSub', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=10, leading=14,
        textColor=colors.HexColor('#4A5568'), spaceAfter=20
    )
    estilo_cuerpo = ParagraphStyle(
        'DocBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10.5, leading=15,
        textColor=colors.HexColor('#2D3748'), spaceAfter=10
    )
    estilo_fuentes = ParagraphStyle(
        'DocSources', parent=styles['Normal'],
        fontName='Courier', fontSize=9, leading=13,
        textColor=colors.HexColor('#4A5568')
    )
    estilo_pie = ParagraphStyle(
        'DocFooter', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10,
        alignment=1, textColor=colors.HexColor('#718096')
    )

    historia = []
    
    # Encabezado Institucional
    historia.append(Paragraph("DICTAMEN CIENTÍFICO AVANZADO - SIVEC", estilo_titulo))
    historia.append(Paragraph(f"Área de Especialidad: {area_estrategica}", estilo_sub))
    historia.append(Spacer(1, 10))
    
    # Procesar el cuerpo del dictamen línea por línea para Markdown básico
    lineas = texto_dictamen.split('\n')
    for linea in lineas:
        if not linea.strip():
            historia.append(Spacer(1, 6))
            continue
        
        # Limpieza básica de cabeceras Markdown
        texto_limpio = linea.replace('**', '').replace('###', '').replace('##', '').replace('#', '').strip()
        
        if linea.startswith('#'):
            historia.append(Paragraph(texto_limpio, ParagraphStyle('H', parent=estilo_cuerpo, fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=colors.HexColor('#2C5282'), spaceBefore=10)))
        elif linea.startswith('-') or linea.startswith('*'):
            texto_limpio = f"• {texto_limpio[1:].strip()}"
            historia.append(Paragraph(texto_limpio, estilo_cuerpo))
        else:
            historia.append(Paragraph(texto_limpio, estilo_cuerpo))
            
    historia.append(Spacer(1, 20))
    historia.append(Paragraph("📚 FUENTES DOCUMENTALES DE VALIDACIÓN", ParagraphStyle('H2', parent=estilo_cuerpo, fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#2C5282'))))
    historia.append(Spacer(1, 5))
    
    for ref in referencias_texto.split('\n'):
        if ref.strip():
            historia.append(Paragraph(ref.strip(), estilo_fuentes))
            
    # Pie de página requerido por la marca
    def agregar_pie_pagina(canvas, doc):
        canvas.saveState()
        texto_pie_str = "Creado con SIVEC (Sistema de Inteligencia para la Vanguardia Experimental y Científica) | Propiedad de Rubio Intelligence Systems."
        canvas.setFont('Helvetica-Bold', 8)
        canvas.setFillColor(colors.HexColor('#A0AEC0'))
        canvas.drawCentredString(letter[0]/2.0, 30, texto_pie_str)
        canvas.restoreState()

    doc.build(historia, onFirstPage=agregar_pie_pagina, onLaterPages=agregar_pie_pagina)
    buffer.seek(0)
    return buffer.getvalue()

# ==============================================================================
# NÚCLEO LÓGICO DE EXTRACCIÓN (Capa Ofuscada)
# ==============================================================================
def ejecutar_sivec(termino, pregunta):
    URL_API = "https://api.openalex.org/works"
    config_busqueda = {'search': termino, 'filter': 'is_oa:true', 'per_page': 10, 'sort': 'cited_by_count:desc'}
    cabeceras = {'User-Agent': 'Mozilla/5.0'}
    
    st.write("🔎 Escaneando literatura global y bases de datos indexadas...")
    try:
        respuesta = requests.get(URL_API, params=config_busqueda).json()
        resultados = respuesta.get('results', [])
    except Exception:
        st.error("❌ Error de comunicación con los repositorios globales.")
        return
    
    lote_sivec = []
    for paper in resultados:
        if len(lote_sivec) >= max_papers: break
        url_pdf = paper.get('open_access', {}).get('oa_url')
        if url_pdf:
            try:
                descarga = requests.get(url_pdf, headers=cabeceras, timeout=10)
                if descarga.status_code == 200 and descarga.content.startswith(b'%PDF'):
                    nombre_archivo = f"temp_core_{len(lote_sivec)+1}.pdf"
                    with open(nombre_archivo, 'wb') as f:
                        f.write(descarga.content)
                    lote_sivec.append({
                        "id": len(lote_sivec)+1,
                        "titulo": paper.get('title', 'Sin título'),
                        "doi": paper.get('doi', 'No registrado'),
                        "archivo_local": nombre_archivo
                    })
                    st.write(f"📥 Fuente de validación #{len(lote_sivec)} asegurada con éxito.")
            except: continue

    if not lote_sivec:
        st.error("❌ No se encontraron fuentes documentales suficientes en acceso abierto para este término.")
        return

    st.write("🧠 Procesando masa crítica en paralelo con IA...")
    try:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        archivos_gemini = []
        referencias = ""
        
        for p in lote_sivec:
            archivo_subido = client.files.upload(file=p['archivo_local'])
            archivos_gemini.append(archivo_subido)
            referencias += f"Doc #{p['id']}: {p['titulo']} | Ref: {p['doi']}\n"

        prompt_maestro = f"""
        Eres un motor analítico avanzado de nivel de producción propiedad de Rubio Intelligence Systems. 
        Analiza con extremo rigor los documentos adjuntos y responde con un dictamen detallado a: "{pregunta}".
        
        Reglas de Adaptación Científica:
        1. Contextualiza tu análisis según la rama seleccionada: {area_estrategica}.
        2. Si la rama pertenece a Ciencias Sociales/Humanidades, prioriza análisis cualitativo y marcos teóricos.
        3. Si la rama pertenece a Ciencias Exactas/Ingeniería/Médicas, extrae métricas, eficiencias y datos duros en tablas estructuradas de Markdown.
        4. Usa citas explícitas como [Documento #1].
        """
        
        respuesta_ia = client.models.generate_content(model="gemini-2.5-flash", contents=archivos_gemini + [prompt_maestro])
        
        if respuesta_ia and respuesta_ia.text:
            st.success("📊 Dictamen Completado")
            st.markdown(respuesta_ia.text)
            
            st.markdown("---")
            st.markdown("### 📚 Fuentes Oficiales de Validación")
            st.info(referencias)
            
            # 📥 BOTÓN EXCLUSIVO: Generación y descarga del entregable PDF corporativo
            pdf_data = generar_pdf_dictamen(respuesta_ia.text, referencias)
            st.download_button(
                label="📥 Descargar Dictamen Oficial en PDF",
                data=pdf_data,
                file_name=f"Dictamen_SIVEC_{area_estrategica.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("⚠️ El motor procesó los datos pero la salida requiere un reintento del buffer.")
        
        for archivo in archivos_gemini:
            client.files.delete(name=archivo.name)
            
    except Exception as e:
        st.error("❌ Error en la capa del motor analítico inteligente.")

# ==============================================================================
# INTERFAZ DE USUARIO PRINCIPAL
# ==============================================================================
st.markdown(f"### 📑 Módulo Activo: {area_estrategica}")
termino_busqueda = st.text_input("Palabras clave para la búsqueda científica (parámetros técnicos globales):", placeholder="Ej. Autonomous weapons laws ethics regulations")
pregunta_usuario = st.text_area("Pregunta de investigación detallada (objetivos del dictamen):", placeholder="Ej. ¿Qué vacíos legales reportan frente al derecho internacional?")

if st.button("🚀 Lanzar Análisis de Vanguardia"):
    if not termino_busqueda or not pregunta_usuario:
        st.warning("⚠️ Completa ambos campos para iniciar el escaneo.")
    else:
        with st.status("🛸 Procesando peticiones en la infraestructura de Rubio Intelligence Systems...", expanded=True) as status:
            ejecutar_sivec(termino_busqueda, pregunta_usuario)
            status.update(label="✅ Análisis finalizado", state="complete")
