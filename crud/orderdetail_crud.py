from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
import schemas.orderdetail_schemas as orderdetail_schemas
from logger import get_logger

logger = get_logger(__name__)


def get_orderdetailss(db: Session, skip: int = 0, limit: int = 100):
    try:
        records = db.query(models.OrderDetails).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(records)} order detail records")
        return records
    except Exception as e:
        logger.error(f"Failed to retrieve order details: {e}")
        raise


def get_orderdetails(db: Session, order_number: int, product_code: str):
    try:
        record = db.query(models.OrderDetails).filter(
            models.OrderDetails.orderNumber == order_number,
            models.OrderDetails.productCode == product_code
        ).first()
        if record:
            logger.info(f"OrderDetail ({order_number}, {product_code}) retrieved successfully")
        else:
            logger.warning(f"OrderDetail ({order_number}, {product_code}) not found")
        return record
    except Exception as e:
        logger.error(f"Failed to retrieve orderdetail ({order_number}, {product_code}): {e}")
        raise


def create_orderdetails(db: Session, orderdetail: orderdetail_schemas.OrderDetailCreate):
    try:
        db_record = models.OrderDetails(**orderdetail.model_dump())
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        logger.info(f"Created orderdetail ({db_record.orderNumber}, {db_record.productCode})")
        return db_record
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating orderdetail: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create orderdetail: {e}")
        raise


def update_orderdetails(
    db: Session,
    order_number: int,
    product_code: str,
    orderdetail_update: orderdetail_schemas.OrderDetailUpdate
):
    try:
        update_data = orderdetail_update.model_dump(exclude_unset=True)
        if not update_data:
            logger.warning(f"No fields provided for update of orderdetail ({order_number}, {product_code})")
            return None
        db_record = db.query(models.OrderDetails).filter(
            models.OrderDetails.orderNumber == order_number,
            models.OrderDetails.productCode == product_code
        ).first()
        if db_record is None:
            logger.warning(f"OrderDetail ({order_number}, {product_code}) not found for update")
            return None
        for key, value in update_data.items():
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
        logger.info(f"Updated orderdetail ({order_number}, {product_code})")
        return db_record
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update orderdetail ({order_number}, {product_code}): {e}")
        raise


def delete_orderdetails(db: Session, order_number: int, product_code: str):
    try:
        db_record = db.query(models.OrderDetails).filter(
            models.OrderDetails.orderNumber == order_number,
            models.OrderDetails.productCode == product_code
        ).first()
        if db_record is None:
            logger.warning(f"OrderDetail ({order_number}, {product_code}) not found for deletion")
            return False
        db.delete(db_record)
        db.commit()
        logger.info(f"Deleted orderdetail ({order_number}, {product_code})")
        return True
    except IntegrityError as e:
        db.rollback()
        logger.error(f"FK constraint error deleting orderdetail ({order_number}, {product_code}): {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete orderdetail ({order_number}, {product_code}): {e}")
        raise


def get_orderdetails_by_order(db: Session, order_number: int):
    try:
        records = db.query(models.OrderDetails).filter(
            models.OrderDetails.orderNumber == order_number
        ).all()
        logger.info(f"Retrieved {len(records)} orderdetails for order {order_number}")
        return records
    except Exception as e:
        logger.error(f"Failed to retrieve orderdetails for order {order_number}: {e}")
        raise


def get_orderdetails_by_product(db: Session, product_code: str):
    try:
        records = db.query(models.OrderDetails).filter(
            models.OrderDetails.productCode == product_code
        ).all()
        logger.info(f"Retrieved {len(records)} orderdetails for product {product_code}")
        return records
    except Exception as e:
        logger.error(f"Failed to retrieve orderdetails for product {product_code}: {e}")
        raise