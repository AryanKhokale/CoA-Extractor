# REST API Reference

The backend exposes an interactive OpenAPI specification accessible at `/docs` (Swagger UI) and `/redoc` (ReDoc).

## Endpoints

### System & Health
- `GET /` — API root information.
- `GET /api/health` — Health check endpoint returning status and service version.
- `GET /api/config` — Current runtime settings, concurrency limits, and active mode (live vs mock).

### Directory Explorer
- `GET /api/directory/architects`
  - Query parameters: `query`, `state`, `city`, `status`, `sort_by`, `sort_order`, `page`, `page_size`.
  - Returns paginated list of validated architect records.
- `GET /api/directory/search`
  - Query parameters: `q`, `limit`.
  - Fast autocomplete search by name or registration number.
- `GET /api/directory/filters`
  - Returns distinct states, cities, and registration statuses for UI filter dropdowns.

### Extraction Jobs
- `POST /api/jobs`
  - Request Body:
    ```json
    {
      "start_page": 1,
      "end_page": 5,
      "concurrency": 5,
      "requests_per_second": 2.0,
      "timeout_seconds": 30,
      "retry_count": 3,
      "mode": "live"
    }
    ```
  - Returns: `JobRead` object.
- `GET /api/jobs` — List past and active extraction jobs.
- `GET /api/jobs/{job_id}` — Get status and summary metrics for a specific job.
- `POST /api/jobs/{job_id}/cancel` — Cancel an in-flight background job.
- `POST /api/jobs/{job_id}/retry` — Retry failed pages or re-run extraction.
- `GET /api/jobs/{job_id}/events` — Server-Sent Events (SSE) streaming real-time job progress.
- `GET /api/jobs/{job_id}/records` — View records extracted by this job.
- `GET /api/jobs/{job_id}/errors` — View error logs for this job.
- `GET /api/jobs/{job_id}/export/csv` — Stream CSV export for this job.
- `GET /api/jobs/{job_id}/export/json` — Stream JSON export for this job.

### Analytics & Exports
- `GET /api/analytics` — Global statistics, state distributions, error distributions, and Data Quality Score.
- `GET /api/export/csv` — Global CSV streaming download of all records.
- `GET /api/export/json` — Global JSON streaming download of all records.
