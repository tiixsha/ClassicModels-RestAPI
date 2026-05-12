from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud.customer_crud as customer_crud
import asyncio
from logger import get_logger
import time

router = APIRouter(tags=["dashboard"])

logger = get_logger(__name__)


@router.get("/customers/count")
async def get_customers_count(db: Session = Depends(get_db)):
    try:
        logger.info("Incoming request: GET /customers/count")
        count = await customer_crud.get_customers_count(db)
        logger.info(f"Response: customers count = {count}")
        return {"count": count}
    except Exception as e:
        logger.error(f"Error on /customers/count: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/orders/count")
async def get_orders_count(db: Session = Depends(get_db)):
    try:
        logger.info("Incoming request: GET /orders/count")
        count = await customer_crud.get_orders_count(db)
        logger.info(f"Response: orders count = {count}")
        return {"count": count}
    except Exception as e:
        logger.error(f"Error on /orders/count: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/products/count")
async def get_products_count(db: Session = Depends(get_db)):
    try:
        logger.info("Incoming request: GET /products/count")
        count = await customer_crud.get_products_count(db)
        logger.info(f"Response: products count = {count}")
        return {"count": count}
    except Exception as e:
        logger.error(f"Error on /products/count: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/employees/count")
async def get_employees_count(db: Session = Depends(get_db)):
    try:
        logger.info("Incoming request: GET /employees/count")
        count = await customer_crud.get_employees_count(db)
        logger.info(f"Response: employees count = {count}")
        return {"count": count}
    except Exception as e:
        logger.error(f"Error on /employees/count: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/offices/count")
async def get_offices_count(db: Session = Depends(get_db)):
    try:
        logger.info("Incoming request: GET /offices/count")
        count = await customer_crud.get_offices_count(db)
        logger.info(f"Response: offices count = {count}")
        return {"count": count}
    except Exception as e:
        logger.error(f"Error on /offices/count: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/payments/count")
async def get_payments_count(db: Session = Depends(get_db)):
    try:
        logger.info("Incoming request: GET /payments/count")
        count = await customer_crud.get_payments_count(db)
        logger.info(f"Response: payments count = {count}")
        return {"count": count}
    except Exception as e:
        logger.error(f"Error on /payments/count: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/orderdetails/count")
async def get_orderdetails_count(db: Session = Depends(get_db)):
    try:
        logger.info("Incoming request: GET /orderdetails/count")
        count = await customer_crud.get_orderdetails_count(db)
        logger.info(f"Response: orderdetails count = {count}")
        return {"count": count}
    except Exception as e:
        logger.error(f"Error on /orderdetails/count: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/productlines/count")
async def get_productlines_count(db: Session = Depends(get_db)):
    try:
        logger.info("Incoming request: GET /productlines/count")
        count = await customer_crud.get_productlines_count(db)
        logger.info(f"Response: productlines count = {count}")
        return {"count": count}
    except Exception as e:
        logger.error(f"Error on /productlines/count: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/overall_counts")
async def get_overall_counts(db: Session = Depends(get_db)):
    try:
        logger.info("Incoming request: GET /overall_counts")
        logger.info("Starting all 8 count queries simultaneously with asyncio.gather()")
        start_time = time.time()
        (   customers,
            orders,
            products,
            employees,
            offices,
            payments,
            orderdetails,
            productlines) = await asyncio.gather(
            customer_crud.get_customers_count(db),
            customer_crud.get_orders_count(db),
            customer_crud.get_products_count(db),
            customer_crud.get_employees_count(db),
            customer_crud.get_offices_count(db),
            customer_crud.get_payments_count(db),
            customer_crud.get_orderdetails_count(db),
            customer_crud.get_productlines_count(db),)
        elapsed = round(time.time() - start_time, 4)
        logger.info(f"asyncio.gather() completed — all 8 counts retrieved")
        logger.info(f"Total response time: {elapsed}s")
        return {"customers": customers,
            "orders": orders,
            "products": products,
            "employees": employees,
            "offices": offices,
            "payments": payments,
            "orderdetails": orderdetails,
            "productlines": productlines}
    except Exception as e:
        logger.error(f"Error on /overall_counts: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")