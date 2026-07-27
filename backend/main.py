from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from database import Base, engine
from routers import auth, problems, submissions
import os

# Tạo bảng DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Online Judge")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files cho frontend
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "frontend")), name="static")

# Include routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(problems.router, prefix="/api", tags=["problems"])
app.include_router(submissions.router, prefix="/api", tags=["submissions"])

@app.get("/", response_class=HTMLResponse)
async def root():
    with open(os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(full_path: str):
    # Serve HTML files for frontend routing
    file_path = os.path.join(os.path.dirname(__file__), "..", "frontend", full_path)
    if os.path.exists(file_path) and not full_path.startswith(("api", "static")):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse(content="Not Found", status_code=404)
