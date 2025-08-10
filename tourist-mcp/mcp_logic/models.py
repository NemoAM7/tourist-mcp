from pydantic import BaseModel, Field

class PlaceReview(BaseModel):
    author: str
    rating: float = Field(..., description="The star rating given by the user (1-5).")
    text: str = Field(..., description="The text content of the review.")
    relative_time_description: str

class PlaceInfo(BaseModel):
    place_id: str = Field(..., description="A unique stable identifier for the place.")
    name: str
    address: str | None = None
    rating: float | None = Field(None, description="The overall star rating (1-5).")
    total_ratings: int | None = None
    phone_number: str | None = None
    website: str | None = None
    open_now: bool | None = Field(None, description="Indicates if the place is currently open.")
    maps_url: str = Field(..., description="A Google Maps URL to the location.")

class PlacePhoto(BaseModel):
    photo_reference: str = Field(..., description="Identifier to fetch the full image.")
    image_url: str = Field(..., description="The direct URL to the photo, including the API key.")