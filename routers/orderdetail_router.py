from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
import crud.orderdetail_crud as orderdetail_crud
import schemas.orderdetail_schemas as orderdetail_schemas
from typing import List
from logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=List[orderdetail_schemas.OrderDetailOut])
def list_orderdetails(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /orderdetails - skip={skip} limit={limit}")
        records = orderdetail_crud.get_orderdetailss(db, skip=skip, limit=limit)
        logger.info(f"Returned {len(records)} orderdetail records")
        return records
    except Exception as e:
        logger.error(f"Error listing orderdetails: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# NOTE: Static-segment routes must come before /{orderNumber}/{productCode}
@router.get("/order/{order_number}", response_model=List[orderdetail_schemas.OrderDetailOut])
def get_orderdetails_by_order(order_number: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /orderdetails/order/{order_number}")
        records = orderdetail_crud.get_orderdetails_by_order(db, order_number)
        logger.info(f"Returned {len(records)} orderdetails for order {order_number}")
        return records
    except Exception as e:
        logger.error(f"Error getting orderdetails for order {order_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/product/{product_code}", response_model=List[orderdetail_schemas.OrderDetailOut])
def get_orderdetails_by_product(product_code: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /orderdetails/product/{product_code}")
        records = orderdetail_crud.get_orderdetails_by_product(db, product_code)
        logger.info(f"Returned {len(records)} orderdetails for product {product_code}")
        return records
    except Exception as e:
        logger.error(f"Error getting orderdetails for product {product_code}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{order_number}/{product_code}", response_model=orderdetail_schemas.OrderDetailOut)
def get_orderdetail(order_number: int, product_code: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /orderdetails/{order_number}/{product_code}")
        record = orderdetail_crud.get_orderdetails(db, order_number, product_code)
        if record is None:
            raise HTTPException(status_code=404, detail="OrderDetail not found")
        return record
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting orderdetail ({order_number}, {product_code}): {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/", response_model=orderdetail_schemas.OrderDetailOut, status_code=201)
def create_orderdetail(
    orderdetail: orderdetail_schemas.OrderDetailCreate,
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"POST /orderdetails - order={orderdetail.orderNumber} product={orderdetail.productCode}")
        record = orderdetail_crud.create_orderdetails(db, orderdetail)
        logger.info(f"OrderDetail ({record.orderNumber}, {record.productCode}) created successfully")
        return record
    except IntegrityError as e:
        logger.error(f"FK violation creating orderdetail: {e}")
        raise HTTPException(
            status_code=422,
            detail="Invalid orderNumber or productCode — referenced record does not exist"
        )
    except Exception as e:
        logger.error(f"Error creating orderdetail: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{order_number}/{product_code}", response_model=orderdetail_schemas.OrderDetailOut)
def update_orderdetail(
    order_number: int,
    product_code: str,
    orderdetail_update: orderdetail_schemas.OrderDetailUpdate,
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"PUT /orderdetails/{order_number}/{product_code}")
        record = orderdetail_crud.update_orderdetails(db, order_number, product_code, orderdetail_update)
        if record is None:
            raise HTTPException(status_code=404, detail="OrderDetail not found or no fields provided")
        return record
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating orderdetail ({order_number}, {product_code}): {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{order_number}/{product_code}", status_code=204)
def delete_orderdetail(order_number: int, product_code: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"DELETE /orderdetails/{order_number}/{product_code}")
        success = orderdetail_crud.delete_orderdetails(db, order_number, product_code)
        if not success:
            raise HTTPException(status_code=404, detail="OrderDetail not found")
        return
    except HTTPException:
        raise
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Cannot delete orderdetail — FK constraint violation")
    except Exception as e:
        logger.error(f"Error deleting orderdetail ({order_number}, {product_code}): {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")