from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
import schemas.productline_schemas as productline_schemas
from logger import get_logger

logger = get_logger(__name__)


def get_productliness(db: Session, skip: int = 0, limit: int = 100):
    try:
        productlines = db.query(models.ProductLines).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(productlines)} product lines")
        return productlines
    except Exception as e:
        logger.error(f"Failed to retrieve product lines: {e}")
        raise


def get_productlines(db: Session, product_line: str):
    try:
        productline = db.query(models.ProductLines).filter(
            models.ProductLines.productLine == product_line
        ).first()
        if productline:
            logger.info(f"ProductLine '{product_line}' retrieved successfully")
        else:
            logger.warning(f"ProductLine '{product_line}' not found")
        return productline
    except Exception as e:
        logger.error(f"Failed to retrieve product line '{product_line}': {e}")
        raise


def create_productlines(db: Session, productline: productline_schemas.ProductLineCreate):
    try:
        db_productline = models.ProductLines(**productline.model_dump())
        db.add(db_productline)
        db.commit()
        db.refresh(db_productline)
        logger.info(f"Created product line '{db_productline.productLine}'")
        return db_productline
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating product line: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create product line: {e}")
        raise


def update_productlines(db: Session, product_line: str, productline_update: productline_schemas.ProductLineUpdate):
    try:
        update_data = productline_update.model_dump(exclude_unset=True)
        if not update_data:
            logger.warning(f"No fields provided for update of product line '{product_line}'")
            return None
        db_productline = db.query(models.ProductLines).filter(
            models.ProductLines.productLine == product_line
        ).first()
        if db_productline is None:
            logger.warning(f"ProductLine '{product_line}' not found for update")
            return None
        for key, value in update_data.items():
            setattr(db_productline, key, value)
        db.commit()
        db.refresh(db_productline)
        logger.info(f"Updated product line '{product_line}'")
        return db_productline
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update product line '{product_line}': {e}")
        raise


def delete_productlines(db: Session, product_line: str):
    try:
        db_productline = db.query(models.ProductLines).filter(
            models.ProductLines.productLine == product_line
        ).first()
        if db_productline is None:
            logger.warning(f"ProductLine '{product_line}' not found for deletion")
            return False
        db.delete(db_productline)
        db.commit()
        logger.info(f"Deleted product line '{product_line}'")
        return True
    except IntegrityError as e:
        db.rollback()
        logger.error(f"FK constraint error deleting product line '{product_line}': {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete product line '{product_line}': {e}")
        raise


def get_productlines_with_products(db: Session, product_line: str):
    try:
        productline = db.query(models.ProductLines).filter(
            models.ProductLines.productLine == product_line
        ).first()
        if productline:
            logger.info(f"Retrieved product line '{product_line}' with {len(productline.products)} products")
        else:
            logger.warning(f"ProductLine '{product_line}' not found")
        return productline
    except Exception as e:
        logger.error(f"Failed to retrieve product line '{product_line}' with products: {e}")
        raise