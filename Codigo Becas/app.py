# -- coding: utf-8 --
"""
Aplicación mejorada con múltiples métodos de conversión PDF a imagen y edición manual de resultados
"""

import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import re
import unicodedata
import base64

st.set_page_config(
    page_title="Plataforma de evaluación de perfiles de becas UTPL",
    layout="wide",
    page_icon="🎓",
    initial_sidebar_state="auto"
)

# Función para cargar imagen local como base64
def get_base64_image(image_path):
    """Convierte una imagen local a base64 para usar en HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.warning(f"⚠ No se encontró la imagen en: {image_path}")
        return None

# Cargar el logo local
logo_path = r"utpl3-Photoroom.png"  # Asume que está en la misma carpeta del script
logo_base64 = get_base64_image(logo_path)

# CSS personalizado para mejorar el diseño
st.markdown("""
<style>
    /* Fondo general blanco */
    .main {
        background-color: white;
    }
    
    .stApp {
        background-color: white;
    }
    
    /* Header personalizado mejorado - MÁS GRANDE Y MÁS ARRIBA */
    .custom-header {
        background: #004270;   
        padding: 3.5rem 3rem;
        border-radius: 20px;
        margin: -2rem 0 2.5rem 0;
        box-shadow: 0 15px 35px rgba(0, 66, 112, 0.2);    /* Ajusté la sombra al nuevo color */
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        align-items: center;
        overflow: hidden;
        min-height: 180px;
    }
    
    .custom-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
        pointer-events: none;
    }
    
    .header-content {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 3rem;
        position: relative;
        z-index: 2;
        height: 100%;
    }
    
    .header-text h1 {
        color: white;
        font-size: 3.2rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
        line-height: 1.1;
    }
    
    .header-text h2 {
        color: #dbeafe;
        font-size: 1.6rem;
        font-weight: 500;
        margin: 1rem 0 0 0;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .logo-container {
        flex-shrink: 0;
    }
    
    /* LOGO MÁS GRANDE */
    .logo-container img {
        width: 160px;        /* Aumenta el ancho */
        height: auto;        /* Mantiene proporción */
        object-fit: contain; /* Asegura buena visualización */
        background: transparent;
        padding: 0;
        margin-top: -30px;
        border: none;
        box-shadow: none;
        border-radius: 0;
        transition: none !important;
    }

    /* SECCIÓN PRINCIPAL CORREGIDA - FONDO CLARO */
    .main-section {
        background: linear-gradient(145deg, #f8fafc 0%, #ffffff 100%);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 2.5rem;
        position: relative;
    }
    
    .main-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4);
        border-radius: 20px 20px 0 0;
    }
    
    /* TÍTULO DE SECCIÓN CORREGIDO - TEXTO OSCURO */
    .section-title {
        color: #1e40af;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* TÍTULO PRINCIPAL MEJORADO - FONDO MUY CLARO */
    .titulo-principal {
        background: linear-gradient(145deg, #f1f5f9 0%, #ffffff 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #3b82f6;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    .titulo-principal h2 {
        color: #1e40af !important;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        text-shadow: none;
    }
            
    /* TÍTULOS DE ARCHIVOS EN EL PROCESAMIENTO - SIN CUADRO AZUL, TEXTO NEGRO */
    h3 {
        color: #1f2937 !important;           /* CAMBIÉ: de #1e40af (azul) a #1f2937 (negro) */
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        margin: 2rem 0 1rem 0 !important;
        padding: 1rem !important;
        background: transparent !important;   /* CAMBIÉ: de gradiente azul a transparente */
        border: none !important;             /* CAMBIÉ: eliminé el borde azul */
        border-radius: 0 !important;         /* CAMBIÉ: eliminé el border-radius */
        box-shadow: none !important;         /* CAMBIÉ: eliminé la sombra */
    }

    /* SELECTORES ADICIONALES PARA TÍTULOS DE ARCHIVOS */
    .main h3,
    [data-testid="stMarkdownContainer"] h3,
    div[data-testid="column"] h3,
    .stMarkdown h3 {
        color: #1f2937 !important;
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        padding: 1rem 0 !important;
    }

    /* SELECTOR MUY ESPECÍFICO PARA ELEMENTOS CON TEXTO DE ARCHIVO */
    [class="stMarkdown"] h3:contains("📄"),
    *:contains("Ejemplo erroneo.pdf") {
        color: #1f2937 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Estilos mejorados para los botones */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
    }
    
    /* Estilos base para la zona de subir archivos */
    .stFileUploader {
        border: 2px solid #e5e7eb;
        border-radius: 20px;
        padding: 3rem;
        background: linear-gradient(145deg, #f9fafb 0%, #f3f4f6 100%);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .stFileUploader::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(156, 163, 175, 0.1) 0%, transparent 70%);
        animation: pulse 3s ease-in-out infinite;
        pointer-events: none;
    }

    @keyframes pulse {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.1); }
    }

    .stFileUploader:hover {
        border-color: #9ca3af;
        background: linear-gradient(145deg, #f3f4f6 0%, #e5e7eb 100%);
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(107, 114, 128, 0.2);
    }

    /* CORREGIDO: Texto de instrucciones en la zona de arrastrar - COLOR OSCURO */
    .stFileUploader label {
        color: #374151 !important;
        font-weight: 600 !important;
    }

    .stFileUploader div[data-testid="stFileUploaderInstructions"] {
        color: #374151 !important;
    }

    /* CUADRO INTERIOR DEL DRAG AND DROP - COLOR MÁS SUAVE */
    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        background-color: #B7B7B7 !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        border: 2px dashed #ffffff40 !important;
    }

    /* DRAG AND DROP - TODOS LOS TEXTOS BLANCOS */
    .stFileUploader [data-testid="stFileUploaderDropzone"] * {
        color: #57564F !important;
        font-weight: 700 !important;
        text-shadow: none !important;
    }

    /* Específicamente el texto principal "Drag and drop files here" */
    .stFileUploader [data-testid="stFileUploaderDropzone"] div {
        color: #57564F !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        text-shadow: none !important;
    }

    /* El subtexto del límite */
    .stFileUploader [data-testid="stFileUploaderDropzone"] span {
        color: #57564F!important;
        font-weight: 600 !important;
        text-shadow: none !important;
    }

    /* Contenedor de archivos cargados - FONDO CLARO */
    .stFileUploader div[data-testid="stFileUploaderDropzone"] ~ div {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%) !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    }

    /* TÍTULOS DE ARCHIVOS - SIN CUADROS AZULES, SOLO TEXTO NEGRO */
    .stFileUploader div[data-testid="stFileUploaderDropzone"] ~ div span {
        color: #1f2937 !important;
        font-weight: 500 !important;
        font-size: 1.2rem !important;
        text-shadow: none !important;
        background: transparent !important;
        padding: 0 !important;
        border-radius: 0 !important;
        border: none !important;
    }

    /* TÍTULOS DE ARCHIVOS - LIMPIOS */
    .stFileUploader [data-testid="stFileUploaderFileName"] {
        color: #1f2937 !important;
        font-weight: 500 !important;
        font-size: 1.2rem !important;
        background: transparent !important;
        padding: 0 !important;
        border-radius: 0 !important;
        border: none !important;
        margin: 0 !important;
        display: inline !important;
    }

    /* CONTENEDOR DE ARCHIVOS - MÁS LIMPIO */
    .stFileUploader div[data-testid="stFileUploaderDropzone"] ~ div {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%) !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    }

    /* Información adicional de archivos - MÁS SUTIL */
    .stFileUploader [data-testid="stFileUploaderFileData"] {
        background-color: #f9fafb !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        margin: 0.5rem 0 !important;
    }

    /* Tamaño del archivo - TEXTO NORMAL */
    .stFileUploader [data-testid="stFileUploaderFileData"] span {
        color: #6b7280 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }

    /* CORREGIDO: Todos los elementos de texto en el file uploader */
    .stFileUploader * {
        color: #374151 !important;
    }

    /* Específicamente para los títulos de archivos */
    .stFileUploader div[data-baseweb="file-uploader"] span {
        color: #1f2937 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
            
   /* Botón "Browse files" - COLOR Y ESTILO CORREGIDO */
    .stFileUploader button[kind="secondary"] {
        background-color: #004270 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stFileUploader button[kind="secondary"]:hover {
        background-color: #003258 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(122, 122, 115, 0.3) !important;
    }

    /* Específicamente para el texto del botón Browse */
    .stFileUploader button[kind="secondary"] span {
        color: white !important;
        font-weight: 600 !important;
    }

    /* Botón de eliminar archivo */

    /* Botón de eliminar archivo */
    .stFileUploader button[title="Remove file"] {
        background-color: #E5E0D8!important;
        color: white !important;
        border-radius: 50% !important;
        width: 24px !important;
        height: 24px !important;
        border: none !important;
        font-weight: bold !important;
    }

    .stFileUploader button[title="Remove file"]:hover {
        background-color: #E5E0D8 !important;
        transform: scale(1.1) !important;
    }

    /* TÍTULOS DE ARCHIVOS EN EL PROCESAMIENTO - MUY VISIBLES */
    h3 {
        color: #1e40af !important;
        font-weight: 800 !important;
        font-size: 1.8rem !important;
        margin: 2rem 0 1rem 0 !important;
        padding: 1rem !important;
        background: linear-gradient(145deg, #f0f9ff 0%, #e0f2fe 100%) !important;
        border-left: 5px solid #2563eb !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* Estilos para los expanders */
    .streamlit-expanderHeader {
        background: #f1f5f9;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    /* Estilos mejorados para success/error messages */
    .stSuccess {
        background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
        border: 2px solid #10b981;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .stSuccess::before {
        content: '✓';
        position: absolute;
        right: 1rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        color: #10b981;
        opacity: 0.3;
    }
    
    .stError {
        background: linear-gradient(135deg, #fef2f2 0%, #fef7f7 100%);
        border: 2px solid #ef4444;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .stError::before {
        content: '✗';
        position: absolute;
        right: 1rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        color: #ef4444;
        opacity: 0.3;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fffbeb 0%, #fefce8 100%);
        border: 2px solid #f59e0b;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .stWarning::before {
        content: '⚠';
        position: absolute;
        right: 1rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        color: #f59e0b;
        opacity: 0.3;
    }
            
    /* MENSAJES DE ERROR Y ADVERTENCIA CON TEXTO OSCURO */
    .stError, .stError div, .stError p, .stError span {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }

    .stWarning, .stWarning div, .stWarning p, .stWarning span {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }

    .stSuccess, .stSuccess div, .stSuccess p, .stSuccess span {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }

    /* SELECTORES ADICIONALES PARA ALERTAS */
    [data-testid="stAlert"] {
        color: #1f2937 !important;
    }

    [data-testid="stAlert"] div,
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span {
        color: #1f2937 !important;
        font-weight: 600 !important;
    
    }
            
    /* TEXTO DE INFORMACIÓN EXTRAÍDA Y FORMULARIOS */
    .stMarkdown p, .stMarkdown li, .stMarkdown strong {
        color: #1f2937 !important;
    }

    /* ESPECÍFICAMENTE PARA LA INFORMACIÓN EXTRAÍDA */
    .stMarkdown p:contains("Información extraída"),
    .stMarkdown p:contains("Título:"),
    .stMarkdown p:contains("Fecha:"),
    .stMarkdown p:contains("Emisor:"),
    .stMarkdown p:contains("Destinatario:"),
    .stMarkdown p:contains("Nacionalidad:") {
        color: #1f2937 !important;
    }

    /* TODOS LOS PÁRRAFOS EN MARKDOWN */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] strong,
    [data-testid="stMarkdownContainer"] span {
        color: #1f2937 !important;
    }
    
    /* BOTONES - TEXTO BLANCO VISIBLE */
    .stButton > button,
    .stDownloadButton > button {
        color: white !important;
        font-weight: 700 !important;
    }

    /* TEXTO DENTRO DE BOTONES */
    .stButton > button span,
    .stDownloadButton > button span,
    .stButton > button p,
    .stDownloadButton > button p {
        color: white !important;
        font-weight: 700 !important;
    }

    /* EXPANDERS */
    .streamlit-expanderHeader p,
    .streamlit-expanderContent p,
    [data-testid="stExpander"] p {
        color: #1f2937 !important;
    }

    /* LABELS DE INPUTS */
    .stTextInput label,
    .stTextArea label,
    [data-testid="stTextInput"] label,
    [data-testid="stTextArea"] label {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }

    /* ASEGURAR VISIBILIDAD DE TODO EL TEXTO */
    .main p, .main li, .main span, .main strong {
        color: #1f2937 !important;
    }

    /* TEXTO EN COLUMNAS */
    .stColumn p, .stColumn li, .stColumn span {
        color: #1f2937 !important;
    }

    /* CONTENIDO GENERAL */
    .block-container p,
    .block-container li,
    .block-container span,
    .block-container strong {
        color: #1f2937 !important;
    }
    
    /* Estilos mejorados para las métricas */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 18px;
        border: 2px solid #e2e8f0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        border-radius: 18px 18px 0 0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.12);
        border-color: #3b82f6;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e40af;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .metric-label {
        color: #64748b;
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Estilos para las imágenes */
    .document-image {
        border: 3px solid #e5e7eb;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* Estilos mejorados para la información extraída */
    .info-card {
        background: linear-gradient(145deg, #f8fafc 0%, #ffffff 100%);
        border: 2px solid #e2e8f0;
        border-radius: 18px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.06);
        position: relative;
    }
    
    .info-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #06b6d4, #3b82f6, #8b5cf6);
        border-radius: 18px 18px 0 0;
    }
    
    .info-card h4 {
        color: #1e40af;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .info-item {
        margin-bottom: 1rem;
        padding: 1rem;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }
    
    .info-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
        border-left-color: #2563eb;
    }
    
    .info-label {
        font-weight: 700;
        color: #374151;
        font-size: 1rem;
        display: inline-block;
        min-width: 150px;
    }
    
    .info-value {
        color: #1f2937;
        font-weight: 500;
        margin-left: 0.5rem;
        font-size: 1rem;
    }
    
    /* Separadores */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #3b82f6, transparent);
        margin: 2rem 0;
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Header personalizado con escudo UTPL - SOLO IMAGEN LOCAL
if logo_base64:
    st.markdown(f"""
    <div class="custom-header">
        <div class="header-content">
            <div class="logo-container">
                <img src="data:image/jpeg;base64,{logo_base64}" alt="Escudo UTPL">
            </div>
            <div class="header-text">
                <h1>Plataforma de evaluación de perfiles de becas UTPL</h1>
                <h2>🎓 Beca de pueblos y nacionalidades</h2>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.error("❌ No se pudo cargar el logo de la UTPL. Verifica que el archivo 'LOGO UTPL.png' esté en la misma carpeta que este script.")
    st.stop()  # Detiene la aplicación si no encuentra el logo

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Título simple sin cuadro - color oscuro
st.markdown("""
<h1 style="color: #1f2937; font-size: 2.5rem; font-weight: 700; margin-bottom: 2rem;">
    📄 Verificador de Documentos
</h1>
""", unsafe_allow_html=True)

# Cargar CSV de pueblos y nacionalidades
df_pueblos = pd.read_csv("pueblos_nacionalidades_actualizado.csv", sep=";")

def normalizar(texto):
    if not texto:
        return ""
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto.lower().strip()

pueblos_originales = df_pueblos["titulo"].tolist()
pueblos_normalizados = [normalizar(p) for p in pueblos_originales]

def contiene_pueblo(texto):
    texto_norm = normalizar(texto)
    
    # Palabras clave principales
    if 'kichwa' in texto_norm:
        return "NACIONALIDAD KICHWA"
    if 'shuar' in texto_norm:
        return "NACIONALIDAD SHUAR"
    # ... agregar más según necesites
    
    # Búsqueda original como respaldo
    for i, pueblo in enumerate(pueblos_normalizados):
        if re.search(rf"\b{re.escape(pueblo)}\b", texto_norm):
            return pueblos_originales[i]
    
    return None

def detectar_nacionalidad_para_advertencia(texto_ocr):
    """Función específica para detectar nacionalidad en documentos no relacionados con Ecuador"""
    
    # Primero buscar pueblos específicos
    pueblos_especificos = [
        r"pueblo\s+(bribri|shuar|achuar|kichwa|chachi|tsachila|awa|cofan|siona|secoya|waodani|shiwiar|andwa|sapara)",
        r"nacionalidad\s+(bribri|shuar|achuar|kichwa|chachi|tsachila|awa|cofan|siona|secoya|waodani|shiwiar|andwa|sapara)",
        r"idioma\s+(bribri|shuar|achuar|kichwa|chachi|tsachila|awa|cofan|siona|secoya|waodani|shiwiar|andwa|sapara)",
        r"hablante\s+del\s+idioma\s+(bribri|shuar|achuar|kichwa|chachi|tsachila|awa|cofan|siona|secoya|waodani|shiwiar|andwa|sapara)"
    ]
    
    for patron in pueblos_especificos:
        match = re.search(patron, texto_ocr, re.IGNORECASE)
        if match:
            return match.group(1).upper()
    
    # Si no encuentra específicos, usar el patrón general
    posibles_nombres = re.findall(r"nacionalidad\s+([a-záéíóúñA-ZÁÉÍÓÚÑ\s]+?)\b", texto_ocr, re.IGNORECASE)
    if posibles_nombres:
        return posibles_nombres[0].strip().upper()
    
    return None

def extraer_info(texto):
    texto = re.sub(r'\s+', ' ', texto.strip())

    titulo = re.search(r"(certificado de pertenencia|resoluci[oó]n\s+n[º°]?\s*\S+|acuerdo|nacionalidades y pueblos originarios.+?|aval)", texto, re.IGNORECASE)
    fecha = re.search(r"(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})", texto, re.IGNORECASE)

    # Emisor
    emisor_match = re.search(r"la\s+suscrita\s+señora[\s,]+([a-záéíóúñ\s]+?)(?:,|\s+con\s+c[eé]dula)", texto, re.IGNORECASE)
    emisor = emisor_match.group(1).strip().upper() if emisor_match else "No detectado"

    # Cargo del emisor
    cargo_match = re.search(rf"{re.escape(emisor)}.*?en\s+calidad\s+de\s+([a-záéíóúñ\s\"']{{5,100}}?)(?:\.|,)", texto, re.IGNORECASE)
    cargo = cargo_match.group(1).strip().upper() if cargo_match else "No detectado"

    # Cédula
    cedula_match = re.search(r"(\d{6,10}[\-\d]*)", texto)
    cedula = cedula_match.group(1) if cedula_match else ""

    # Destinatario (nueva lógica mejorada)
    destinatario_match = re.search(
        r"(?:certifica\s+que\s+)?(?:la|el)\s+(?:ciudadana|ciudadano|joven)?\s*([A-ZÁÉÍÓÚÑa-záéíóúñ]{2,}(?:\s+[A-ZÁÉÍÓÚÑa-záéíóúñ]{2,}){1,4})[,;\s]+\s*con\s+c[eé]dula",
        texto,
        re.IGNORECASE
    )
    if not destinatario_match:
        destinatario_match = re.search(
            r"conocer\s+al\s+(?:joven|ciudadano):?\s*([A-ZÁÉÍÓÚÑa-záéíóúñ\s]{3,50})[,;\s]+portador",
            texto,
            re.IGNORECASE
        )
    destinatario = destinatario_match.group(1).strip().upper() if destinatario_match else "No detectado"

    # Nacionalidad
    nacionalidad_match = re.search(r"nacionalidad\s*[:\-]?\s*([a-záéíóúñ\s]{3,80}?)(?:[\.,;\n]|$)", texto, re.IGNORECASE)
    nacionalidad = nacionalidad_match.group(1).strip().upper() if nacionalidad_match else "No detectada"

    # Ubicación
    provincia = re.search(r"provincia\s*[:\-]?\s*([a-záéíóúñ\s]+)", texto, re.IGNORECASE)
    canton = re.search(r"cant[oó]n\s*[:\-]?\s*([a-záéíóúñ\s]+)", texto, re.IGNORECASE)
    parroquia = re.search(r"parroquia\s*[:\-]?\s*([a-záéíóúñ\s]+)", texto, re.IGNORECASE)
    barrio = re.search(r"(barrio|comunidad)\s*[:\-]?\s*([a-záéíóúñ\s]+)", texto, re.IGNORECASE)

    # Motivo
    motivo_match = re.search(r"(para\s+tramitar.+?\.|por\s+el\s+presente.+?\.|certifica.+?\.|motivo:.+?\.|que\s+se\s+encuentra.+?\.)", texto, re.IGNORECASE)
    motivo = motivo_match.group(0).strip().capitalize() if motivo_match else "No detectado"

    return {
        "title": titulo.group(0).strip().upper() if titulo else "No detectado",
        "date": fecha.group(0).strip().capitalize() if fecha else "No detectada",
        "issuer": emisor,
        "issuer_position": cargo,
        "recipient": destinatario,
        "recipient_id": cedula,
        "nationality": nacionalidad,
        "province": provincia.group(1).strip().upper() if provincia else "N/A",
        "canton": canton.group(1).strip().upper() if canton else "N/A",
        "parish": parroquia.group(1).strip().upper() if parroquia else "N/A",
        "neighborhood": barrio.group(2).strip().upper() if barrio else "N/A",
        "reason": motivo
    }



def extraer_imagenes(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []
    for page in doc:
        mat = fitz.Matrix(4, 4)
        pix = page.get_pixmap(matrix=mat)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        images.append(img)
    doc.close()
    return images

uploaded_files = st.file_uploader("📁 Sube archivos PDF", type="pdf", accept_multiple_files=True)
resultados = []

if uploaded_files:
    for i, pdf_file in enumerate(uploaded_files):
        st.markdown(f"---\n### 📄 {pdf_file.name}")
        pdf_bytes = pdf_file.read()
        imagenes = extraer_imagenes(pdf_bytes)

        texto_ocr = ""
        for img in imagenes:
            st.image(img, width=400)
            texto_ocr += pytesseract.image_to_string(img, lang="spa") + "\n"

        pueblo_detectado = contiene_pueblo(texto_ocr)

        if not pueblo_detectado:
            st.error("❌ El documento no está relacionado con ningún pueblo o nacionalidad reconocida del Ecuador.")
            
            # Usar la nueva función para detectar nacionalidad
            nacionalidad_detectada = detectar_nacionalidad_para_advertencia(texto_ocr)
            if nacionalidad_detectada:
                st.warning(f"⚠ Nacionalidad detectada: {nacionalidad_detectada}")
            continue

        st.success(f"✅ Relacionado con pueblos y nacionalidades del Ecuador: {pueblo_detectado}")

        info = extraer_info(texto_ocr)

        data = {
            "Nombre de archivo": pdf_file.name,
            "Texto extraído": texto_ocr.strip(),
            **info
        }

        with st.expander("✏ Editar información", expanded=False):
            key_prefix = pdf_file.name + str(i)
            col1, col2 = st.columns(2)
            with col1:
                data['title'] = st.text_input("Título", data['title'], key=f"title_{key_prefix}")
                data['date'] = st.text_input("Fecha", data['date'], key=f"date_{key_prefix}")
                data['issuer'] = st.text_input("Emisor", data['issuer'], key=f"issuer_{key_prefix}")
                data['issuer_position'] = st.text_input("Cargo del emisor", data['issuer_position'], key=f"pos_{key_prefix}")
            with col2:
                data['recipient'] = st.text_input("Destinatario", data['recipient'], key=f"dest_{key_prefix}")
                data['recipient_id'] = st.text_input("Cédula", data['recipient_id'], key=f"ced_{key_prefix}")
                data['nationality'] = st.text_input("Nacionalidad", data['nationality'], key=f"nac_{key_prefix}")
            data['province'] = st.text_input("Provincia", data['province'], key=f"prov_{key_prefix}")
            data['canton'] = st.text_input("Cantón", data['canton'], key=f"canton_{key_prefix}")
            data['parish'] = st.text_input("Parroquia", data['parish'], key=f"parish_{key_prefix}")
            data['neighborhood'] = st.text_input("Barrio", data['neighborhood'], key=f"neigh_{key_prefix}")
            data['reason'] = st.text_area("Motivo", data['reason'], height=100, key=f"mot_{key_prefix}")

        st.markdown(f"""
        📌 *Información extraída:*

        - *Título:* {data['title']}
        - *Fecha:* {data['date']}
        - *Emisor:* {data['issuer']}
        - *Cargo del emisor:* {data['issuer_position']}
        - *Destinatario:* {data['recipient']}
        - *Cédula:* {data['recipient_id']}
        - *Nacionalidad:* {data['nationality']}
        - *Provincia:* {data['province']}
        - *Cantón:* {data['canton']}
        - *Parroquia:* {data['parish']}
        - *Barrio/Comunidad:* {data['neighborhood']}
        - *Motivo:* {data['reason']}
        """)

        resultados.append(data)

    if resultados:
        df = pd.DataFrame(resultados)
        df = df.rename(columns={
            "title": "Título",
            "date": "Fecha",
            "issuer": "Emisor",
            "issuer_position": "Cargo del emisor",
            "recipient": "Destinatario",
            "recipient_id": "Cédula",
            "nationality": "Nacionalidad",
            "province": "Provincia",
            "canton": "Cantón",
            "parish": "Parroquia",
            "neighborhood": "Barrio/Comunidad",
            "reason": "Motivo"
        })

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Análisis")

        st.download_button(
            label="📥 Descargar resultados en Excel",
            data=output.getvalue(),
            file_name="analisis_mistral_pueblos_editable.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )