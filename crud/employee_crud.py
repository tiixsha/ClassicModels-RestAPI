from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
import schemas.employee_schemas as employee_schemas
from logger import get_logger

logger = get_logger(__name__)


def get_employeess(db: Session, skip: int = 0, limit: int = 100):
    try:
        employees = db.query(models.Employees).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(employees)} employees")
        return employees
    except Exception as e:
        logger.error(f"Failed to retrieve employees: {e}")
        raise


def get_employees(db: Session, employee_number: int):
    try:
        employee = db.query(models.Employees).filter(
            models.Employees.employeeNumber == employee_number
        ).first()
        if employee:
            logger.info(f"Employee {employee_number} retrieved successfully")
        else:
            logger.warning(f"Employee {employee_number} not found")
        return employee
    except Exception as e:
        logger.error(f"Failed to retrieve employee {employee_number}: {e}")
        raise


def create_employees(db: Session, employee: employee_schemas.EmployeeCreate):
    try:
        db_employee = models.Employees(**employee.model_dump())
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        logger.info(f"Created employee {db_employee.employeeNumber}")
        return db_employee
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating employee: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create employee: {e}")
        raise


def update_employees(db: Session, employee_number: int, employee_update: employee_schemas.EmployeeUpdate):
    try:
        update_data = employee_update.model_dump(exclude_unset=True)
        if not update_data:
            logger.warning(f"No fields provided for update of employee {employee_number}")
            return None
        db_employee = db.query(models.Employees).filter(
            models.Employees.employeeNumber == employee_number
        ).first()
        if db_employee is None:
            logger.warning(f"Employee {employee_number} not found for update")
            return None
        for key, value in update_data.items():
            setattr(db_employee, key, value)
        db.commit()
        db.refresh(db_employee)
        logger.info(f"Updated employee {employee_number}")
        return db_employee
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update employee {employee_number}: {e}")
        raise


def delete_employees(db: Session, employee_number: int):
    try:
        db_employee = db.query(models.Employees).filter(
            models.Employees.employeeNumber == employee_number
        ).first()
        if db_employee is None:
            logger.warning(f"Employee {employee_number} not found for deletion")
            return False
        db.delete(db_employee)
        db.commit()
        logger.info(f"Deleted employee {employee_number}")
        return True
    except IntegrityError as e:
        db.rollback()
        logger.error(f"FK constraint error deleting employee {employee_number}: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete employee {employee_number}: {e}")
        raise


def get_employees_with_customers(db: Session, employee_number: int):
    try:
        employee = db.query(models.Employees).filter(
            models.Employees.employeeNumber == employee_number
        ).first()
        if employee:
            logger.info(f"Retrieved employee {employee_number} with customers")
        else:
            logger.warning(f"Employee {employee_number} not found")
        return employee
    except Exception as e:
        logger.error(f"Failed to retrieve employee {employee_number} with customers: {e}")
        raise


def get_employee_reports(db: Session, employee_number: int):
    try:
        reports = db.query(models.Employees).filter(
            models.Employees.reportsTo == employee_number
        ).all()
        logger.info(f"Retrieved {len(reports)} employees reporting to {employee_number}")
        return reports
    except Exception as e:
        logger.error(f"Failed to retrieve reports for employee {employee_number}: {e}")
        raise