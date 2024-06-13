from fastapi import FastAPI

from app.views.products import router as product_router

app = FastAPI()
app.include_router(product_router, prefix='/product')


@app.get("/")
async def root():
    return {"message": "Welcome to bitA project"}
