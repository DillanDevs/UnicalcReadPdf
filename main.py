from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers.reader import reader_router
from middlewares.error_handler import ErrorHandler
import uvicorn
import os

app = FastAPI(
    title="API unicalc",
    description="API para el extraer notas, para el proyecto unicalc",
    version="1.0",
)

# Configurar los orígenes permitidos
origins = [
    "http://localhost:3000",  # Agrega aquí el origen de tu aplicación de React
    # Otros orígenes permitidos si es necesario
    "https://unicalcgmd.netlify.app"  # Agrega aquí el dominio de tu página web desplegada
    # Otros orígenes permitidos si es necesario
]

# Habilitar CORS

app.add_middleware(ErrorHandler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reader_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
                port=int(os.environ.get("PORT", 8000)))