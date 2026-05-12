from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
import crud.office_crud as office_crud
import schemas.office_schemas as office_schemas
from typing import List
from logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=List[office_schemas.OfficeOut])
def list_offices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /offices - skip={skip} limit={limit}")
        offices = office_crud.get_officess(db, skip=skip, limit=limit)
        logger.info(f"Returned {len(offices)} offices")
        return offices
    except Exception as e:
        logger.error(f"Error listing offices: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{office_code}/employees", response_model=office_schemas.OfficeOut)
def get_office_with_employees(office_code: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /offices/{office_code}/employees")
        office = office_crud.get_offices_with_employees(db, office_code)
        if office is None:
            raise HTTPException(status_code=404, detail="Office not found")
        return office
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting employees for office '{office_code}': {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{office_code}", response_model=office_schemas.OfficeOut)
def get_office(office_code: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /offices/{office_code}")
        office = office_crud.get_offices(db, office_code)
        if office is None:
            raise HTTPException(status_code=404, detail="Office not found")
        return office
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting office '{office_code}': {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/", response_model=office_schemas.OfficeOut, status_code=201)
def create_office(office: office_schemas.OfficeCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"POST /offices - creating '{office.officeCode}'")
        db_office = office_crud.create_offices(db, office)
        logger.info(f"Office '{db_office.officeCode}' created successfully")
        return db_office
    except IntegrityError:
        logger.error(f"Duplicate office '{office.officeCode}'")
        raise HTTPException(status_code=409, detail="Office already exists")
    except Exception as e:
        logger.error(f"Error creating office: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{office_code}", response_model=office_schemas.OfficeOut)
def update_office(office_code: str, office_update: office_schemas.OfficeUpdate, db: Session = Depends(get_db)):
    try:
        logger.info(f"PUT /offices/{office_code}")
        db_office = office_crud.update_offices(db, office_code, office_update)
        if db_office is None:
            raise HTTPException(status_code=404, detail="Office not found")
        return db_office
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating office '{office_code}': {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{office_code}", status_code=204)
def delete_office(office_code: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"DELETE /offices/{office_code}")
        success = office_crud.delete_offices(db, office_code)
        if not success:
            raise HTTPException(status_code=404, detail="Office not found")
        return
    except HTTPException:
        raise
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Cannot delete office — employees still reference it")
    except Exception as e:
        logger.error(f"Error deleting office '{office_code}': {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")