from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from geopy.distance import geodesic
from fastapi import Query
from app.database import get_db
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressResponse
from fastapi import HTTPException
from app.utils.logger import logger


router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"]
)


@router.post("/", response_model=AddressResponse)
def create_address(
        payload: AddressCreate,
        db: Session = Depends(get_db)
):
    address = Address(
        name=payload.name,
        street=payload.street,
        city=payload.city,
        latitude=payload.latitude,
        longitude=payload.longitude
    )

    db.add(address)
    db.commit()
    db.refresh(address)
    logger.info("Creating new address")
    return address


@router.get("/", response_model=list[AddressResponse])
def get_addresses(db: Session = Depends(get_db)):
    addresses = db.query(Address).all()
    return addresses


@router.put("/{address_id}", response_model=AddressResponse)
def update_address(
        address_id: int,
        payload: AddressCreate,
        db: Session = Depends(get_db)
):
    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    address.name = payload.name
    address.street = payload.street
    address.city = payload.city
    address.latitude = payload.latitude
    address.longitude = payload.longitude

    db.commit()
    db.refresh(address)
    logger.info(f"Updating address with id {address_id}")
    return address


@router.delete("/{address_id}")
def delete_address(
        address_id: int,
        db: Session = Depends(get_db)
):
    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        return {"message": "Address not found"}

    db.delete(address)
    db.commit()
    logger.info(f"Deleting address with id {address_id}")
    return {"message": "Address deleted successfully"}


@router.get("/nearby/")
def get_nearby_addresses(
        latitude: float = Query(...),
        longitude: float = Query(...),
        distance: float = Query(...),
        db: Session = Depends(get_db)
):
    addresses = db.query(Address).all()

    nearby_addresses = []

    for address in addresses:
        calculated_distance = geodesic(
            (latitude, longitude),
            (address.latitude, address.longitude)
        ).km

        if calculated_distance <= distance:
            nearby_addresses.append({
                "id": address.id,
                "name": address.name,
                "street": address.street,
                "city": address.city,
                "latitude": address.latitude,
                "longitude": address.longitude,
                "distance_km": round(calculated_distance, 2)
            })

    return nearby_addresses
