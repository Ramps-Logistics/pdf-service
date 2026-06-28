import sys
import asyncio
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Response, Depends, Header

# Fix Windows asyncio subprocess issue (no-op on Linux)
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from .browser import browser_pool
from .renderer import render_pdf
from .schemas import ConvertRequest
from .config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    await browser_pool.start()
    yield
    await browser_pool.stop()

app = FastAPI(title="PDF Service", lifespan=lifespan)
_start_time = time.time()

def verify_api_key(x_api_key: str | None = Header(None)):
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "browser_ready": browser_pool.is_ready,
        "uptime_seconds": round(time.time() - _start_time, 1),
    }

@app.get("/status")
async def status():
    return {
        "status": "healthy" if browser_pool.is_ready else "starting",
        "browser_ready": browser_pool.is_ready,
        "queue": browser_pool.stats,
    }

@app.post("/convert", dependencies=[Depends(verify_api_key)])
async def convert(request: ConvertRequest):
    if len(request.html.encode()) > settings.max_html_size_bytes:
        raise HTTPException(status_code=400, detail="HTML too large")
    
    if not browser_pool.is_ready:
        raise HTTPException(status_code=503, detail="Browser not ready")
    
    try:
        pdf_bytes = await render_pdf(request.html, request.options)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Render failed: {str(e)}")
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=document.pdf"}
    )
