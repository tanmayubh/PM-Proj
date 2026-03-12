from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from routers.projects import router as projects_router
from routers.tasks import router as tasks_router
from routers.users import router as users_router
from routers import auth

app = FastAPI(
    title="Project Management API",
    description="Backend API for project & task management with role-based access",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler for validation errors
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

# Root endpoint
@app.get("/")
def root():
    return {"message": "API is running", "version": "1.0.0"}

app.include_router(auth.router)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(users_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "project-management-api"
    }