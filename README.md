# PDF Service

HTML-to-PDF microservice using Playwright (Chromium).

## API

### POST /convert

Convert HTML to PDF.

**Headers:**
- `X-API-Key`: API key (required if `API_KEY` env var is set)

**Request Body:**
```json
{
  "html": "<html>...</html>",
  "options": {
    "format": "A4",
    "margin": {
      "top": "10mm",
      "bottom": "10mm",
      "left": "10mm",
      "right": "10mm"
    },
    "print_background": true
  }
}
```

**Response:** `application/pdf` binary

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "browser_ready": true
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | API key for authentication | None |
| `MAX_BROWSER_CONTEXTS` | Max concurrent PDF renders | 4 |
| `PORT` | Server port (used by Railway) | 8000 |

## Local Development

```bash
# Build
docker build -t pdf-service .

# Run
docker run -p 8000:8000 -e API_KEY=test pdf-service
```

## Testing

Run the test suite with pytest:

```bash
pytest
```

## Deploy to Railway

1. Push to GitHub
2. Create new Railway project from repo
3. Set environment variables
4. Deploy
