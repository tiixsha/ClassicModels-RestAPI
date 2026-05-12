from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
import crud.product_crud as product_crud
import schemas.product_schemas as product_schemas
from typing import List
from logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=List[product_schemas.ProductOut])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /products - skip={skip} limit={limit}")
        products = product_crud.get_products(db, skip=skip, limit=limit)
        logger.info(f"Returned {len(products)} products")
        return products
    except Exception as e:
        logger.error(f"Error listing products: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/count")
def get_products_count(db: Session = Depends(get_db)):
    try:
        logger.info("GET /products/count")
        count = db.query(product_crud.models.Products).count()
        return {"count": count}
    except Exception as e:
        logger.error(f"Error getting products count: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{product_code}/orderdetails", response_model=product_schemas.ProductOut)
def get_product_orderdetails(product_code: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /products/{product_code}/orderdetails")
        product = product_crud.get_product_with_orderdetails(db, product_code)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting orderdetails for product {product_code}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{product_code}", response_model=product_schemas.ProductOut)
def get_product(product_code: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /products/{product_code}")
        product = product_crud.get_product(db, product_code)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting product {product_code}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/", response_model=product_schemas.ProductOut, status_code=201)
def create_product(product: product_schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"POST /products - creating {product.productCode}")
        db_product = product_crud.create_product(db, product)
        logger.info(f"Product {db_product.productCode} created successfully")
        return db_product
    except IntegrityError as e:
        logger.error(f"FK violation creating product: {e}")
        raise HTTPException(status_code=422, detail="Invalid productLine — does not exist in productlines table")
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{product_code}", response_model=product_schemas.ProductOut)
def update_product(product_code: str, product_update: product_schemas.ProductUpdate, db: Session = Depends(get_db)):
    try:
        logger.info(f"PUT /products/{product_code}")
        db_product = product_crud.update_product(db, product_code, product_update)
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return db_product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product {product_code}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{product_code}", status_code=204)
def delete_product(product_code: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"DELETE /products/{product_code}")
        success = product_crud.delete_product(db, product_code)
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        return
    except HTTPException:
        raise
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Cannot delete product — it is referenced by existing order details")
    except Exception as e:
        logger.error(f"Error deleting product {product_code}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")