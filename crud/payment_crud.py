
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
import schemas.payment_schemas as payment_schemas
from logger import get_logger
 
logger = get_logger(__name__)
 
 
def get_paymentss(db: Session, skip: int = 0, limit: int = 100):
    try:
        records = db.query(models.Payments).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(records)} payment records")
        return records
    except Exception as e:
        logger.error(f"Failed to retrieve payments: {e}")
        raise
 
 
def get_payments(db: Session, customer_number: int, check_number: str):
    try:
        record = db.query(models.Payments).filter(
            models.Payments.customerNumber == customer_number,
            models.Payments.checkNumber == check_number
        ).first()
        if record:
            logger.info(f"Payment ({customer_number}, {check_number}) retrieved successfully")
        else:
            logger.warning(f"Payment ({customer_number}, {check_number}) not found")
        return record
    except Exception as e:
        logger.error(f"Failed to retrieve payment ({customer_number}, {check_number}): {e}")
        raise
 
 
def create_payments(db: Session, payment: payment_schemas.PaymentCreate):
    try:
        db_record = models.Payments(**payment.model_dump())
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        logger.info(f"Created payment ({db_record.customerNumber}, {db_record.checkNumber})")
        return db_record
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating payment: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create payment: {e}")
        raise
 
 
def update_payments(
    db: Session,
    customer_number: int,
    check_number: str,
    payment_update: payment_schemas.PaymentUpdate
):
    try:
        update_data = payment_update.model_dump(exclude_unset=True)
        if not update_data:
            logger.warning(f"No fields provided for update of payment ({customer_number}, {check_number})")
            return None
        db_record = db.query(models.Payments).filter(
            models.Payments.customerNumber == customer_number,
            models.Payments.checkNumber == check_number
        ).first()
        if db_record is None:
            logger.warning(f"Payment ({customer_number}, {check_number}) not found for update")
            return None
        for key, value in update_data.items():
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
        logger.info(f"Updated payment ({customer_number}, {check_number})")
        return db_record
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update payment ({customer_number}, {check_number}): {e}")
        raise
 
 
def delete_payments(db: Session, customer_number: int, check_number: str):
    try:
        db_record = db.query(models.Payments).filter(
            models.Payments.customerNumber == customer_number,
            models.Payments.checkNumber == check_number
        ).first()
        if db_record is None:
            logger.warning(f"Payment ({customer_number}, {check_number}) not found for deletion")
            return False
        db.delete(db_record)
        db.commit()
        logger.info(f"Deleted payment ({customer_number}, {check_number})")
        return True
    except IntegrityError as e:
        db.rollback()
        logger.error(f"FK constraint error deleting payment ({customer_number}, {check_number}): {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete payment ({customer_number}, {check_number}): {e}")
        raise
 
 
def get_payments_by_customer(db: Session, customer_number: int):
    try:
        records = db.query(models.Payments).filter(
            models.Payments.customerNumber == customer_number
        ).all()
        logger.info(f"Retrieved {len(records)} payments for customer {customer_number}")
        return records
    except Exception as e:
        logger.error(f"Failed to retrieve payments for customer {customer_number}: {e}")
        raise
 
