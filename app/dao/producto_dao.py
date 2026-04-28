from app.utils.firebase import get_firestore
from app.DTOs.producto_dto import ProductoCreate, ProductoUpdate
from app.utils.exceptions import NotFoundException, DatabaseException


class ProductoDAO:
    """Data Access Object para Producto (usando Firestore)"""

    COLLECTION = "productos"

    @staticmethod
    def create(producto: ProductoCreate) -> dict:
        """Crear un nuevo producto en Firestore"""
        try:
            db = get_firestore()
            producto_dict = producto.dict()
            
            # Generar ID si no existe
            if not producto_dict.get("id"):
                producto_dict["id"] = db.collection(ProductoDAO.COLLECTION).document().id
            
            doc_ref = db.collection(ProductoDAO.COLLECTION).document(producto_dict["id"])
            doc_ref.set(producto_dict)
            
            return producto_dict
        except Exception as e:
            raise DatabaseException(f"Error al crear producto: {str(e)}")

    @staticmethod
    def get_by_id(producto_id: str) -> dict:
        """Obtener producto por ID desde Firestore"""
        try:
            db = get_firestore()
            doc = db.collection(ProductoDAO.COLLECTION).document(producto_id).get()
            
            if not doc.exists:
                raise NotFoundException(f"Producto con ID {producto_id} no encontrado")
            
            return doc.to_dict()
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al obtener producto: {str(e)}")

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> list:
        """Obtener todos los productos desde Firestore"""
        try:
            db = get_firestore()
            docs = db.collection(ProductoDAO.COLLECTION).offset(skip).limit(limit).stream()
            
            productos = []
            for doc in docs:
                productos.append(doc.to_dict())
            
            return productos
        except Exception as e:
            raise DatabaseException(f"Error al obtener productos: {str(e)}")

    @staticmethod
    def get_by_categoria(categoria: str) -> list:
        """Obtener productos por categoría desde Firestore"""
        try:
            db = get_firestore()
            docs = db.collection(ProductoDAO.COLLECTION).where("categoria", "==", categoria).stream()
            
            productos = []
            for doc in docs:
                productos.append(doc.to_dict())
            
            return productos
        except Exception as e:
            raise DatabaseException(f"Error al obtener productos por categoría: {str(e)}")

    @staticmethod
    def update(producto_id: str, producto_update: ProductoUpdate) -> dict:
        """Actualizar producto en Firestore"""
        try:
            db = get_firestore()
            producto = ProductoDAO.get_by_id(producto_id)
            
            update_data = producto_update.dict(exclude_unset=True)
            producto.update(update_data)
            
            db.collection(ProductoDAO.COLLECTION).document(producto_id).update(update_data)
            
            return producto
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al actualizar producto: {str(e)}")

    @staticmethod
    def delete(producto_id: str) -> bool:
        """Eliminar producto de Firestore"""
        try:
            db = get_firestore()
            ProductoDAO.get_by_id(producto_id)  # Verificar que existe
            
            db.collection(ProductoDAO.COLLECTION).document(producto_id).delete()
            return True
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al eliminar producto: {str(e)}")
