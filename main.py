import requests
from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.testclient import TestClient

from app.views.products import router as product_router

app = FastAPI()
app.include_router(product_router, prefix='/product')


@app.get("/")
async def root():
    return {"message": "Welcome to bitA project"}


# Mount static files
app.mount("/static", StaticFiles(directory="app/statics"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

client = TestClient(app)


@app.get("/website", response_class=HTMLResponse)
async def read_products(request: Request, page: int = 1, page_size: int = 3):
    # Fetch product data from the API
    response = client.get(f"/product?page={page}&page_size={page_size}")
    product_data = response.json()
    products = product_data["data"]
    total_pages = (len(products) + page_size - 1) // page_size

    return templates.TemplateResponse("index.html", {
        "request": request,
        "products": products,
        "page": page,
        "total_pages": total_pages
    })
