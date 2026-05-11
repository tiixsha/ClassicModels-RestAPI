from sqlalchemy.orm import Session
import models, schemas
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    try:
        customers = db.query(models.Customers).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(customers)} customers from the database")
        return customers
    except Exception as e:
        logger.error(f"Failed to retrieve customers: {e}")
        raise


def get_customer(db: Session, customer_number: int):
    try:
        customer = db.query(models.Customers).filter(
            models.Customers.customerNumber == customer_number
        ).first()
        if customer:
            logger.info(f"Customer with ID {customer_number} retrieved successfully")
        else:
            logger.warning(f"Customer with ID {customer_number} not found")
        return customer
    except Exception as e:
        logger.error(f"Failed to retrieve customer {customer_number}: {e}")
        raise


def create_customer(db: Session, customer: schemas.CustomerCreate):
    try:
        db_customer = models.Customers(**customer.model_dump())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        logger.info(f"Created new customer with ID {db_customer.customerNumber}")
        return db_customer
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create customer: {e}")
        raise


def update_customer(db: Session, customer_number: int, customer_update: schemas.CustomerUpdate):
    try:
        update_data = customer_update.model_dump(exclude_unset=True)
        if not update_data:
            logger.warning(f"No fields provided for update of customer {customer_number}")
            return None
        db_customer = db.query(models.Customers).filter(
            models.Customers.customerNumber == customer_number
        ).first()
        if db_customer is None:
            logger.warning(f"Customer with ID {customer_number} not found for update")
            return None
        for key, value in update_data.items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
        logger.info(f"Updated customer with ID {customer_number}")
        return db_customer
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update customer {customer_number}: {e}")
        raise


def delete_customer(db: Session, customer_number: int):
    try:
        db_customer = db.query(models.Customers).filter(
            models.Customers.customerNumber == customer_number
        ).first()
        if db_customer is None:
            logger.warning(f"Customer with ID {customer_number} not found for deletion")
            return False
        db.delete(db_customer)
        db.commit()
        logger.info(f"Deleted customer with ID {customer_number}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete customer {customer_number}: {e}")
        raise


def get_customer_orders(db: Session, customer_number: int):
    try:
        orders = db.query(models.Orders).filter(
            models.Orders.customerNumber == customer_number
        ).all()
        logger.info(f"Retrieved {len(orders)} orders for customer ID {customer_number}")
        return orders
    except Exception as e:
        logger.error(f"Failed to retrieve orders for customer {customer_number}: {e}")
        raise


def get_customer_payments(db: Session, customer_number: int):
    try:
        payments = db.query(models.Payments).filter(
            models.Payments.customerNumber == customer_number
        ).all()
        logger.info(f"Retrieved {len(payments)} payments for customer ID {customer_number}")
        return payments
    except Exception as e:
        logger.error(f"Failed to retrieve payments for customer {customer_number}: {e}")
        raise