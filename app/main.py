from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.v1.router import router

app = FastAPI(
    title="Event Booking System",
    version="1.0.0",
    description="BookMyShow-style backend",
)

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Event Booking System",
        version="1.0.0",
        description="BookMyShow-style backend",
        routes=app.routes,
    )

    # Add Bearer token security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply security to all routes
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi