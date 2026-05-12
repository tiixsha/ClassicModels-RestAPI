from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
import schemas.order_schemas as order_schemas
from logger import get_logger

logger = get_logger(__name__)


def get_orderss(db: Session, skip: int = 0, limit: int = 100):
    try:
        orders = db.query(models.Orders).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(orders)} orders")
        return orders
    except Exception as e:
        logger.error(f"Failed to retrieve orders: {e}")
        raise


def get_orders(db: Session, order_number: int):
    try:
        order = db.query(models.Orders).filter(
            models.Orders.orderNumber == order_number
        ).first()
        if order:
            logger.info(f"Order {order_number} retrieved successfully")
        else:
            logger.warning(f"Order {order_number} not found")
        return order
    except Exception as e:
        logger.error(f"Failed to retrieve order {order_number}: {e}")
        raise


def create_orders(db: Session, order: order_schemas.OrderCreate):
    try:
        db_order = models.Orders(**order.model_dump())
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        logger.info(f"Created order {db_order.orderNumber}")
        return db_order
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating order: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create order: {e}")
        raise


def update_orders(db: Session, order_number: int, order_update: order_schemas.OrderUpdate):
    try:
        update_data = order_update.model_dump(exclude_unset=True)
        if not update_data:
            logger.warning(f"No fields provided for update of order {order_number}")
            return None
        db_order = db.query(models.Orders).filter(
            models.Orders.orderNumber == order_number
        ).first()
        if db_order is None:
            logger.warning(f"Order {order_number} not found for update")
            return None
        for key, value in update_data.items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
        logger.info(f"Updated order {order_number}")
        return db_order
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update order {order_number}: {e}")
        raise


def delete_orders(db: Session, order_number: int):
    try:
        db_order = db.query(models.Orders).filter(
            models.Orders.orderNumber == order_number
        ).first()
        if db_order is None:
            logger.warning(f"Order {order_number} not found for deletion")
            return False
        db.delete(db_order)
        db.commit()
        logger.info(f"Deleted order {order_number}")
        return True
    except IntegrityError as e:
        db.rollback()
        logger.error(f"FK constraint error deleting order {order_number}: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete order {order_number}: {e}")
        raise


def get_orders_with_orderdetails(db: Session, order_number: int):
    try:
        order = db.query(models.Orders).filter(
            models.Orders.orderNumber == order_number
        ).first()
        if order:
            logger.info(f"Retrieved order {order_number} with {len(order.orderdetails)} orderdetails")
        else:
            logger.warning(f"Order {order_number} not found")
        return order
    except Exception as e:
        logger.error(f"Failed to retrieve order {order_number} with orderdetails: {e}")
        raise


def get_orders_by_customer(db: Session, customer_number: int):
    try:
        orders = db.query(models.Orders).filter(
            models.Orders.customerNumber == customer_number
        ).all()
        logger.info(f"Retrieved {len(orders)} orders for customer {customer_number}")
        return orders
    except Exception as e:
        logger.error(f"Failed to retrieve orders for customer {customer_number}: {e}")
        raise