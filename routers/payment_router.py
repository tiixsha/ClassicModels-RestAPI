from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
import crud.payment_crud as payment_crud
import schemas.payment_schemas as payment_schemas
from typing import List
from logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=List[payment_schemas.PaymentOut])
def list_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /payments - skip={skip} limit={limit}")
        records = payment_crud.get_paymentss(db, skip=skip, limit=limit)
        logger.info(f"Returned {len(records)} payment records")
        return records
    except Exception as e:
        logger.error(f"Error listing payments: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# NOTE: Static-segment route must come before /{customerNumber}/{checkNumber}
@router.get("/customer/{customer_number}", response_model=List[payment_schemas.PaymentOut])
def get_payments_by_customer(customer_number: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /payments/customer/{customer_number}")
        records = payment_crud.get_payments_by_customer(db, customer_number)
        logger.info(f"Returned {len(records)} payments for customer {customer_number}")
        return records  # Returns [] if none — never 404
    except Exception as e:
        logger.error(f"Error getting payments for customer {customer_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{customer_number}/{check_number}", response_model=payment_schemas.PaymentOut)
def get_payment(customer_number: int, check_number: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /payments/{customer_number}/{check_number}")
        record = payment_crud.get_payments(db, customer_number, check_number)
        if record is None:
            raise HTTPException(status_code=404, detail="Payment not found")
        return record
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting payment ({customer_number}, {check_number}): {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/", response_model=payment_schemas.PaymentOut, status_code=201)
def create_payment(payment: payment_schemas.PaymentCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"POST /payments - customer={payment.customerNumber} check={payment.checkNumber}")
        record = payment_crud.create_payments(db, payment)
        logger.info(f"Payment ({record.customerNumber}, {record.checkNumber}) created successfully")
        return record
    except IntegrityError as e:
        logger.error(f"FK violation creating payment: {e}")
        raise HTTPException(
            status_code=422,
            detail="Invalid customerNumber — customer does not exist"
        )
    except Exception as e:
        logger.error(f"Error creating payment: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{customer_number}/{check_number}", response_model=payment_schemas.PaymentOut)
def update_payment(
    customer_number: int,
    check_number: str,
    payment_update: payment_schemas.PaymentUpdate,
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"PUT /payments/{customer_number}/{check_number}")
        record = payment_crud.update_payments(db, customer_number, check_number, payment_update)
        if record is None:
            raise HTTPException(status_code=404, detail="Payment not found or no fields provided")
        return record
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating payment ({customer_number}, {check_number}): {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{customer_number}/{check_number}", status_code=204)
def delete_payment(customer_number: int, check_number: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"DELETE /payments/{customer_number}/{check_number}")
        success = payment_crud.delete_payments(db, customer_number, check_number)
        if not success:
            raise HTTPException(status_code=404, detail="Payment not found")
        return
    except HTTPException:
        raise
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Cannot delete payment — FK constraint violation")
    except Exception as e:
        logger.error(f"Error deleting payment ({customer_number}, {check_number}): {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")