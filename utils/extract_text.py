import os
import PyPDF2

def leer_pdf(file):
    # Guardar el archivo PDF en el sistema de archivos
    with open(file.filename, 'wb') as pdf_file:
        pdf_file.write(file.file.read())

    # Leer el contenido del archivo PDF guardado
    with open(file.filename, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_object = pdf_reader.pages[0]
        data = pdf_object.extract_text()

    # Eliminar el archivo PDF guardado
    os.remove(file.filename)

    return data
