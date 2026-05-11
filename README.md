# Solar Quote API - Parallel Fetch Demo

A FastAPI backend service that accepts a solar installation location, fetches real solar production data from Forecast.Solar, fetches finance data from an internal mock API, and combines both results into one JSON response.

## Features

- FastAPI backend with Swagger UI and ReDoc
- Real Forecast.Solar integration
- Internal mock finance API with a simulated 300ms delay
- Parallel API execution with `asyncio.gather`
- Graceful partial-error responses when one upstream call fails
- Environment-based configuration for local and production deployments
- CORS middleware enabled for production-style deployments

## Project Structure

```text
.
├── app/
│   ├── api/routes/
│   │   ├── finance.py
│   │   ├── health.py
│   │   └── solar.py
│   ├── core/
│   │   └── config.py
│   ├── models/
│   │   ├── request_models.py
│   │   └── response_models.py
│   ├── services/
│   │   ├── finance_service.py
│   │   ├── parallel_service.py
│   │   └── solar_service.py
│   ├── __init__.py
│   └── main.py
├── .env.example
├── requirements.txt
├── README.md
└── run.py
```

## Requirements

- Python 3.9+
- Internet connection for Forecast.Solar requests

## Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your environment file

Copy `.env.example` to `.env` and adjust values if needed.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

## Run Locally

Option 1:

```bash
python run.py
```

Option 2:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Once the server is running:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- OpenAPI JSON: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## API Endpoints

- `GET /solar-quote` - combined solar + finance quote
- `GET /mock-finance` - mock finance provider response
- `GET /health` - health check
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc

## Example Requests

### Solar quote

```http
GET /solar-quote?lat=51.5&lon=-0.1&tilt=35&azimuth=0&kwp=4
```

Example curl:

```bash
curl "http://localhost:8000/solar-quote?lat=51.5&lon=-0.1&tilt=35&azimuth=0&kwp=4"
```

### Mock finance

```bash
curl "http://localhost:8000/mock-finance?kwp=4"
```

### Health check

```bash
curl "http://localhost:8000/health"
```

## Example Response

```json
{
  "status": "success",
  "location": {
    "lat": 51.5,
    "lon": -0.1
  },
  "system": {
    "kwp": 4,
    "tilt_degrees": 35,
    "azimuth_degrees": 0
  },
  "solar": {
    "today_production_wh": 12500,
    "today_production_kwh": 12.5,
    "api_source": "forecast.solar",
    "error": null
  },
  "finance": {
    "provider": "Demo Finance",
    "apr_percent": 9.9,
    "monthly_payment_per_kw": 15,
    "estimated_monthly_payment": 60,
    "term_months": 120,
    "error": null
  }
}
```

## Testing

### Manual browser test

1. Start the server.
2. Open [http://localhost:8000/docs](http://localhost:8000/docs).
3. Expand `GET /solar-quote`.
4. Click `Try it out`.
5. Enter:
   - `lat=51.5`
   - `lon=-0.1`
   - `tilt=35`
   - `azimuth=0`
   - `kwp=4`
6. Click `Execute`.

### Command-line smoke tests

```bash
curl "http://localhost:8000/health"
curl "http://localhost:8000/mock-finance?kwp=4"
curl "http://localhost:8000/solar-quote?lat=51.5&lon=-0.1"
```

### PowerShell test

```powershell
Invoke-RestMethod "http://localhost:8000/solar-quote?lat=51.5&lon=-0.1&tilt=35&azimuth=0&kwp=4"
```

## Environment Variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `API_HOST` | `0.0.0.0` | Host interface for the FastAPI server |
| `API_PORT` | `8000` | Local port for the API |
| `PORT` | unset | Render-style port fallback used automatically if `API_PORT` is not set |
| `ENVIRONMENT` | `development` | Enables production-aware behavior such as CORS defaults |
| `SOLAR_API_BASE_URL` | `https://api.forecast.solar` | Forecast.Solar base URL |
| `INTERNAL_API_HOST` | `127.0.0.1` | Host used for internal `/mock-finance` API calls |
| `REQUEST_TIMEOUT_SECONDS` | `10` | HTTP timeout for solar and finance requests |
| `ENABLE_CORS` | `false` in development, `true` in production | Toggle CORS middleware |
| `CORS_ALLOW_ORIGINS` | `*` | Allowed origins, comma-separated if needed |
| `FINANCE_API_URL` | unset | Optional override for the internal finance endpoint URL |

## Deploy to Render

This repository includes a `render.yaml` Blueprint file, so you can either deploy manually or let Render read the configuration from the repo automatically.

### 1. Push the code to GitHub

Render deploys from a GitHub repository, so commit your changes and push the project first.

### 2. Create a new service in Render

1. Log in to [Render](https://render.com/).
2. Click `New +`.
3. Choose either:
   - `Blueprint` to use the included `render.yaml`, or
   - `Web Service` to configure everything manually
4. Connect your GitHub repository.
5. Select the repository for this project.

### 3. Configure the service

Use these values:

- Runtime: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 4. Set environment variables in Render

Add at least:

- `ENVIRONMENT=production`
- `ENABLE_CORS=true`
- `CORS_ALLOW_ORIGINS=*`

Optional:

- `SOLAR_API_BASE_URL=https://api.forecast.solar`
- `REQUEST_TIMEOUT_SECONDS=10`

### 5. Deploy

Click `Create Web Service`. Render will build and start the application.

After deployment, your URLs will look like:

- `https://your-service-name.onrender.com/docs`
- `https://your-service-name.onrender.com/solar-quote?lat=51.5&lon=-0.1`

## Notes

- Forecast.Solar is a free public API and may rate-limit repeated requests.
- The combined quote endpoint calls the internal finance API over HTTP so the parallel fetch behavior is easy to demonstrate and inspect.
- In production, replace `CORS_ALLOW_ORIGINS=*` with your actual frontend domains if needed.
