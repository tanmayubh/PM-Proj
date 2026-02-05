from fastapi import FastAPI
from routers.projects import router as projects_router
from routers.tasks import router as tasks_router
from routers.users import router as users_router
from routers import auth
app = FastAPI()

# Root endpoint
@app.get("/")
def root():
    return {"message": "SERVER WORKS"}

app.include_router(auth.router)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(users_router)

@app.get("/health")
def dealth_check():
    return {
        "status": "ok",
        "service": "project-management-api"
    }