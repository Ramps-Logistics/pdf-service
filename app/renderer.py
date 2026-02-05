from .browser import browser_pool
from .schemas import PDFOptions
from .config import settings

async def render_pdf(html: str, options: PDFOptions) -> bytes:
    async with browser_pool.acquire_context() as context:
        page = await context.new_page()
        try:
            await page.set_content(
                html,
                wait_until="networkidle",
                timeout=settings.render_timeout_ms,
            )
            pdf_bytes = await page.pdf(
                format=options.format,
                landscape=options.landscape,
                margin={
                    "top": options.margin.top,
                    "bottom": options.margin.bottom,
                    "left": options.margin.left,
                    "right": options.margin.right,
                },
                print_background=options.print_background,
                timeout=settings.render_timeout_ms,
            )
            return pdf_bytes
        finally:
            await page.close()
