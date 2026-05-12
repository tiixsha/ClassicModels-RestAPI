from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
import schemas.product_schemas as product_schemas
from logger import get_logger

logger = get_logger(__name__)


def get_products(db: Session, skip: int = 0, limit: int = 100):
    try:
        products = db.query(models.Products).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(products)} products")
        return products
    except Exception as e:
        logger.error(f"Failed to retrieve products: {e}")
        raise


def get_product(db: Session, product_code: str):
    try:
        product = db.query(models.Products).filter(
            models.Products.productCode == product_code
        ).first()
        if product:
            logger.info(f"Product {product_code} retrieved successfully")
        else:
            logger.warning(f"Product {product_code} not found")
        return product
    except Exception as e:
        logger.error(f"Failed to retrieve product {product_code}: {e}")
        raise


def create_product(db: Session, product: product_schemas.ProductCreate):
    try:
        db_product = models.Products(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        logger.info(f"Created product {db_product.productCode}")
        return db_product
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating product: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create product: {e}")
        raise


def update_product(db: Session, product_code: str, product_update: product_schemas.ProductUpdate):
    try:
        update_data = product_update.model_dump(exclude_unset=True)
        if not update_data:
            logger.warning(f"No fields provided for update of product {product_code}")
            return None
        db_product = db.query(models.Products).filter(
            models.Products.productCode == product_code
        ).first()
        if db_product is None:
            logger.warning(f"Product {product_code} not found for update")
            return None
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        logger.info(f"Updated product {product_code}")
        return db_product
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update product {product_code}: {e}")
        raise


def delete_product(db: Session, product_code: str):
    try:
        db_product = db.query(models.Products).filter(
            models.Products.productCode == product_code
        ).first()
        if db_product is None:
            logger.warning(f"Product {product_code} not found for deletion")
            return False
        db.delete(db_product)
        db.commit()
        logger.info(f"Deleted product {product_code}")
        return True
    except IntegrityError as e:
        db.rollback()
        logger.error(f"FK constraint error deleting product {product_code}: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete product {product_code}: {e}")
        raise


def get_product_with_orderdetails(db: Session, product_code: str):
    try:
        product = db.query(models.Products).filter(
            models.Products.productCode == product_code
        ).first()
        if product:
            logger.info(f"Retrieved product {product_code} with orderdetails")
        else:
            logger.warning(f"Product {product_code} not found")
        return product
    except Exception as e:
        logger.error(f"Failed to retrieve product {product_code} with orderdetails: {e}")
        raise