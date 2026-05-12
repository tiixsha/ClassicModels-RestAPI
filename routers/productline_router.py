from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
import crud.productline_crud as productline_crud
import schemas.productline_schemas as productline_schemas
from typing import List
from logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=List[productline_schemas.ProductLineOut])
def list_productlines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /productlines - skip={skip} limit={limit}")
        productlines = productline_crud.get_productliness(db, skip=skip, limit=limit)
        logger.info(f"Returned {len(productlines)} product lines")
        return productlines
    except Exception as e:
        logger.error(f"Error listing product lines: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{product_line}/products", response_model=productline_schemas.ProductLineOut)
def get_productline_with_products(product_line: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /productlines/{product_line}/products")
        productline = productline_crud.get_productlines_with_products(db, product_line)
        if productline is None:
            raise HTTPException(status_code=404, detail="Product line not found")
        return productline
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting products for product line '{product_line}': {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{product_line}", response_model=productline_schemas.ProductLineOut)
def get_productline(product_line: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /productlines/{product_line}")
        productline = productline_crud.get_productlines(db, product_line)
        if productline is None:
            raise HTTPException(status_code=404, detail="Product line not found")
        return productline
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting product line '{product_line}': {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/", response_model=productline_schemas.ProductLineOut, status_code=201)
def create_productline(productline: productline_schemas.ProductLineCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"POST /productlines - creating '{productline.productLine}'")
        db_productline = productline_crud.create_productlines(db, productline)
        logger.info(f"Product line '{db_productline.productLine}' created successfully")
        return db_productline
    except IntegrityError:
        logger.error(f"Duplicate product line '{productline.productLine}'")
        raise HTTPException(status_code=409, detail="Product line already exists")
    except Exception as e:
        logger.error(f"Error creating product line: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{product_line}", response_model=productline_schemas.ProductLineOut)
def update_productline(product_line: str, productline_update: productline_schemas.ProductLineUpdate, db: Session = Depends(get_db)):
    try:
        logger.info(f"PUT /productlines/{product_line}")
        db_productline = productline_crud.update_productlines(db, product_line, productline_update)
        if db_productline is None:
            raise HTTPException(status_code=404, detail="Product line not found")
        return db_productline
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product line '{product_line}': {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{product_line}", status_code=204)
def delete_productline(product_line: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"DELETE /productlines/{product_line}")
        success = productline_crud.delete_productlines(db, product_line)
        if not success:
            raise HTTPException(status_code=404, detail="Product line not found")
        return
    except HTTPException:
        raise
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Cannot delete product line — products still reference it")
    except Exception as e:
        logger.error(f"Error deleting product line '{product_line}': {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")