import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { PageHeader } from '../components/common/PageHeader';
import { JobProgressCard } from '../components/jobs/JobProgressCard';
import { StatusBadge } from '../components/common/StatusBadge';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { EmptyState } from '../components/common/EmptyState';
import { jobsApi } from '../api/jobs';
import { Job, ArchitectListResponse } from '../types';
import { ArrowLeft, Table, AlertOctagon, ChevronLeft, ChevronRight } from 'lucide-react';

export const JobDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [job, setJob] = useState<Job | null>(null);
  const [records, setRecords] = useState<ArchitectListResponse | null>(null);
  const [errors, setErrors] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<'records' | 'errors'>('records');
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);

  const loadJobDetails = async () => {
    if (!id) return;
    try {
      const [jobData, recordsData, errorsData] = await Promise.all([
        jobsApi.get(id),
        jobsApi.getRecords(id, page, 25),
        jobsApi.getErrors(id)
      ]);
      setJob(jobData);
      setRecords(recordsData);
      setErrors(errorsData);
    } catch (err) {
      console.error('Failed to load job details', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadJobDetails();
  }, [id, page]);

  if (loading && !job) {
    return (
      <div>
        <PageHeader title="Job Details" />
        <LoadingSkeleton rows={6} height={40} />
      </div>
    );
  }

  if (!job) {
    return (
      <EmptyState 
        title="Job Not Found" 
        message={`Extraction job #${id} could not be located.`}
        action={
          <button className="btn btn-secondary" onClick={() => navigate('/jobs')}>
            <ArrowLeft size={14} />
            <span>Back to Jobs</span>
          </button>
        }
      />
    );
  }

  return (
    <div>
      <PageHeader 
        title={`Extraction Job #${job.id}`}
        description={`Run scope: Pages ${job.start_page} to ${job.end_page} (${job.mode.toUpperCase()} mode)`}
        actions={
          <button className="btn btn-secondary" onClick={() => navigate('/jobs')}>
            <ArrowLeft size={16} />
            <span>All Jobs</span>
          </button>
        }
      />

      <JobProgressCard job={job} onJobUpdated={loadJobDetails} />

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 'var(--spacing-sm)', marginBottom: 'var(--spacing-md)' }}>
        <button 
          className={`btn ${activeTab === 'records' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveTab('records')}
        >
          <Table size={14} />
          <span>Extracted Records ({records?.total.toLocaleString() || 0})</span>
        </button>

        <button 
          className={`btn ${activeTab === 'errors' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveTab('errors')}
        >
          <AlertOctagon size={14} />
          <span>Extraction Errors ({errors.length})</span>
        </button>
      </div>

      {activeTab === 'records' ? (
        <div className="table-container">
          {!records || records.items.length === 0 ? (
            <div style={{ padding: 'var(--spacing-xl)', textAlign: 'center', color: 'var(--color-text-muted)' }}>
              No records extracted for this job yet.
            </div>
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
                  </tr>
                </thead>
                <tbody>
                  {records.items.map((arch) => (
                    <tr key={arch.id}>
                      <td style={{ fontWeight: 'var(--font-weight-medium)', color: 'var(--color-primary)' }}>
                        {arch.registration_number}
                      </td>
                      <td>{arch.name}</td>
                      <td>{arch.city || '—'}</td>
                      <td>{arch.state || '—'}</td>
                      <td>{arch.valid_up_to || '—'}</td>
                      <td><StatusBadge status={arch.status} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="pagination-bar">
                <div>
                  Showing {((records.page - 1) * records.page_size) + 1}–{Math.min(records.page * records.page_size, records.total)} of {records.total.toLocaleString()} records
                </div>
                <div className="pagination-controls">
                  <button 
                    className="btn btn-secondary btn-sm"
                    disabled={records.page <= 1}
                    onClick={() => setPage(page - 1)}
                  >
                    <ChevronLeft size={14} />
                    <span>Previous</span>
                  </button>
                  <span style={{ margin: '0 var(--spacing-xs)' }}>Page {records.page} of {records.total_pages}</span>
                  <button 
                    className="btn btn-secondary btn-sm"
                    disabled={records.page >= records.total_pages}
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
      ) : (
        <div className="table-container">
          {errors.length === 0 ? (
            <div style={{ padding: 'var(--spacing-xl)', textAlign: 'center', color: 'var(--color-success)' }}>
              No extraction errors encountered! Pipeline execution was 100% clean.
            </div>
          ) : (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Page</th>
                  <th>Error Type</th>
                  <th>Identifier</th>
                  <th>Message</th>
                  <th>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {errors.map((err) => (
                  <tr key={err.id}>
                    <td>Page {err.page || '—'}</td>
                    <td>
                      <span className="badge badge-danger">{err.error_type}</span>
                    </td>
                    <td>{err.record_identifier || '—'}</td>
                    <td style={{ color: 'var(--color-danger-text)', maxWidth: '400px', whiteSpace: 'normal' }}>
                      {err.error_message}
                    </td>
                    <td style={{ color: 'var(--color-text-muted)' }}>
                      {new Date(err.created_at).toLocaleTimeString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
};
