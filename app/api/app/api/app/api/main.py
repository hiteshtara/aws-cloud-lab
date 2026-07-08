from fastapi import FastAPI

app = FastAPI(title="CloudShop API")


@app.get("/")
def root():
    return {
        "service": "CloudShop API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/products")
def products():
    return [
        {"id": 1, "name": "Laptop", "price": 999.99},
        {"id": 2, "name": "Phone", "price": 699.99},
        {"id": 3, "name": "Headphones", "price": 149.99}
    ]
