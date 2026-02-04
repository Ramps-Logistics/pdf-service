from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, Response

from app.browser import browser_pool
from app.config import settings
from app.renderer import render_pdf
from app.schemas import HealthResponse, PDFRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    await browser_pool.start()
    yield
    await browser_pool.stop()


app = FastAPI(title="PDF Service", lifespan=lifespan)


async def verify_api_key(x_api_key: str | None = Header(default=None)):
    if settings.API_KEY is None:
        return
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.post("/convert")
async def convert(request: PDFRequest, _: None = Depends(verify_api_key)):
    pdf_bytes = await render_pdf(request.html, request.options)
    return Response(content=pdf_bytes, media_type="application/pdf")


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="healthy", browser_ready=browser_pool.is_ready)
