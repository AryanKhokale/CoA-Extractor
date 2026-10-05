import React, { useEffect, useState } from 'react';
import { PageHeader } from '../components/common/PageHeader';
import { StatusBadge } from '../components/common/StatusBadge';
import { Modal } from '../components/common/Modal';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { EmptyState } from '../components/common/EmptyState';
import { directoryApi, DirectoryFilterParams } from '../api/directory';
import { Architect, ArchitectListResponse } from '../types';
import { Search, Filter, ChevronLeft, ChevronRight, Eye, User, MapPin, Calendar, Award } from 'lucide-react';

export const DirectoryPage: React.FC = () => {
  const [data, setData] = useState<ArchitectListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<{ states: string[]; cities: string[]; statuses: string[] }>({
    states: [],
    cities: [],
    statuses: []
  });

  const [params, setParams] = useState<DirectoryFilterParams>({
    query: '',
    state: 'All',
    city: 'All',
    status: 'All',
    sortBy: 'registration_number',
    sortOrder: 'asc',
    page: 1,
    pageSize: 25
  });

  const [selectedArchitect, setSelectedArchitect] = useState<Architect | null>(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await directoryApi.list(params);
      setData(res);
    } catch (err) {
      console.error('Failed to load directory data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    directoryApi.getFilters().then(setFilters).catch(() => null);
  }, []);

  useEffect(() => {
    loadData();
  }, [params.page, params.state, params.city, params.status, params.sortBy, params.sortOrder]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setParams((prev) => ({ ...prev, page: 1 }));
    loadData();
  };

  return (
    <div>
      <PageHeader 
        title="Architect Directory Explorer" 
        description="Search and filter verified Council of Architecture registrants across all Indian states and territories."
      />

      {/* Filter and Search Bar */}
      <div className="card" style={{ marginBottom: 'var(--spacing-lg)' }}>
        <form onSubmit={handleSearchSubmit}>
          <div style={{ display: 'flex', gap: 'var(--spacing-md)', flexWrap: 'wrap', alignItems: 'flex-end' }}>
            <div className="form-group" style={{ flex: '1 1 280px', marginBottom: 0 }}>
              <label className="form-label">Search Architect</label>
              <div style={{ position: 'relative' }}>
                <input 
                  type="text" 
                  className="form-input" 
                  placeholder="Search by name, CA/YYYY/XXXXX, or city..."
                  value={params.query || ''}
                  onChange={(e) => setParams({ ...params, query: e.target.value })}
                  style={{ width: '100%', paddingLeft: '32px' }}
                />
                <Search size={16} color="var(--color-text-muted)" style={{ position: 'absolute', left: 10, top: 10 }} />
              </div>
            </div>

            <div className="form-group" style={{ flex: '1 1 180px', marginBottom: 0 }}>
              <label className="form-label">State</label>
              <select 
                className="form-select"
                value={params.state || 'All'}
                onChange={(e) => setParams({ ...params, state: e.target.value, page: 1 })}
              >
                <option value="All">All States</option>
                {filters.states.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>

            <div className="form-group" style={{ flex: '1 1 160px', marginBottom: 0 }}>
              <label className="form-label">Status</label>
              <select 
                className="form-select"
                value={params.status || 'All'}
                onChange={(e) => setParams({ ...params, status: e.target.value, page: 1 })}
              >
                <option value="All">All Statuses</option>
                {filters.statuses.map((st) => (
                  <option key={st} value={st}>{st}</option>
                ))}
              </select>
            </div>

            <button type="submit" className="btn btn-primary" style={{ height: '38px' }}>
              <Search size={16} />
              <span>Search</span>
            </button>
          </div>
        </form>
      </div>

      {/* Directory Table */}
      <div className="table-container">
        {loading ? (
          <div style={{ padding: 'var(--spacing-lg)' }}>
            <LoadingSkeleton rows={10} height={38} />
          </div>
        ) : !data || data.items.length === 0 ? (
          <EmptyState 
            title="No Architects Found"
            message="No registered architects match the selected search criteria. Try modifying your search query or reset the filters."
            action={
              <button 
                className="btn btn-secondary" 
                onClick={() => setParams({ query: '', state: 'All', city: 'All', status: 'All', page: 1, pageSize: 25 })}
              >
                Reset Filters
              </button>
            }
          />
        ) : (
          <>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Registration No.</th>
                  <th>Architect Name</th>
                  <th>City</th>
                  <th>State</th>
                  <th>Valid Up To</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {data.items.map((arch) => (
                  <tr key={arch.id} style={{ cursor: 'pointer' }} onClick={() => setSelectedArchitect(arch)}>
                    <td style={{ fontWeight: 'var(--font-weight-medium)', color: 'var(--color-primary)' }}>
                      {arch.registration_number}
                    </td>
                    <td style={{ fontWeight: 'var(--font-weight-medium)' }}>
                      {arch.name}
                    </td>
                    <td>{arch.city || '—'}</td>
                    <td>{arch.state || '—'}</td>
                    <td>{arch.valid_up_to || '—'}</td>
                    <td>
                      <StatusBadge status={arch.status} />
                    </td>
                    <td>
                      <button 
                        className="btn btn-secondary btn-sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedArchitect(arch);
                        }}
                      >
                        <Eye size={12} />
                        <span>Details</span>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Pagination Controls */}
            <div className="pagination-bar">
              <div>
                Showing {((data.page - 1) * data.page_size) + 1}–{Math.min(data.page * data.page_size, data.total)} of {data.total.toLocaleString()} records
              </div>

              <div className="pagination-controls">
                <button 
                  className="btn btn-secondary btn-sm"
                  disabled={data.page <= 1}
                  onClick={() => setParams((p) => ({ ...p, page: (p.page || 1) - 1 }))}
                >
                  <ChevronLeft size={14} />
                  <span>Previous</span>
                </button>

                <span style={{ margin: '0 var(--spacing-xs)' }}>
                  Page {data.page} of {data.total_pages}
                </span>

                <button 
                  className="btn btn-secondary btn-sm"
                  disabled={data.page >= data.total_pages}
                  onClick={() => setParams((p) => ({ ...p, page: (p.page || 1) + 1 }))}
                >
                  <span>Next</span>
                  <ChevronRight size={14} />
                </button>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Architect Detail Modal */}
      <Modal 
        isOpen={!!selectedArchitect} 
        onClose={() => setSelectedArchitect(null)}
        title="Council of Architecture Record"
      >
        {selectedArchitect && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-md)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingBottom: 'var(--spacing-sm)', borderBottom: '1px solid var(--color-border)' }}>
              <div>
                <h3 style={{ fontSize: 'var(--font-size-lg)', fontWeight: 'var(--font-weight-bold)' }}>
                  {selectedArchitect.name}
                </h3>
                <span style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-primary)', fontWeight: 'var(--font-weight-semibold)' }}>
                  {selectedArchitect.registration_number}
                </span>
              </div>
              <StatusBadge status={selectedArchitect.status} />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 'var(--spacing-md)' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--color-text-muted)', fontSize: 'var(--font-size-xs)' }}>
                  <MapPin size={14} />
                  <span>LOCATION</span>
                </div>
                <div style={{ fontWeight: 'var(--font-weight-medium)', marginTop: '4px' }}>
                  {selectedArchitect.city || '—'}, {selectedArchitect.state || '—'}
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--color-text-muted)', fontSize: 'var(--font-size-xs)' }}>
                  <Calendar size={14} />
                  <span>REGISTRATION YEAR / VALIDITY</span>
                </div>
                <div style={{ fontWeight: 'var(--font-weight-medium)', marginTop: '4px' }}>
                  {selectedArchitect.registration_year || '—'} (Valid up to: {selectedArchitect.valid_up_to || '—'})
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--color-text-muted)', fontSize: 'var(--font-size-xs)' }}>
                  <Award size={14} />
                  <span>QUALIFICATION</span>
                </div>
                <div style={{ fontWeight: 'var(--font-weight-medium)', marginTop: '4px' }}>
                  {selectedArchitect.qualification || 'B.Arch (Council of Architecture Recognized)'}
                </div>
              </div>
            </div>

            {selectedArchitect.address && (
              <div>
                <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>REGISTERED ADDRESS</span>
                <p style={{ marginTop: '4px', fontSize: 'var(--font-size-sm)', backgroundColor: 'var(--color-bg-base)', padding: 'var(--spacing-sm)', borderRadius: 'var(--radius-sm)' }}>
                  {selectedArchitect.address}
                </p>
              </div>
            )}

            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 'var(--spacing-md)' }}>
              <button className="btn btn-secondary" onClick={() => setSelectedArchitect(null)}>
                Close
              </button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};
