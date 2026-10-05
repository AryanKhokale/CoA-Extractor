# Responsible Extraction & Ethical Use Policy

## Statutory Context
The Council of Architecture (CoA) is a statutory authority established under the Architects Act, 1972 by the Government of India. The public register maintained by CoA is intended for public verification of licensed professionals.

## Technical Safeguards Implemented

To ensure respectful and non-disruptive access to public government resources:

1. **Strictly Bounded Concurrency**:
   - Concurrency is hard-capped at a safe maximum of 5–10 simultaneous workers.
   - Unbounded asynchronous loops (e.g. `asyncio.gather(*thousands)`) are strictly prohibited.

2. **Token-Bucket Rate Limiting**:
   - Default pacing of 2.0 requests per second prevents burst loads on the target web server.

3. **Adaptive Backoff on HTTP 429**:
   - The engine monitors HTTP 429 status codes, respects `Retry-After` headers, and automatically slows down if repeat rate limit responses occur.

4. **Public Endpoint Utilization**:
   - The pipeline targets the openly published paginated directory `default_arch.php` rather than brute-forcing forms requiring captchas or subscription credentials.
   - The engine does NOT bypass authentication, defeat security controls, or circumvent access restrictions.

5. **Offline Mock Mode**:
   - For educational exploration, continuous integration, and user interface testing, developers should utilize the pre-packaged Mock Mode (`mock_data/architects.json`) instead of querying live government infrastructure repeatedly.
