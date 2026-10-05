import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { PageHeader } from '../components/common/PageHeader';
import { StatusBadge } from '../components/common/StatusBadge';
import { JobProgressCard } from '../components/jobs/JobProgressCard';
import { NewJobModal } from '../components/jobs/NewJobModal';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { EmptyState } from '../components/common/EmptyState';
import { jobsApi } from '../api/jobs';
import { getExportUrl } from '../api/client';
import { Job } from '../types';
import { Play, RotateCcw, Download, Eye, Layers } from 'lucide-react';

export const JobsPage: React.FC = () => {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const loadJobs = async () => {
    try {
      const data = await jobsApi.list(50);
      setJobs(data);
    } catch (err) {
      console.error('Failed to load jobs', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadJobs();
    const interval = setInterval(loadJobs, 8000);
    return () => clearInterval(interval);
  }, []);

  const activeJobs = jobs.filter((j) => j.status === 'RUNNING' || j.status === 'PENDING');
  const pastJobs = jobs.filter((j) => j.status !== 'RUNNING' && j.status !== 'PENDING');

  return (
    <div>
      <PageHeader 
        title="Extraction Jobs" 
        description="Monitor, schedule, and review asynchronous Council of Architecture public directory extraction runs."
        actions={
          <button className="btn btn-primary" onClick={() => setIsModalOpen(true)}>
            <Play size={16} />
            <span>New Extraction Job</span>
          </button>
        }
      />

      {/* Active Jobs Live Cards */}
      {activeJobs.length > 0 && (
        <div style={{ marginBottom: 'var(--spacing-xl)' }}>
          <h2 style={{ fontSize: 'var(--font-size-base)', fontWeight: 'var(--font-weight-semibold)', marginBottom: 'var(--spacing-sm)' }}>
            Active Extraction Tasks ({activeJobs.length})
          </h2>
          {activeJobs.map((job) => (
            <JobProgressCard key={job.id} job={job} onJobUpdated={loadJobs} />
          ))}
        </div>
      )}

      {/* Job Execution History */}
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Job History</h2>
            <p className="card-subtitle">All historical extraction runs with audit metrics</p>
          </div>
        </div>

        {loading && jobs.length === 0 ? (
          <div style={{ padding: 'var(--spacing-lg)' }}>
            <LoadingSkeleton rows={5} height={42} />
          </div>
        ) : jobs.length === 0 ? (
          <EmptyState 
            title="No Extraction Jobs Yet"
            message="Configure and trigger your first extraction job to collect public CoA directory records."
            action={
              <button className="btn btn-primary" onClick={() => setIsModalOpen(true)}>
                <Play size={14} />
                <span>Create Extraction Job</span>
              </button>
            }
          />
        ) : (
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Job ID</th>
                  <th>Status</th>
                  <th>Mode</th>
                  <th>Page Range</th>
                  <th>Processed</th>
                  <th>Success</th>
                  <th>Duplicates</th>
                  <th>Failed</th>
                  <th>Speed</th>
                  <th>Data Quality</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {jobs.map((job) => (
                  <tr key={job.id}>
                    <td style={{ fontWeight: 'var(--font-weight-medium)', color: 'var(--color-primary)' }}>
                      #{job.id}
                    </td>
                    <td>
                      <StatusBadge status={job.status} />
                    </td>
                    <td>
                      <span className={`badge ${job.mode === 'live' ? 'badge-info' : 'badge-warning'}`}>
                        {job.mode.toUpperCase()}
                      </span>
                    </td>
                    <td>Pages {job.start_page}–{job.end_page}</td>
                    <td>{job.processed_records.toLocaleString()}</td>
                    <td style={{ color: 'var(--color-success)', fontWeight: 'var(--font-weight-medium)' }}>
                      {job.successful_records.toLocaleString()}
                    </td>
                    <td style={{ color: 'var(--color-warning)' }}>
                      {job.duplicate_records.toLocaleString()}
                    </td>
                    <td style={{ color: job.failed_records > 0 ? 'var(--color-danger)' : 'inherit' }}>
                      {job.failed_records.toLocaleString()}
                    </td>
                    <td>{job.speed_records_per_sec} rec/s</td>
                    <td>
                      <strong>{job.data_quality_score}%</strong>
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '4px' }}>
                        <button 
                          className="btn btn-secondary btn-sm"
                          onClick={() => navigate(`/jobs/${job.id}`)}
                          title="View Records & Errors"
                        >
                          <Eye size={12} />
                          <span>View</span>
                        </button>

                        {job.status === 'COMPLETED' && (
                          <a 
                            href={getExportUrl(`/jobs/${job.id}/export/csv`)} 
                            className="btn btn-secondary btn-sm"
                            download={`coa_${job.id}.csv`}
                            title="Download CSV"
                          >
                            <Download size={12} />
                          </a>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <NewJobModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)}
        onJobCreated={loadJobs}
      />
    </div>
  );
};
