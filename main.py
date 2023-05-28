import os
import PyPDF2
from fastapi import FastAPI, UploadFile, File
from reader import reader

app = FastAPI()

@app.post("/upload/pdf")
async def process_pdf(file: UploadFile = File(...)):
    # Obtener el nombre del archivo enviado
    file_name = file.filename

    # Guardar el archivo PDF en el sistema de archivos
    with open(file_name, 'wb') as pdf_file:
        pdf_file.write(await file.read())

    # Leer el contenido del archivo PDF guardado
    with open(file_name, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_object = pdf_reader.pages[0]
        data = pdf_object.extract_text()
        

    # Eliminar el archivo PDF guardado
    os.remove(file_name)

    # Realiza aquí el procesamiento adicional de la información extraída si es necesario
    return reader(data)