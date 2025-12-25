from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth_router, camera_router

app = FastAPI(title="TverEyNg Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(camera_router)


@app.get("/")
async def root():
    return {"message": "Server is running"}
