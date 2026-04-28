from fastapi import APIRouter, HTTPException, status
from app.services.producto_service import ProductoService
from app.DTOs.producto_dto import ProductoCreate, ProductoUpdate, ProductoResponse
from app.utils.exceptions import SubSonicException

router = APIRouter(prefix="/api/productos", tags=["Productos"])


@router.post("", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate):
    """Crear un nuevo producto"""
    try:
        return ProductoService.crear_producto(producto)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: str):
    """Obtener datos de un producto"""
    try:
        return ProductoService.obtener_producto(producto_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", response_model=list[ProductoResponse])
def obtener_productos(skip: int = 0, limit: int = 100):
    """Obtener lista de productos"""
    return ProductoService.obtener_productos(skip, limit)


@router.get("/categoria/{categoria}", response_model=list[ProductoResponse])
def obtener_productos_por_categoria(categoria: str):
    """Obtener productos por categoría"""
    return ProductoService.obtener_productos_por_categoria(categoria)


@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: str, producto_update: ProductoUpdate):
    """Actualizar datos de producto"""
    try:
        return ProductoService.actualizar_producto(producto_id, producto_update)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{producto_id}")
def eliminar_producto(producto_id: str):
    """Eliminar un producto"""
    try:
        return ProductoService.eliminar_producto(producto_id)
    except SubSonicException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
