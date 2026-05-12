from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
import crud.order_crud as order_crud
import schemas.order_schemas as order_schemas
from typing import List
from logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=List[order_schemas.OrderOut])
def list_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /orders - skip={skip} limit={limit}")
        orders = order_crud.get_orderss(db, skip=skip, limit=limit)
        logger.info(f"Returned {len(orders)} orders")
        return orders
    except Exception as e:
        logger.error(f"Error listing orders: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/customer/{customer_number}", response_model=List[order_schemas.OrderOut])
def get_orders_by_customer(customer_number: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /orders/customer/{customer_number}")
        orders = order_crud.get_orders_by_customer(db, customer_number)
        logger.info(f"Returned {len(orders)} orders for customer {customer_number}")
        return orders
    except Exception as e:
        logger.error(f"Error getting orders for customer {customer_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{order_number}/orderdetails", response_model=order_schemas.OrderOut)
def get_order_with_orderdetails(order_number: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /orders/{order_number}/orderdetails")
        order = order_crud.get_orders_with_orderdetails(db, order_number)
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting orderdetails for order {order_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{order_number}", response_model=order_schemas.OrderOut)
def get_order(order_number: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /orders/{order_number}")
        order = order_crud.get_orders(db, order_number)
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting order {order_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/", response_model=order_schemas.OrderOut, status_code=201)
def create_order(order: order_schemas.OrderCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"POST /orders - creating order {order.orderNumber}")
        db_order = order_crud.create_orders(db, order)
        logger.info(f"Order {db_order.orderNumber} created successfully")
        return db_order
    except IntegrityError as e:
        logger.error(f"FK violation creating order: {e}")
        raise HTTPException(status_code=422, detail="Invalid customerNumber — customer does not exist")
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{order_number}", response_model=order_schemas.OrderOut)
def update_order(order_number: int, order_update: order_schemas.OrderUpdate, db: Session = Depends(get_db)):
    try:
        logger.info(f"PUT /orders/{order_number}")
        db_order = order_crud.update_orders(db, order_number, order_update)
        if db_order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return db_order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating order {order_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{order_number}", status_code=204)
def delete_order(order_number: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"DELETE /orders/{order_number}")
        success = order_crud.delete_orders(db, order_number)
        if not success:
            raise HTTPException(status_code=404, detail="Order not found")
        return
    except HTTPException:
        raise
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Cannot delete order — orderdetails still reference it")
    except Exception as e:
        logger.error(f"Error deleting order {order_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")