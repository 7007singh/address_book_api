from fastapi import FastAPI

from app.database import Base, engine
from app.models.address import Address
from app.routes.address import router as address_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address Book API")

app.include_router(address_router)


@app.get("/")
def home():
    return {"message": "Address Book API Running"}