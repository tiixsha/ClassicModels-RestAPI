from sqlalchemy import Column, Integer, String, Numeric,ForeignKey, Date, Text
from database import Base
from sqlalchemy.orm import relationship

class Customers(Base):
    __tablename__ = 'customers'

    customerNumber = Column(Integer, primary_key=True, index=True)
    customerName = Column(String(50), nullable=False)
    contactLastName = Column(String(50), nullable=False)
    contactFirstName = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    addressLine1 = Column(String(50), nullable=False)
    addressLine2 = Column(String(50), nullable=True)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=True)
    postalCode = Column(String(15), nullable=True)
    country = Column(String(50), nullable=False)
    salesRepEmployeeNumber = Column(Integer, nullable=True, index=True)
    creditLimit = Column(Numeric(10,2), nullable=True)

    orders = relationship("Orders", back_populates="customer")
    payments = relationship("Payments", back_populates="customer")

    def __repr__(self):
        return f"<Customers(customerNumber={self.customerNumber}, customerName='{self.customerName}')>"
    

class Orders(Base):
    __tablename__ = 'orders'

    orderNumber = Column(Integer, primary_key=True, index=True)
    orderDate = Column(Date, nullable=False)
    requiredDate = Column(Date, nullable=False)
    shippedDate = Column(Date, nullable=True)
    status = Column(String(15), nullable=False)
    comments = Column(Text, nullable=True)
    customerNumber = Column(Integer, ForeignKey('customers.customerNumber'), nullable=False, index=True)

    customer = relationship("Customers", back_populates="orders")

    def __repr__(self):
        return f"<Orders(orderNumber={self.orderNumber}, status='{self.status}')>"
    
    

class Payments(Base):
    __tablename__ = 'payments'

    customerNumber = Column(Integer, ForeignKey('customers.customerNumber'), primary_key=True, index=True)
    checkNumber = Column(String(50), primary_key=True, index=True)
    paymentDate = Column(Date, nullable=False)
    amount = Column(Numeric(10,2), nullable=False)

    customer = relationship("Customers", back_populates="payments")

    def __repr__(self):
        return f"<Payments(customerNumber={self.customerNumber}, checkNumber='{self.checkNumber}', amount={self.amount})>"
    
    