from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date, Text, SmallInteger, LargeBinary
from database import Base
from sqlalchemy.orm import relationship


class Offices(Base):
    __tablename__ = 'offices'

    officeCode = Column(String(10), primary_key=True, index=True)
    city = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    addressLine1 = Column(String(50), nullable=False)
    addressLine2 = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    country = Column(String(50), nullable=False)
    postalCode = Column(String(15), nullable=False)
    territory = Column(String(10), nullable=False)

    employees = relationship("Employees", back_populates="office")

    def __repr__(self):
        return f"<Offices(officeCode='{self.officeCode}', city='{self.city}')>"


class Employees(Base):
    __tablename__ = 'employees'

    employeeNumber = Column(Integer, primary_key=True, index=True)
    lastName = Column(String(50), nullable=False)
    firstName = Column(String(50), nullable=False)
    extension = Column(String(10), nullable=False)
    email = Column(String(100), nullable=False)
    officeCode = Column(String(10), ForeignKey('offices.officeCode'), nullable=False, index=True)
    reportsTo = Column(Integer, nullable=True)
    jobTitle = Column(String(50), nullable=False)

    office = relationship("Offices", back_populates="employees")

    def __repr__(self):
        return f"<Employees(employeeNumber={self.employeeNumber}, lastName='{self.lastName}')>"


class ProductLines(Base):
    __tablename__ = 'productlines'

    productLine = Column(String(50), primary_key=True, index=True)
    textDescription = Column(String(4000), nullable=True)
    htmlDescription = Column(Text, nullable=True)
    image = Column(LargeBinary, nullable=True)

    products = relationship("Products", back_populates="productline")

    def __repr__(self):
        return f"<ProductLines(productLine='{self.productLine}')>"


class Products(Base):
    __tablename__ = 'products'

    productCode = Column(String(15), primary_key=True, index=True)
    productName = Column(String(70), nullable=False)
    productLine = Column(String(50), ForeignKey('productlines.productLine'), nullable=False, index=True)
    productScale = Column(String(10), nullable=False)
    productVendor = Column(String(50), nullable=False)
    productDescription = Column(Text, nullable=False)
    quantityInStock = Column(Integer, nullable=False)
    buyPrice = Column(Numeric(10,2), nullable=False)
    MSRP = Column(Numeric(10,2), nullable=False)

    productline = relationship("ProductLines", back_populates="products")
    orderdetails = relationship("OrderDetails", back_populates="product")

    def __repr__(self):
        return f"<Products(productCode='{self.productCode}', productName='{self.productName}')>"


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
    orderdetails = relationship("OrderDetails", back_populates="order")

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


class OrderDetails(Base):
    __tablename__ = 'orderdetails'

    orderNumber = Column(Integer, ForeignKey('orders.orderNumber'), primary_key=True, nullable=False, index=True)
    productCode = Column(String(15), ForeignKey('products.productCode'), primary_key=True, nullable=False, index=True)
    quantityOrdered = Column(Integer, nullable=False)
    priceEach = Column(Numeric(10,2), nullable=False)
    orderLineNumber = Column(SmallInteger, nullable=False)

    order = relationship("Orders", back_populates="orderdetails")
    product = relationship("Products", back_populates="orderdetails")

    def __repr__(self):
        return f"<OrderDetails(orderNumber={self.orderNumber}, productCode='{self.productCode}')>"