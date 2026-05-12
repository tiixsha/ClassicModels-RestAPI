from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
import crud.employee_crud as employee_crud
import schemas.employee_schemas as employee_schemas
from typing import List
from logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=List[employee_schemas.EmployeeOut])
def list_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /employees - skip={skip} limit={limit}")
        employees = employee_crud.get_employeess(db, skip=skip, limit=limit)
        logger.info(f"Returned {len(employees)} employees")
        return employees
    except Exception as e:
        logger.error(f"Error listing employees: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{employee_number}/customers", response_model=employee_schemas.EmployeeOut)
def get_employee_with_customers(employee_number: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /employees/{employee_number}/customers")
        employee = employee_crud.get_employees_with_customers(db, employee_number)
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting customers for employee {employee_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{employee_number}/reports", response_model=List[employee_schemas.EmployeeOut])
def get_employee_reports(employee_number: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /employees/{employee_number}/reports")
        employee = employee_crud.get_employees(db, employee_number)
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        reports = employee_crud.get_employee_reports(db, employee_number)
        logger.info(f"Returned {len(reports)} reports for employee {employee_number}")
        return reports
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting reports for employee {employee_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{employee_number}", response_model=employee_schemas.EmployeeOut)
def get_employee(employee_number: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"GET /employees/{employee_number}")
        employee = employee_crud.get_employees(db, employee_number)
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting employee {employee_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/", response_model=employee_schemas.EmployeeOut, status_code=201)
def create_employee(employee: employee_schemas.EmployeeCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"POST /employees - creating employee {employee.employeeNumber}")
        db_employee = employee_crud.create_employees(db, employee)
        logger.info(f"Employee {db_employee.employeeNumber} created successfully")
        return db_employee
    except IntegrityError as e:
        logger.error(f"FK violation creating employee: {e}")
        raise HTTPException(status_code=422, detail="Invalid officeCode or reportsTo — referenced record does not exist")
    except Exception as e:
        logger.error(f"Error creating employee: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{employee_number}", response_model=employee_schemas.EmployeeOut)
def update_employee(employee_number: int, employee_update: employee_schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    try:
        logger.info(f"PUT /employees/{employee_number}")
        db_employee = employee_crud.update_employees(db, employee_number, employee_update)
        if db_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return db_employee
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating employee {employee_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{employee_number}", status_code=204)
def delete_employee(employee_number: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"DELETE /employees/{employee_number}")
        success = employee_crud.delete_employees(db, employee_number)
        if not success:
            raise HTTPException(status_code=404, detail="Employee not found")
        return
    except HTTPException:
        raise
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Cannot delete employee — they have direct reports or assigned customers")
    except Exception as e:
        logger.error(f"Error deleting employee {employee_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")