# WhatsApp Local Guide Bot - MCP Server

This project is a backend server built with **FastMCP** that provides a set of tools for a WhatsApp bot or another AI-powered service. It acts as a specialized "co-processor" to fetch information about local places, such as restaurants, parks, and landmarks, by using the Google Places API.

The server exposes simple, high-level tools that an application can call to find places, get details, retrieve reviews, and fetch photos, without needing to know the complexities of the underlying Google API.

## Core Features

*   **Find Places**: Search for places using natural language queries (e.g., "good pizza place nearby").
*   **Get Details**: Retrieve detailed information for any place, including its address, rating, phone number, and opening hours.
*   **Get Reviews**: Fetch the latest user reviews for a specific location.
*   **Get Photos**: Retrieve high-quality photo URLs for a place.
*   **Secure**: Uses bearer token authentication to protect the API endpoints.
*   **Structured**: Built with a clean, modular architecture for easy maintenance and extension.

## Technology Stack

*   **Framework**: FastMCP
*   **Language**: Python 3.10+
*   **API Communication**: HTTpx for asynchronous HTTP requests.
*   **Data Validation**: Pydantic for robust data modeling and validation.
*   **External APIs**: Google Places API.
*   **Configuration**: `python-dotenv` for managing environment variables.

## Project Structure

The project is organized into modules with clear responsibilities:

```
local_guide_bot/
├── .env                  # Stores secret keys and configuration
├── requirements.txt      # Python dependencies
├── config.py             # Loads and validates environment variables
├── auth.py               # Handles API authentication logic
├── mcp_logic/
│   ├── __init__.py
│   ├── models.py         # Pydantic data models (PlaceInfo, etc.)
│   ├── google_api.py     # Low-level functions to call Google APIs
│   └── tools.py          # High-level MCP tool definitions
└── main.py               # Main server entrypoint
```

## Setup and Installation

Follow these steps to get the server running on your local machine.

### 1. Prerequisites

*   Python 3.10 or newer.
*   A Google Cloud Platform account with the **Places API** enabled. You can get an API key from the Google Cloud Console.

### 2. Clone the Repository (Optional)

If you have this project in a git repository, clone it. Otherwise, just ensure you have the file structure described above.

```sh
git clone <your-repo-url>
cd local_guide_bot
```

### 3. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```sh
# For Windows
python -m venv .venv
.\.venv\Scripts\activate

# For macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

Install all the required Python packages from `requirements.txt`.

```sh
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a file named `.env` in the root of the project directory. Copy the contents of `.env.example` (or the block below) into it and add your secret keys.

**Create the `.env` file:**

```
# .env

# A secret token you define to secure your MCP server. Make it long and random.
AUTH_TOKEN="your_super_secret_mcp_token_here"

# Your API key from Google Cloud Platform
GOOGLE_MAPS_API_KEY="your_google_maps_api_key_here"
```

*   `AUTH_TOKEN`: A secret password of your choice. Any client calling the server must provide this token.
*   `GOOGLE_MAPS_API_KEY`: Your key for the Google Places API.

## Running the Server

Once the setup is complete, you can start the server with the following command:

```sh
python main.py
```

You should see the following output, indicating the server is running successfully:

```
Starting WhatsApp Local Guide MCP server on http://0.0.0.0:8088
```

The server is now listening for requests on port `8088`.

## API Tools

The MCP server exposes the following tools, which can be called via JSON-RPC requests.

### 1. `find_nearby_places`

Finds places based on a query and returns key details.

*   **Params**:
    *   `user_query` (str): The user's search query (e.g., "a good pizza place").
    *   `user_location` (str, optional): The user's location as `"latitude,longitude"`.
    *   `max_results` (int, optional): The maximum number of places to return (default: 3).
*   **Returns**: A list of `PlaceInfo` objects.

### 2. `get_place_reviews`

Fetches user reviews for a specific place.

*   **Params**:
    *   `place_id` (str): The unique ID of the place, obtained from `find_nearby_places`.
*   **Returns**: A list of `PlaceReview` objects.

### 3. `get_place_photos`

Gets photo URLs for a specific place.

*   **Params**:
    *   `place_id` (str): The unique ID of the place.
    *   `max_photos` (int, optional): The maximum number of photos to return (default: 2).
*   **Returns**: A list of `PlacePhoto` objects with direct image URLs.

## Example: How to Call a Tool

You can call the tools using any HTTP client that supports POST requests. Here is an example using `curl` to call the `find_nearby_places` tool.

Remember to replace `<your_auth_token>` with the `AUTH_TOKEN` you set in your `.env` file.

```sh
curl -X POST http://localhost:8088/mcp \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_auth_token>" \
     -d '{
           "jsonrpc": "2.0",
           "method": "find_nearby_places",
           "params": {
             "user_query": "Eiffel Tower",
             "max_results": 1
           },
           "id": 1
         }'
```

