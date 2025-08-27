import os
from dotenv import load_dotenv

# IMPORTANT: Load environment variables at the very top of the file
# This is the most reliable way to ensure they are available everywhere.
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from routers import player

# Create the main FastAPI application instance.
app = FastAPI()

# Add the CORS middleware to handle cross-origin requests from your Wix site.
# For production, it's best to specify your exact domain instead of allowing all origins.
origins = [
    "https://tripforbeauty.wixsite.com",
    "https://*.wixsite.com",
    "http://localhost:3000",  # Example for local frontend development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure basic logging to help with debugging.
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Include the router from the 'player' module.
# This means all API endpoints defined in player.py are now part of your application.
app.include_router(player.router)

print("Main file was loaded")

# A simple root endpoint to confirm that the API is running.
@app.get("/")
def root():
    return {"message": "Welcome to the game backend!"}

# This block ensures the server runs when you execute this file directly.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
