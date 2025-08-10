from typing import Annotated
from fastmcp import FastMCP
from mcp import McpError, ErrorData
from pydantic import Field
from . import google_api
from mcp.types import TextContent, ImageContent

NOT_FOUND = -32004

def register_tools(mcp: FastMCP):
    """
    Registers all the local guide tools with the given FastMCP instance.
    """
    
    @mcp.tool
    async def find_nearby_places(
        user_query: Annotated[
            str, Field(description="User's request, e.g., 'a good pizza place'.")
        ],
        user_location: Annotated[
            str | None, Field(description="User's location as 'latitude,longitude'.")
        ] = None,
        max_results: Annotated[int, Field(description="Maximum number of places to return.")] = 3,
    ) -> dict:
        """Finds places based on a query and returns key details for each."""
        place_ids = await google_api.search_places_by_text(user_query, user_location)
        if not place_ids:
            raise McpError(ErrorData(code=NOT_FOUND, message="Couldn't find any places matching that."))

        detailed_places = [
            await google_api.fetch_place_details(pid) for pid in place_ids[:max_results]
        ]
        valid_places = [p for p in detailed_places if p]

        if not valid_places:
            raise McpError(ErrorData(code=NOT_FOUND, message="Found places, but couldn't fetch their details."))

        return {"places": [p.model_dump() for p in valid_places]}

    @mcp.tool
    async def get_place_reviews(
        place_id: Annotated[str, Field(description="The ID of the place.")]
    ) -> dict:
        """Fetches user reviews for a specific place."""
        reviews = await google_api.fetch_place_reviews(place_id)
        if not reviews:
            raise McpError(ErrorData(code=NOT_FOUND, message="No reviews found for this place."))
        return {"reviews": [r.model_dump() for r in reviews]}

    @mcp.tool
    async def get_place_photos(
        place_id: Annotated[str, Field(description="The ID of the place.")],
        place_name: Annotated[str, Field(description="The name of the place for the caption.")],
        max_photos: Annotated[int, Field(description="Max photos to return.")] = 1
    ) -> list[TextContent | ImageContent]: # <-- 1. CHANGE THE RETURN TYPE
        """
        Gets photos for a specific place, encodes them to Base64, and returns them
        inline with a caption.
        """
        photos_with_urls = await google_api.fetch_place_photos(place_id, max_photos)
        if not photos_with_urls:
            raise McpError(ErrorData(code=NOT_FOUND, message="No photos found for this place."))

        message_parts: list[TextContent | ImageContent] = []
        message_parts.append(
            TextContent(type="text", text=f"Here is a photo of {place_name}:")
        )

        for photo in photos_with_urls:
            base64_data = await google_api.fetch_and_encode_photo(photo.image_url)
            
            if base64_data:
                message_parts.append(
                    ImageContent(
                        type="image",
                        mimeType="image/jpeg",
                        data=base64_data
                    )
                )

        if len(message_parts) <= 1:
             raise McpError(ErrorData(code=NOT_FOUND, message="Found photo references, but failed to download the images."))

        return message_parts