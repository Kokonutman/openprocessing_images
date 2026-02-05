from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from PIL import Image
import requests
from io import BytesIO

app = FastAPI(title="OpenProcessing Image API", version="1.0.0")

# Global variable for image
img = Image.open(BytesIO(requests.get("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxSuFBVRoFSZV2aWth19jlE71sFU0isoOF5VbN4SzZDuoeH0YjzYE0ppnYJGfO_ErLLb6ZE08PuFRzbdm6ShAIpDHM10HQLZ0EhowWvhiYEg&s=10").content))
rgbData = img.get_flattened_data();
# Request/Response models
class PostRequestModel(BaseModel):
    endpoint: str


class PostResponseModel(BaseModel):
    # Add your POST response fields here
    pass


# POST endpoint
@app.post("/api/uploadURL", response_model=PostResponseModel)
async def uploadURL(url: str):
    global img, rgbData
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        rgbData = img.get_flattened_data();
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET endpoint 1
@app.get("/api/getDimensions")
async def getDimensions():
    try:
        #returns a tuple in the form x,y
        return img.size
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET endpoint 2
@app.get("/api/getPixels")
async def getPixel():
    """
    GET endpoint 2 - Add your implementation here
    """
    try:
        #returns an array of tuples [r,g,b]
        return rgbData
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Health check endpoint (useful for Render)
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

