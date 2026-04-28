from app.dao.producto_dao import ProductoDAO
from app.DTOs.producto_dto import ProductoCreate, ProductoUpdate, ProductoResponse


class ProductoService:
    """Service para la lógica de negocio de Productos (usando Firestore)"""

    @staticmethod
    def crear_producto(producto: ProductoCreate) -> ProductoResponse:
        """Crear un nuevo producto"""
        db_producto = ProductoDAO.create(producto)
        return ProductoResponse(**db_producto)

    @staticmethod
    def obtener_producto(producto_id: str) -> ProductoResponse:
        """Obtener datos de un producto"""
        producto = ProductoDAO.get_by_id(producto_id)
        return ProductoResponse(**producto)

    @staticmethod
    def obtener_productos(skip: int = 0, limit: int = 100) -> list[ProductoResponse]:
        """Obtener lista de productos"""
        productos = ProductoDAO.get_all(skip, limit)
        return [ProductoResponse(**p) for p in productos]

    @staticmethod
    def obtener_productos_por_categoria(categoria: str) -> list[ProductoResponse]:
        """Obtener productos por categoría"""
        productos = ProductoDAO.get_by_categoria(categoria)
        return [ProductoResponse(**p) for p in productos]

    @staticmethod
    def actualizar_producto(producto_id: str, producto_update: ProductoUpdate) -> ProductoResponse:
        """Actualizar datos de producto"""
        producto = ProductoDAO.update(producto_id, producto_update)
        return ProductoResponse(**producto)

    @staticmethod
    def eliminar_producto(producto_id: str) -> dict:
        """Eliminar un producto"""
        ProductoDAO.delete(producto_id)
        return {"mensaje": "Producto eliminado correctamente"}
