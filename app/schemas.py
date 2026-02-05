from pydantic import BaseModel, Field

class MarginOptions(BaseModel):
    top: str = "10mm"
    bottom: str = "10mm"
    left: str = "10mm"
    right: str = "10mm"

class PDFOptions(BaseModel):
    format: str = "A4"
    landscape: bool = False
    margin: MarginOptions = Field(default_factory=MarginOptions)
    print_background: bool = True

class ConvertRequest(BaseModel):
    html: str
    options: PDFOptions = Field(default_factory=PDFOptions)
