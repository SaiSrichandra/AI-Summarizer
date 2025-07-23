from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.routers import auth, user, summary
from app.db.session import init_db
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="AI Web Article Summarizer",
    description="Submit a link and get a summary of the article using AI.",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/api/users", tags=["Users"])
app.include_router(summary.router, prefix="/api/summaries", tags=["Summaries"])



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_dir = os.path.join(BASE_DIR, "frontend")

# Mount /static to serve /frontend/
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# HTML routes
@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse("frontend/index.html")

@app.get("/dashboard", include_in_schema=False)
async def serve_dashboard():
    return FileResponse("frontend/dashboard.html")

@app.get("/admin", include_in_schema=False)
async def serve_admin():
    return FileResponse("frontend/admin.html")

# DB startup
@app.on_event("startup")
async def on_startup():
    await init_db()