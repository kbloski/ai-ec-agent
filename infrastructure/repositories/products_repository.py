from sqlalchemy.orm import Session
from typing import List, Optional
from domain.models.product.product import Product
from infrastructure.logging.logger import Logger

class ProductRepository:
    def __init__(self, logger : Logger, db: Session):
        self.db = db

    # ➕ CREATE
    def create(self, product : Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    # 🔍 GET BY ID
    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    # 📋 GET ALL
    def get_all(self) -> List[Product]:
        return self.db.query(Product).all()

    # # ✏️ UPDATE
    # def update(self, product_id: int, name: str = None, price: float = None) -> Optional[Product]:
    #     product = self.get_by_id(product_id)
    #     if not product:
    #         return None

    #     if name is not None:
    #         product.name = name
    #     if price is not None:
    #         product.price = price

    #     self.db.commit()
    #     self.db.refresh(product)
    #     return product

    # # ❌ DELETE
    # def delete(self, product_id: int) -> bool:
    #     product = self.get_by_id(product_id)
    #     if not product:
    #         return False

    #     self.db.delete(product)
    #     self.db.commit()
    #     return True

    def delete_all(self) -> int:
        deleted = self.db.query(Product).delete()
        self.db.commit()
        return deleted