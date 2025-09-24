# 📄Sistema de Extracción de Información de Documentos PDF

Sistema automatizado para extraer información clave de documentos PDF relacionados con becas de pueblos y nacionalidades ecuatorianas, utilizando OCR y procesamiento de documentos escaneados.

## 🎯 Objetivo
Automatizar la extracción de información importante (nombres, número de cédula, pueblo de origen, etc.) desde documentos PDF, facilitando la evaluación de perfiles de becas de forma más rápida y precisa.

## ✨ Características
- Procesa **PDFs escaneados** (no requiere texto digital).
- Usa **PyMuPDF, Tesseract y PIL** para extraer información clave.
- Extracción Automática: Nombres, cédulas, nacionalidades, ubicaciones y motivos
- Validación de pueblos/nacionalidades reconocidos.
- Exportación a **Excel** de los resultados.
- Soporte para múltiples documentos.
- Interfaz simple en **Streamlit**.

## 🔧 Tecnologías Utilizadas
- Python 3.10+
- PyMuPDF
- Pandas
- XlsxWriter
- Pillow (PIL)
- Tesseract OCR
- Streamlit

## ☑ Instalación 

1. **Clonar el repositorio**
```bash
git clone https://github.com/mariangel188/Beca_Pueblos_Nacionalidades.git
cd Beca_Pueblos_Nacionalidades
```
2. **Crear entorno virtual**
```bash
python -m venv env
```
3. **Activar entorno virtual**
- En Windows:
```bash
.\env\Scripts\activate
```
- En Linux / MacOS:
```bash
source env/bin/activate
```
4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```
5. **Configurar Tesseract OCR**
- En Windows:
  
  1.Descargar el instalador desde: Tesseract UB Mannheim.
  
  2.Ejecutar el instalador y seguir los pasos para la respectiva instalación.
  
  3.Por defecto se instalará en:
  ```python
  C:\Program Files\Tesseract-OCR\
  ```
  4.En app.py, ajustar la ruta si es necesario:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```
- En Linux / MacOS:
```bash
sudo apt install tesseract-ocr
```
Verificar la instalación:
```bash
tesseract --version
```
6. **Ejecutar la aplicación**
```bash
streamlit run app.py
```
Abrir el navegador: http://localhost:8501

## Personalizar Pueblos y Nacionalidades
Editar data/pueblos_nacionalidades.json: 
```json
{
  "pueblos": ["Achuar", "Awá", "Chachi", "Cofán", "..."],
  "nacionalidades": ["Kichwa", "Shuar", "Tsáchila", "..."]
}
```
## 📁 Estructura del proyecto
```
Beca_Pueblos_Nacionalidades/
├── codigo_becas/                  # Código y archivos principales
│   ├── app.py
│   ├── articles_processing.ipynb
│   ├── build_RAG_with_milvus_and_mistral.ipynb
│   ├── documents.pkl
│   └── requirements.txt
├── ejemplos_pdf/                  # PDFs de prueba
│   ├── prueba1.pdf
│   ├── prueba2.pdf
│   └── prueba3.pdf
├── ejemplo_excel/                 # Resultados de ejemplo
│   └── resultados.xlsx
├── pueblos_nacionalidades_actualizado.csv
├── pueblos_y_nacionalidades.csv
└── README.md
```
## 🔍 Flujo de uso 
1. Subir el documento PDF escaneado.
   
2. El sistema procesa con OCR y extrae los elementos importantes.
   
3. Valida y edita los datos detectados.
   
4. Exporta los resultados a Excel.

## 🔄 Limitaciones
- No válida legalmente firmas ni sellos.
- Tiene una dependencia de la calidad del escaneo.
- Es sensible a variaciones de formato en los documentos.

## 🚧 Próximas mejoras
- Verificación automática de firmas válidas.
- Integración con el sistema oficial de becas.
  
## 📈 Estadísticas del Proyecto 
- Precisión OCR: ~85-95% (dependiente de calidad de documentos)
- Tiempo de Procesamiento: 2-5 segundos por página
- Formatos Soportados: PDF (escaneados y nativos)
- Tamaño Máximo: 200MB por archivo
