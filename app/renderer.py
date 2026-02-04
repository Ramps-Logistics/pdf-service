from app.browser import browser_pool
from app.schemas import PDFOptions


async def render_pdf(html: str, options: PDFOptions | None = None) -> bytes:
    if options is None:
        options = PDFOptions()

    async with browser_pool.acquire_context() as context:
        page = await context.new_page()
        await page.set_content(html, wait_until="networkidle")
        pdf_bytes = await page.pdf(
            format=options.format,
            margin={
                "top": options.margin_top,
                "bottom": options.margin_bottom,
                "left": options.margin_left,
                "right": options.margin_right,
            },
            print_background=options.print_background,
        )
        return pdf_bytes
