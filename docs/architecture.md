# System Architecture

## Overview
The Council of Architecture (CoA) Directory Data Extraction & High-Speed Pipeline is a production-grade, asynchronous web harvesting, normalization, and analytics platform. It is engineered to process public records from the Council of Architecture statutory registry (`coa.gov.in`) with bounded concurrency, adaptive rate limiting, duplicate detection, and streaming exports.

```mermaid
flowchart TD
    subgraph Frontend["React 19 Frontend (Vercel)"]
        UI["Plain CSS Custom Design System"]
        Router["React Router v7"]
        SSEListener["EventSource SSE Consumer"]
    end

    subgraph Backend["FastAPI Monolith (Render)"]
        API["FastAPI REST & Streaming Endpoints"]
        JM["JobManager (Asyncio Orchestrator)"]
        RL["Token-Bucket Rate Limiter"]
        Adapter["CoADirectoryAdapter / MockDirectoryAdapter"]
        Pipeline["Validation & Normalization Pipeline"]
        Dedup["O(1) In-Memory & Database Deduplicator"]
        Scorer["DataQualityScorer (4 Pillars)"]
    end

    subgraph Persistence["Storage Layer"]
        DB[("PostgreSQL / SQLite Storage")]
        CSVExport["Chunked Streaming CSV"]
        JSONExport["Chunked Streaming JSON"]
    end

    subgraph Target["Official Source"]
        CoA["CoA Public Portal (default_arch.php)"]
    end

    UI --> API
    SSEListener <-->|SSE Progress Events| API
    API --> JM
    JM --> Adapter
    Adapter --> RL
    RL --> CoA
    CoA -->|HTML Payload| Adapter
    Adapter --> Pipeline
    Pipeline --> Dedup
    Dedup --> DB
    DB --> Scorer
    DB --> CSVExport
    DB --> JSONExport
```

## Key Architectural Decisions

1. **Modular Monolith for Zero-Cost Deployment**:
   - Single FastAPI backend service eliminates the operational overhead and memory consumption of microservices, Kafka, or external Redis queues.
   - Built to run seamlessly within free-tier compute boundaries (e.g. Render 512MB RAM, Vercel Serverless).

2. **Adaptive Token-Bucket Rate Limiter**:
   - Strictly enforces requests-per-second constraints (`REQUESTS_PER_SECOND=2.0`).
   - Dynamically backs off upon encountering HTTP 429 status codes and honors `Retry-After` headers.

3. **In-Flight Deduplication**:
   - Registration numbers (`CA/YYYY/NNNNN`) serve as primary unique keys.
   - Composite keys `(normalized_name, city)` prevent corrupt or re-issued entry collision.

4. **Zero-Memory Streaming Exports**:
   - Database queries use SQLAlchemy's `yield_per()` to stream CSV and JSON directly to the client without buffering entire datasets in memory.
