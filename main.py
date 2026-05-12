from fastapi import FastAPI
import routers.customer_router as customer_router, models
import routers.dashboard_router as dashboard_router
from database import engine
import uvicorn
from logger import get_logger
from routers import customer_router, dashboard_router, product_router, productline_router,office_router,employee_router,order_router, orderdetail_router,payment_router    



logger = get_logger(__name__)

app = FastAPI(
    title="ClassicModels REST API",
    description="A REST API for managing the ClassicModels database",
    version="1.0.0"
)

models.Base.metadata.create_all(bind=engine)

app.include_router(dashboard_router.router) # Include the dashboard router first to ensure its endpoints are registered before the customers router
app.include_router(customer_router.router)
app.include_router(product_router.router, prefix="/products", tags=["Products"])
app.include_router(productline_router.router, prefix="/productlines", tags=["ProductLines"])
app.include_router(office_router.router, prefix="/offices", tags=["Offices"])
app.include_router(employee_router.router, prefix="/employees", tags=["Employees"])
app.include_router(order_router.router, prefix="/orders", tags=["Orders"])
app.include_router(orderdetail_router.router,  prefix="/orderdetails", tags=["OrderDetails"])
app.include_router(payment_router.router,      prefix="/payments",     tags=["Payments"])

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "ClassicModels API is running!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)