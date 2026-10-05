# Council of Architecture (CoA) Public Directory Analysis

## Executive Summary
This document provides an empirical analysis of the Council of Architecture (CoA) official web portal (`https://www.coa.gov.in`), conducted by directly inspecting HTTP headers, network endpoints, form structures, DOM hierarchies, session handlers, and anti-abuse mechanisms.

The Council of Architecture is a statutory body constituted by the Government of India under the Architects Act, 1972, tasked with maintaining the official Register of Architects.

---

## 1. Target URLs & Directory Endpoints

| Resource | Target URL | HTTP Method | Auth / Access Requirements |
| :--- | :--- | :--- | :--- |
| **Main Portal** | `https://www.coa.gov.in` | `GET` | Public |
| **Public Directory (Register / Inactive / Defaulter list)** | `https://www.coa.gov.in/default_arch.php` | `GET` | Public, No Session Required |
| **Directory Pagination** | `https://www.coa.gov.in/default_arch.php?page={N}&lang=1` | `GET` | Public, Sequential or Random Access |
| **Search Directory** | `https://www.coa.gov.in/search_arch.php` | `GET` | Public Landing Page |
| **Search Sub-Forms** | `https://www.coa.gov.in/search_arch2.php?searCat={1-6}` | `GET` | 3 Searches/Day IP quota; Session Captcha |
| **Architect Verification** | `https://www.coa.gov.in/ver_arch.php?lang=1` | `GET` / `POST` | Security code (captcha) verification |
| **Council Member Directory** | `https://www.coa.gov.in/member_list.php?lang=1` | `GET` | Public, Server-side rendered table |
| **State Distribution Statistics** | `https://www.coa.gov.in/index1.php?lang=1&level=1&sublinkid=376&lid=330` | `GET` | Public, Authoritative breakdown |
| **Yearwise Registration Statistics** | `https://www.coa.gov.in/index1.php?lang=1&level=1&sublinkid=37&lid=50` | `GET` | Public, 1975–2026 registration totals |
| **City Distribution Statistics** | `https://www.coa.gov.in/index1.php?lang=1&level=1&sublinkid=32&lid=45` | `GET` | Public, Cities with >500 architects |

---

## 2. Directory Structure & Mechanics

### 2.1 Public Directory (`default_arch.php`)
- **Rendering Model**: Server-side rendered PHP delivering plain HTML tables.
- **Record Batching**: 50 records per page.
- **Total Depth**: 998+ discovered pages (>49,900 indexed architect records).
- **Pagination Mechanism**: URL query parameter `page={N}`.
- **JavaScript Dependency**: Minimal. The table is rendered directly in the initial HTML payload inside `<div id="cmscontent2">`. Client-side script only toggles filter tabs (`w3AddClass` / `w3RemoveClass`).
- **Access Restrictions**: Does not enforce session tokens or IP search quotas on `default_arch.php`, making it the most reliable, stable, and high-throughput endpoint for public directory extraction.

### 2.2 Search Directory (`search_arch2.php`)
- **Categories Supported (`searCat`)**:
  1. Name (`arc_name`, `m_name`, `l_name`)
  2. Year of Registration (`arc_reg_date`)
  3. Registration Number (`arc_reg`)
  4. State (`state_id`)
  5. City
  6. Pincode
- **Protection Model**: Enforces a strict quota of 3 free searches per day per IP address (`"You can opt for three searches per day from an IP address without subscription"`). Requires session cookies (`PHPSESSID`) and a 6-character captcha challenge (`T3` & `cap_code`). Captcha reload queries `app/admin/captcha/php_captcha.php` and `ajax_captcha.php`.
- **Target Action**: POSTs to `search_architectResult.php`. If unauthenticated or exceeding quota, returns a JavaScript redirect `<script>window.location="search_arch.php..."</script>`.

---

## 3. Discovered Data Fields

Empirical inspection of table headers and DOM rows reveals the following schema:

