from fastapi import FastAPI, HTTPException
from PIL import Image
import requests
from io import BytesIO

app = FastAPI(title="OpenProcessing Image API", version="1.0.0")


# Single GET endpoint
@app.get("/getImage")
async def getImage(url: str):
    """
    GET endpoint that takes an image URL and returns image data
    Usage: /getImage?url=<image_url>
    """
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.convert('RGB')
        rgbData = list(img.getdata())
        return {
            "dimensions": img.size,
            "pixels": rgbData
        }
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

