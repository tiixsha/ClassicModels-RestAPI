from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
import logging

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/", response_model=list[schemas.CustomerOut])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        customers = crud.get_customers(db, skip=skip, limit=limit)
        logger.info(f"Retrieved {len(customers)} customers")
        return customers
    except Exception as e:
        logger.error(f"Error retrieving customers: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{customer_number}", response_model=schemas.CustomerOut)
def read_customer(customer_number: int, db: Session = Depends(get_db)):
    try:
        customer = crud.get_customer(db, customer_number=customer_number)
        if customer is None:
            logger.warning(f"Customer with ID {customer_number} not found")
            raise HTTPException(status_code=404, detail="Customer not found")
        logger.info(f"Customer with ID {customer_number} retrieved successfully")
        return customer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving customer {customer_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/", response_model=schemas.CustomerOut, status_code=201)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    try:
        db_customer = crud.create_customer(db, customer=customer)
        logger.info(f"Customer with ID {db_customer.customerNumber} created successfully")
        return db_customer
    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{customer_number}", response_model=schemas.CustomerOut)
def update_customer(customer_number: int, customer_update: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    try:
        db_customer = crud.update_customer(db, customer_number=customer_number, customer_update=customer_update)
        if db_customer is None:
            logger.warning(f"Customer with ID {customer_number} not found for update")
            raise HTTPException(status_code=404, detail="Customer not found")
        logger.info(f"Customer with ID {customer_number} updated successfully")
        return db_customer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating customer {customer_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{customer_number}", status_code=204)
def delete_customer(customer_number: int, db: Session = Depends(get_db)):
    try:
        success = crud.delete_customer(db, customer_number=customer_number)
        if not success:
            logger.warning(f"Customer with ID {customer_number} not found for deletion")
            raise HTTPException(status_code=404, detail="Customer not found")
        logger.info(f"Customer with ID {customer_number} deleted successfully")
        return
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting customer {customer_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{customer_number}/orders", response_model=list[schemas.OrderOut])
def read_customer_orders(customer_number: int, db: Session = Depends(get_db)):
    try:
        customer = crud.get_customer(db, customer_number=customer_number)
        if customer is None:
            logger.warning(f"Customer with ID {customer_number} not found")
            raise HTTPException(status_code=404, detail="Customer not found")
        orders = crud.get_customer_orders(db, customer_number=customer_number)
        logger.info(f"Retrieved {len(orders)} orders for customer ID {customer_number}")
        return orders
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving orders for customer {customer_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{customer_number}/payments", response_model=list[schemas.PaymentOut])
def read_customer_payments(customer_number: int, db: Session = Depends(get_db)):
    try:
        customer = crud.get_customer(db, customer_number=customer_number)
        if customer is None:
            logger.warning(f"Customer with ID {customer_number} not found")
            raise HTTPException(status_code=404, detail="Customer not found")
        payments = crud.get_customer_payments(db, customer_number=customer_number)
        logger.info(f"Retrieved {len(payments)} payments for customer ID {customer_number}")
        return payments
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving payments for customer {customer_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")