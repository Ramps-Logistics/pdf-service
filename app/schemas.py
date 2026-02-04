from pydantic import BaseModel


class PDFOptions(BaseModel):
    format: str = "A4"
    margin_top: str = "10mm"
    margin_bottom: str = "10mm"
    margin_left: str = "10mm"
    margin_right: str = "10mm"
    print_background: bool = True


class PDFRequest(BaseModel):
    html: str
    options: PDFOptions | None = None


class HealthResponse(BaseModel):
    status: str
    browser_ready: bool
