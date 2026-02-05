from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import requests
from io import BytesIO

app = FastAPI(title="OpenProcessing Image API", version="1.0.0")

# Enable CORS for OpenProcessing
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://preview.openprocessing.org",
        "https://openprocessing.org",
        "http://localhost:3000",  # For local development
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# Single GET endpoint
@app.get("/getImage")
async def getImage(url: str):
    """
    GET endpoint that takes an image URL and returns image data
    Usage: /getImage?url=<image_url>
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Check if response is actually an image
        content_type = response.headers.get('content-type', '').lower()
        if not content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, 
                detail=f"URL does not return an image. Content-Type: {content_type}"
            )
        
        img = Image.open(BytesIO(response.content))
        img = img.convert('RGB')
        rgbData = list(img.getdata())
        return {
            "dimensions": img.size,
            "pixels": rgbData
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch image: {str(e)}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# Default image endpoint with fixed response
@app.get("/getImageDefault")
async def getImageDefault():
    """
    GET endpoint that returns a fixed response (no URL parameter needed)
    """
    try:
        img = Image.open("utah_teapot.jpg")
        img = img.convert('RGB')
        rgbData = list(img.getdata())
        return {
            "dimensions": img.size,
            "pixels": rgbData
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# Health check endpoint (useful for Render)
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

