from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from geopy.distance import geodesic
from fastapi import Query
from app.database import get_db
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressResponse
from fastapi import HTTPException
from app.utils.logger import logger
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"]
)


@router.post(
    "/",
    response_model=AddressResponse,
    summary="Create a new address"
)
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

    try:
        db.add(address)
        db.commit()
        db.refresh(address)

        logger.info("Address created successfully")

        return address

    except SQLAlchemyError as error:
        db.rollback()

        logger.error(f"Database error: {str(error)}")

        raise HTTPException(
            status_code=500,
            detail="Database error occurred"
        )


@router.get(
    "/",
    response_model=list[AddressResponse],
    summary="Get all addresses"
)
def get_addresses(db: Session = Depends(get_db)):
    addresses = db.query(Address).all()
    return addresses


@router.put(
    "/{address_id}",
    response_model=AddressResponse,
    summary="Update an address"
)
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

    try:
        db.commit()
        db.refresh(address)

        logger.info(f"Address updated successfully: {address_id}")

        return address

    except SQLAlchemyError as error:
        db.rollback()

        logger.error(f"Database error while updating: {str(error)}")

        raise HTTPException(
            status_code=500,
            detail="Database error occurred"
        )


@router.delete(
    "/{address_id}",
    summary="Delete an address"
)
def delete_address(
        address_id: int,
        db: Session = Depends(get_db)
):
    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        return {"message": "Address not found"}

    try:
        db.delete(address)
        db.commit()

        logger.info(f"Address deleted successfully: {address_id}")

        return {"message": "Address deleted successfully"}

    except SQLAlchemyError as error:
        db.rollback()

        logger.error(f"Database error while deleting: {str(error)}")

        raise HTTPException(
            status_code=500,
            detail="Database error occurred"
        )


@router.get(
    "/nearby/",
    summary="Get nearby addresses"
)
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
