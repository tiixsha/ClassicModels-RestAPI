from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
import schemas.office_schemas as office_schemas
from logger import get_logger

logger = get_logger(__name__)


def get_officess(db: Session, skip: int = 0, limit: int = 100):
    try:
        offices = db.query(models.Offices).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(offices)} offices")
        return offices
    except Exception as e:
        logger.error(f"Failed to retrieve offices: {e}")
        raise


def get_offices(db: Session, office_code: str):
    try:
        office = db.query(models.Offices).filter(
            models.Offices.officeCode == office_code
        ).first()
        if office:
            logger.info(f"Office '{office_code}' retrieved successfully")
        else:
            logger.warning(f"Office '{office_code}' not found")
        return office
    except Exception as e:
        logger.error(f"Failed to retrieve office '{office_code}': {e}")
        raise


def create_offices(db: Session, office: office_schemas.OfficeCreate):
    try:
        db_office = models.Offices(**office.model_dump())
        db.add(db_office)
        db.commit()
        db.refresh(db_office)
        logger.info(f"Created office '{db_office.officeCode}'")
        return db_office
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating office: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create office: {e}")
        raise


def update_offices(db: Session, office_code: str, office_update: office_schemas.OfficeUpdate):
    try:
        update_data = office_update.model_dump(exclude_unset=True)
        if not update_data:
            logger.warning(f"No fields provided for update of office '{office_code}'")
            return None
        db_office = db.query(models.Offices).filter(
            models.Offices.officeCode == office_code
        ).first()
        if db_office is None:
            logger.warning(f"Office '{office_code}' not found for update")
            return None
        for key, value in update_data.items():
            setattr(db_office, key, value)
        db.commit()
        db.refresh(db_office)
        logger.info(f"Updated office '{office_code}'")
        return db_office
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update office '{office_code}': {e}")
        raise


def delete_offices(db: Session, office_code: str):
    try:
        db_office = db.query(models.Offices).filter(
            models.Offices.officeCode == office_code
        ).first()
        if db_office is None:
            logger.warning(f"Office '{office_code}' not found for deletion")
            return False
        db.delete(db_office)
        db.commit()
        logger.info(f"Deleted office '{office_code}'")
        return True
    except IntegrityError as e:
        db.rollback()
        logger.error(f"FK constraint error deleting office '{office_code}': {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete office '{office_code}': {e}")
        raise


def get_offices_with_employees(db: Session, office_code: str):
    try:
        office = db.query(models.Offices).filter(
            models.Offices.officeCode == office_code
        ).first()
        if office:
            logger.info(f"Retrieved office '{office_code}' with {len(office.employees)} employees")
        else:
            logger.warning(f"Office '{office_code}' not found")
        return office
    except Exception as e:
        logger.error(f"Failed to retrieve office '{office_code}' with employees: {e}")
        raise