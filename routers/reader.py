from fastapi import APIRouter
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from utils.extract_text import leer_pdf
from services.reader import ReaderService

reader_router = APIRouter()

@reader_router.post("/upload/pdf", tags=["reader"], status_code=200)
async def process_pdf(file: UploadFile = File(...)):
    data = leer_pdf(file)
    result = ReaderService().procesar(data)
    return JSONResponse(status_code=200, content= jsonable_encoder(result))


