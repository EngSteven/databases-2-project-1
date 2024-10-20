import uvicorn
from fastapi import FastAPI
from routes import user_routes, travel_routes, destiny_routes, posts_routes
from auth import verify_token, oauth2_scheme

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(travel_routes.router)
app.include_router(destiny_routes.router)
app.include_router(posts_routes.router)

@app.get("/")
async def ver_version():
    return {"version": "0.0.1"}

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
