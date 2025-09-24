# Sistema de Extracción de Información de Documentos PDF
Proyecto: Beca de Pueblos y Nacionalidades

## Objetivo
Automatizar la extracción de información importante (nombres, número de cédula, pueblo de origen, etc.) desde documentos PDF, facilitando la evaluación de perfiles de becas de forma más rápida y precisa.

## Características
- Procesa **PDFs escaneados** (no requiere texto digital).
- Usa **PyMuPDF, Tesseract y PIL** para extraer información clave.
- Extrae automáticamente:
  - Número de cédula
  - Nombres y apellidos
  - Pueblo / Nacionalidad
  - Ubicación y motivo
- Validación de pueblos/nacionalidades reconocidos.
- Exportación a **Excel** de los resultados.
- Soporte para múltiples documentos.
- Interfaz simple en **Streamlit**.

## Tecnologías
- Python 3.10+
- PyMuPDF
- Pandas
- XlsxWriter
- Pillow (PIL)
- Tesseract OCR
- Streamlit

## Instalación 

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
- En Linux/MacOS:
```bash
source env/bin/activate
```
4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```
5. **Configurar Tesseract OCR**
- En Windows:
  
  1.Descargar el instalador desde: Tesseract UB Mannheim
  
  2.Ejecutar el instalador y seguir los pasos para la respectiva instalación
  
  3.Por defecto se instalará en:
  ```python
  C:\Program Files\Tesseract-OCR\
  ```
  4.En app.py, ajustar la ruta si es necesario:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```
- En Linux/ MacOS:
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
