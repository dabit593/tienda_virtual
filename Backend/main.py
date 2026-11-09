from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from controller.auth_controller import router as auth_router
from controller.carrito_controller import router as carrito_router
from controller.categoria_controller import router as categoria_router
from controller.pedido_controller import router as pedido_router
from controller.producto_controller import router as producto_router
from db.database import crear_tablas

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app = FastAPI(lifespan=crear_tablas)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def error_de_datos(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Revisa los datos. Faltan campos o algún valor no es válido."
        }
    )


app.include_router(auth_router)
app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(carrito_router)
app.include_router(pedido_router)

carpeta_assets = Path(__file__).resolve().parent.parent / "Assets"
app.mount("/assets", StaticFiles(directory=carpeta_assets), name="assets")
