from typing import Any
import httpx
from config import GOOGLE_MAPS_API_KEY
from .models import PlaceInfo, PlacePhoto, PlaceReview
import base64

PLACES_API_BASE_URL = "https://maps.googleapis.com/maps/api/place/"

async def fetch_and_encode_photo(photo_url: str) -> str | None:
    """Downloads an image from a URL and encodes it to a Base64 string."""
    async with httpx.AsyncClient(timeout=20) as client:
        try:
            resp = await client.get(photo_url)
            resp.raise_for_status()
            image_bytes = resp.content
            return base64.b64encode(image_bytes).decode("utf-8")
        except httpx.HTTPStatusError as e:
            print(f"Failed to download image: {e}")
            return None

async def _call_places_api(endpoint: str, params: dict[str, Any]) -> dict:
    """A generic helper to call the Google Places API."""
    async with httpx.AsyncClient(timeout=20) as client:
        params["key"] = GOOGLE_MAPS_API_KEY
        resp = await client.get(f"{PLACES_API_BASE_URL}{endpoint}/json", params=params)
        resp.raise_for_status()
        return resp.json()

async def search_places_by_text(query: str, location: str | None) -> list[str]:
    """Uses Text Search to find place IDs based on a string query."""
    params = {"query": query}
    if location:
        params["location"] = location
        params["radius"] = 5000  

    data = await _call_places_api("textsearch", params)
    return [place.get("place_id") for place in data.get("results", []) if place.get("place_id")]

async def fetch_place_details(place_id: str) -> PlaceInfo | None:
    """Fetches detailed information for a single place."""
    fields = ["place_id", "name", "formatted_address", "rating", "user_ratings_total",
              "international_phone_number", "website", "opening_hours", "url", "review", "photo"]
    params = {"place_id": place_id, "fields": ",".join(fields)}
    
    data = await _call_places_api("details", params)
    result = data.get("result")
    if not result:
        return None

    return PlaceInfo(
        place_id=result["place_id"],
        name=result.get("name", "N/A"),
        address=result.get("formatted_address"),
        rating=result.get("rating"),
        total_ratings=result.get("user_ratings_total"),
        phone_number=result.get("international_phone_number"),
        website=result.get("website"),
        open_now=(result.get("opening_hours") or {}).get("open_now"),
        maps_url=result.get("url", ""),
    )

async def fetch_place_reviews(place_id: str) -> list[PlaceReview]:
    """Fetches reviews from a full place details response."""
    params = {"place_id": place_id, "fields": "review"}
    data = await _call_places_api("details", params)
    reviews_data = (data.get("result") or {}).get("reviews") or []
    return [
        PlaceReview(
            author=r.get("author_name", "A user"), rating=r.get("rating", 0),
            text=r.get("text", ""), relative_time_description=r.get("relative_time_description", "")
        ) for r in reviews_data
    ]

async def fetch_place_photos(place_id: str, max_photos: int) -> list[PlacePhoto]:
    """Fetches photos from a full place details response."""
    params = {"place_id": place_id, "fields": "photo"}
    data = await _call_places_api("details", params)
    photos_data = (data.get("result") or {}).get("photos") or []

    photos = []
    photo_url = f"{PLACES_API_BASE_URL}photo"
    for photo in photos_data[:max_photos]:
        photo_ref = photo.get("photo_reference")
        if photo_ref:
            full_url = f"{photo_url}?maxwidth=400&photoreference={photo_ref}&key={GOOGLE_MAPS_API_KEY}"
            photos.append(PlacePhoto(photo_reference=photo_ref, image_url=full_url))
    return photos