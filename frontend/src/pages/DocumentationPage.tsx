import React from 'react';
import { PageHeader } from '../components/common/PageHeader';
import { BookOpen, ShieldCheck, Database, Server, Cpu, ExternalLink } from 'lucide-react';

export const DocumentationPage: React.FC = () => {
  return (
    <div>
      <PageHeader 
        title="System Documentation & Architecture"
        description="Comprehensive technical guide to the Council of Architecture (CoA) extraction engine, schema normalization, and responsible data harvesting."
      />

      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-xl)', maxWidth: '900px' }}>
        
        {/* Source Analysis Summary */}
        <div className="card">
          <h2 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)', marginBottom: 'var(--spacing-sm)' }}>
            <Server size={18} color="var(--color-primary)" />
            <span>Council of Architecture Source Architecture</span>
          </h2>
          <p style={{ color: 'var(--color-text-secondary)', lineHeight: 1.6, fontSize: 'var(--font-size-sm)', marginBottom: 'var(--spacing-md)' }}>
            The Council of Architecture (CoA) is a statutory authority established by the Government of India under the Architects Act, 1972. It maintains the official National Register of Architects.
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 'var(--spacing-md)' }}>
            <div style={{ padding: 'var(--spacing-md)', backgroundColor: 'var(--color-bg-base)', borderRadius: 'var(--radius-md)' }}>
              <strong>Public Directory Endpoint</strong>
              <p style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)', marginTop: '4px' }}>
                <code>https://www.coa.gov.in/default_arch.php</code>
              </p>
              <span className="badge badge-success" style={{ marginTop: '6px' }}>50 records/page (998+ pages)</span>
            </div>

            <div style={{ padding: 'var(--spacing-md)', backgroundColor: 'var(--color-bg-base)', borderRadius: 'var(--radius-md)' }}>
              <strong>Search & Verification</strong>
              <p style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)', marginTop: '4px' }}>
                <code>search_arch2.php</code> / <code>ver_arch.php</code>
              </p>
              <span className="badge badge-warning" style={{ marginTop: '6px' }}>Protected by IP quota (3 searches/day)</span>
            </div>
          </div>
        </div>

        {/* Pipeline Mechanics */}
        <div className="card">
          <h2 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)', marginBottom: 'var(--spacing-sm)' }}>
            <Cpu size={18} color="var(--color-primary)" />
            <span>High-Speed Extraction & Processing Pipeline</span>
          </h2>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-md)', marginTop: 'var(--spacing-md)' }}>
            <div style={{ display: 'flex', gap: 'var(--spacing-md)', alignItems: 'flex-start' }}>
              <span className="badge badge-info" style={{ minWidth: '80px', justifyContent: 'center' }}>Step 1: Fetch</span>
              <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)' }}>
                Asynchronous network I/O with <code>httpx.AsyncClient</code>, HTTP keep-alive connection pooling, and token-bucket rate limiting (2.0 req/s, 5 concurrent workers).
              </p>
            </div>

            <div style={{ display: 'flex', gap: 'var(--spacing-md)', alignItems: 'flex-start' }}>
              <span className="badge badge-info" style={{ minWidth: '80px', justifyContent: 'center' }}>Step 2: Parse</span>
              <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)' }}>
                Robust DOM parser extracting serial numbers, full architect names, standard registration numbers, cities, and validity expiration dates.
              </p>
            </div>

            <div style={{ display: 'flex', gap: 'var(--spacing-md)', alignItems: 'flex-start' }}>
              <span className="badge badge-info" style={{ minWidth: '80px', justifyContent: 'center' }}>Step 3: Validate</span>
              <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)' }}>
                Rigorous Pydantic schema validation requiring non-empty names and strict regex pattern match <code>^CA\/\d&#123;4&#125;\/\d&#123;1,6&#125;$</code>.
              </p>
            </div>

            <div style={{ display: 'flex', gap: 'var(--spacing-md)', alignItems: 'flex-start' }}>
              <span className="badge badge-info" style={{ minWidth: '80px', justifyContent: 'center' }}>Step 4: Normalize</span>
              <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)' }}>
                Unicode NFKC normalization, whitespace collapse, Title Casing with honorific preservation (Ar., Mr., Ms., Dr.), and Indian state inference from city mappings.
              </p>
            </div>

            <div style={{ display: 'flex', gap: 'var(--spacing-md)', alignItems: 'flex-start' }}>
              <span className="badge badge-info" style={{ minWidth: '80px', justifyContent: 'center' }}>Step 5: Deduplicate</span>
              <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)' }}>
                High-speed O(1) in-memory index against database records using canonical registration number as primary key and composite <code>(name, city)</code> as fallback.
              </p>
            </div>

            <div style={{ display: 'flex', gap: 'var(--spacing-md)', alignItems: 'flex-start' }}>
              <span className="badge badge-info" style={{ minWidth: '80px', justifyContent: 'center' }}>Step 6: Stream</span>
              <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)' }}>
                Live real-time progress broadcasted to user browser via Server-Sent Events (SSE). Chunked streaming CSV and JSON exports for arbitrarily large datasets.
              </p>
            </div>
          </div>
        </div>

        {/* REST API Endpoints */}
        <div className="card">
          <h2 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)', marginBottom: 'var(--spacing-sm)' }}>
            <Database size={18} color="var(--color-primary)" />
            <span>FastAPI REST Endpoints</span>
          </h2>
          
          <table className="data-table" style={{ marginTop: 'var(--spacing-sm)' }}>
            <thead>
              <tr>
                <th>Method</th>
                <th>Path</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><span className="badge badge-success">GET</span></td>
                <td><code>/api/health</code></td>
                <td>Health check and service status</td>
              </tr>
              <tr>
                <td><span className="badge badge-success">GET</span></td>
                <td><code>/api/directory/architects</code></td>
                <td>Search and filter directory with pagination</td>
              </tr>
              <tr>
                <td><span className="badge badge-info">POST</span></td>
                <td><code>/api/jobs</code></td>
                <td>Create and start asynchronous extraction job</td>
              </tr>
              <tr>
                <td><span className="badge badge-success">GET</span></td>
                <td><code>/api/jobs/&#123;id&#125;/events</code></td>
                <td>Server-Sent Events real-time progress stream</td>
              </tr>
              <tr>
                <td><span className="badge badge-success">GET</span></td>
                <td><code>/api/analytics</code></td>
                <td>State distributions and Data Quality Score</td>
              </tr>
              <tr>
                <td><span className="badge badge-success">GET</span></td>
                <td><code>/api/export/csv</code></td>
                <td>Streaming CSV download of all records</td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>
    </div>
  );
};
