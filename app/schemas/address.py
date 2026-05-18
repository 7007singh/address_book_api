from pydantic import BaseModel, Field


class AddressCreate(BaseModel):
    name: str
    street: str
    city: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class AddressResponse(AddressCreate):
    id: int

    class Config:
        from_attributes = True