| Field Name | Type | Example Value | Description |
| :--- | :--- | :--- | :--- |
| `serial_no` | Integer / String | `1`, `42` | Sequence index on page |
| `registration_number`| String | `CA/1975/00005` | Standard Council of Architecture registration code (`CA/{YYYY}/{NNNNN}`) |
| `name` | String | `Mr. N.T. VENKATESH` | Full legal name including title (`Mr.`, `Ms.`, `Ar.`, `Dr.`) |
| `city` | String | `Bengaluru`, `Mumbai` | Primary practice city |
| `state` | String | `Karnataka`, `Maharashtra` | Indian state / union territory |
| `valid_up_to` | Date (DD/MM/YYYY) | `31/12/1979`, `31/12/2026` | Renewal validity expiration date |
| `registration_year` | Integer | `1975`, `2021` | Inferred from registration number or registration date |
| `status` | String | `Defaulter`, `Inactive`, `Active` | Current registration standing |
| `raw_data` | JSON | `{...}` | Complete unparsed raw record for auditability |

---

## 4. Extraction Strategy

To achieve **high-speed**, **reliable**, and **responsible** extraction without overloading public infrastructure or triggering anti-bot firewalls:

1. **Dual-Adapter Architecture**:
   - `CoADirectoryAdapter`: Live HTTP adapter extracting from `default_arch.php` with bounded concurrency.
   - `MockDirectoryAdapter`: High-fidelity synthetic generator using real CoA statistical distributions for development, CI/CD, and offline demonstrations.

2. **Asynchronous Bounded Concurrency**:
   - `asyncio.Semaphore(MAX_CONCURRENCY)` (safe default: 3–5 concurrent connections).
   - Single persistent `httpx.AsyncClient` utilizing HTTP keep-alive connection pooling.

3. **Adaptive Rate Limiting**:
   - Token-bucket algorithm enforcing `REQUESTS_PER_SECOND` (safe default: 2.0 req/sec).
   - Proactive delay jitter (0.1–0.3s) to mimic natural traffic and prevent synchronized bursts.

4. **Failure & Retry Protocol**:
   - Intercept HTTP 429, 500, 502, 503, 504 and network timeouts.
   - Parse `Retry-After` header if present.
   - Exponential backoff with jitter: $t_{\text{wait}} = \min(2^{\text{attempt}} + \text{jitter}, 30\text{s})$.
   - Automatic concurrency throttle if multiple consecutive rate-limit responses occur.

---

## 5. Parser Strategy

- **HTML Parsing**: Robust extraction using BeautifulSoup4 with Python's standard `html.parser` for zero-dependency overhead.
- **Selector Path**:
  - Target table: `table[cellpadding="5"]` located inside `#cmscontent2`.
  - Header validation: Inspect `th` elements for `['Sl.', 'Name', 'Registration Number', 'City', 'Valid up to']`.
  - Row extraction: Loop through `tr` tags skipping header index 0.
  - Cell mapping: Extract text from `td` spans, stripping excessive whitespace and Unicode non-breaking spaces (`&nbsp;` / `\xa0`).

---

## 6. Potential Failure Points & Mitigations

| Failure Point | Manifestation | Mitigation Strategy |
| :--- | :--- | :--- |
| **IP Quota on Search** | Redirect to `search_arch.php` | Primary extraction utilizes public paginated directory `default_arch.php` which has no IP quota. |
| **Site Outage / Maintenance** | HTTP 500/503 or Connection Refused | Circuit-breaker flags job as PAUSED/FAILED; UI offers one-click retry; Development/Mock mode available. |
| **HTML Schema Change** | Missing table or column count mismatch | Schema validator emits structured `PARSE_ERROR`, records failed page number, and prevents corrupt inserts. |
| **Transient Latency Spikes** | Request timeout (>30s) | Configurable async timeouts with bounded exponential backoff retries. |

---

## 7. Validation & Normalization Rules

1. **Registration Number**: Must match regex `^CA\/\d{4}\/\d{1,6}$` or conform to CoA alphanumeric format.
2. **Name**: Clean Honorifics (`Ar.`, `Mr.`, `Ms.`, `Mrs.`, `Dr.`), trim redundant internal whitespace, Title Case.
3. **Location (City/State)**: Normalize city naming (e.g. `Bangalore` -> `Bengaluru`, `Bombay` -> `Mumbai`, `Calcutta` -> `Kolkata`), map city to standard Indian State table.
4. **Dates**: Normalize `DD/MM/YYYY` strings into ISO `YYYY-MM-DD` standard.
5. **Deduplication**: Hash unique key `registration_number.upper().strip()`. Secondary composite fallback `(normalized_name, city, state)`.
