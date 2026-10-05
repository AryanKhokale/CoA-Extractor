import React, { useEffect, useState } from 'react';
import { PageHeader } from '../components/common/PageHeader';
import { StatusBadge } from '../components/common/StatusBadge';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { directoryApi } from '../api/directory';
import { getExportUrl } from '../api/client';
import { ArchitectListResponse } from '../types';
import { Download, Search, ChevronLeft, ChevronRight, Copy, Check } from 'lucide-react';

export const DataPreviewPage: React.FC = () => {
  const [data, setData] = useState<ArchitectListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);
  const [query, setQuery] = useState('');
  const [copiedId, setCopiedId] = useState<number | null>(null);

  const loadRecords = async () => {
    setLoading(true);
    try {
      const res = await directoryApi.list({
        page,
        pageSize,
        query: query.trim() || undefined
      });
      setData(res);
    } catch (err) {
      console.error('Failed to load data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRecords();
  }, [page, pageSize]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    loadRecords();
  };

  const copyToClipboard = (text: string, id: number) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div>
      <PageHeader 
        title="Data Preview & Export"
        description="Inspect validated directory records and stream full exports directly in CSV or JSON format."
        actions={
          <div style={{ display: 'flex', gap: 'var(--spacing-sm)' }}>
            <a 
              href={getExportUrl('/export/csv')} 
              className="btn btn-secondary"
              download="all_coa_architects.csv"
            >
              <Download size={14} />
              <span>Download CSV</span>
            </a>
            <a 
              href={getExportUrl('/export/json')} 
              className="btn btn-secondary"
              download="all_coa_architects.json"
            >
              <Download size={14} />
              <span>Download JSON</span>
            </a>
          </div>
        }
      />

      {/* Search and Page Size Controls */}
      <div className="card" style={{ marginBottom: 'var(--spacing-md)' }}>
        <form onSubmit={handleSearchSubmit} style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: 'var(--spacing-md)', alignItems: 'center' }}>
          <div style={{ position: 'relative', width: '320px' }}>
            <input 
              type="text" 
              className="form-input" 
              placeholder="Search in preview..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              style={{ width: '100%', paddingLeft: '32px' }}
            />
            <Search size={16} color="var(--color-text-muted)" style={{ position: 'absolute', left: 10, top: 10 }} />
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
            <label className="form-label" style={{ marginBottom: 0 }}>Rows per page:</label>
            <select 
              className="form-select"
              value={pageSize}
              onChange={(e) => {
                setPageSize(parseInt(e.target.value));
                setPage(1);
              }}
            >
              <option value="25">25</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
          </div>
        </form>
      </div>

      {/* Table */}
      <div className="table-container">
        {loading ? (
          <div style={{ padding: 'var(--spacing-lg)' }}>
            <LoadingSkeleton rows={10} height={38} />
          </div>
        ) : !data || data.items.length === 0 ? (
          <div style={{ padding: 'var(--spacing-xl)', textAlign: 'center', color: 'var(--color-text-muted)' }}>
            No records available for preview.
          </div>
        ) : (
          <>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Reg Number</th>
                  <th>Architect Name</th>
                  <th>City</th>
                  <th>State</th>
                  <th>Validity</th>
                  <th>Year</th>
                  <th>Status</th>
                  <th>Copy</th>
                </tr>
              </thead>
              <tbody>
                {data.items.map((arch) => (
                  <tr key={arch.id}>
                    <td style={{ fontWeight: 'var(--font-weight-medium)', color: 'var(--color-primary)' }}>
                      {arch.registration_number}
                    </td>
                    <td>{arch.name}</td>
                    <td>{arch.city || '—'}</td>
                    <td>{arch.state || '—'}</td>
                    <td>{arch.valid_up_to || '—'}</td>
                    <td>{arch.registration_year || '—'}</td>
                    <td><StatusBadge status={arch.status} /></td>
                    <td>
                      <button 
                        className="btn btn-secondary btn-sm"
                        onClick={() => copyToClipboard(`${arch.name} (${arch.registration_number}) - ${arch.city || ''}, ${arch.state || ''}`, arch.id)}
                        title="Copy to clipboard"
                      >
                        {copiedId === arch.id ? <Check size={12} color="var(--color-success)" /> : <Copy size={12} />}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="pagination-bar">
              <div>
                Showing {((data.page - 1) * data.page_size) + 1}–{Math.min(data.page * data.page_size, data.total)} of {data.total.toLocaleString()} records
              </div>
              <div className="pagination-controls">
                <button 
                  className="btn btn-secondary btn-sm"
                  disabled={data.page <= 1}
                  onClick={() => setPage(page - 1)}
                >
                  <ChevronLeft size={14} />
                  <span>Previous</span>
                </button>
                <span style={{ margin: '0 var(--spacing-xs)' }}>Page {data.page} of {data.total_pages}</span>
                <button 
                  className="btn btn-secondary btn-sm"
                  disabled={data.page >= data.total_pages}
                  onClick={() => setPage(page + 1)}
                >
                  <span>Next</span>
                  <ChevronRight size={14} />
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};
