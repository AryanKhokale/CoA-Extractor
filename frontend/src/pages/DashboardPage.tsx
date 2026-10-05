import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { PageHeader } from '../components/common/PageHeader';
import { StatCard } from '../components/common/StatCard';
import { JobProgressCard } from '../components/jobs/JobProgressCard';
import { NewJobModal } from '../components/jobs/NewJobModal';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { analyticsApi } from '../api/analytics';
import { jobsApi } from '../api/jobs';
import { AnalyticsSummary, Job } from '../types';
import { 
  Database, 
  Layers, 
  CheckCircle, 
  AlertTriangle, 
  Copy, 
  Zap, 
  Play, 
  Compass, 
  ShieldCheck, 
  ArrowRight,
  TrendingUp
} from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const loadData = async () => {
    try {
      const [sumData, jobData] = await Promise.all([
        analyticsApi.getSummary(),
        jobsApi.list(5)
      ]);
      setSummary(sumData);
      setJobs(jobData);
    } catch (err) {
      console.error('Failed to load dashboard data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 10000);
    return () => clearInterval(interval);
  }, []);

  const activeJob = jobs.find((j) => j.status === 'RUNNING' || j.status === 'PENDING');
  const totalProcessed = summary?.total_extracted || 0;
  const successRate = totalProcessed > 0
    ? (((summary?.total_successful || 0) / totalProcessed) * 100).toFixed(1)
    : '100.0';

  if (loading && !summary) {
    return (
      <div>
        <PageHeader 
          title="CoA Directory Extractor" 
          description="Public Architecture Directory Data Pipeline" 
        />
        <LoadingSkeleton rows={6} height={40} />
      </div>
    );
  }

  return (
    <div>
      <PageHeader 
        title="CoA Directory Extractor" 
        description="Extract, validate, analyze, and export publicly available Council of Architecture directory records through a reliable high-performance data pipeline."
        actions={
          <div style={{ display: 'flex', gap: 'var(--spacing-sm)' }}>
            <button className="btn btn-secondary" onClick={() => navigate('/directory')}>
              <Compass size={16} />
              <span>Explore Directory</span>
            </button>
            <button className="btn btn-primary" onClick={() => setIsModalOpen(true)}>
              <Play size={16} />
              <span>New Extraction Job</span>
            </button>
          </div>
        }
      />

      {/* First Time Workflow Banner */}
      <div className="card" style={{ 
        marginBottom: 'var(--spacing-xl)', 
        backgroundColor: 'var(--color-primary-light)',
        borderColor: 'var(--color-primary-subtle)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 'var(--spacing-md)' }}>
          <div>
            <h2 style={{ fontSize: 'var(--font-size-base)', fontWeight: 'var(--font-weight-semibold)', color: 'var(--color-primary)' }}>
              How the Extraction Pipeline Works
            </h2>
            <p style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-secondary)', marginTop: '4px' }}>
              1. Explore Directory &rarr; 2. Configure Pacing & Concurrency &rarr; 3. Start Job &rarr; 4. Monitor Live Progress &rarr; 5. Validate & Deduplicate &rarr; 6. Export CSV/JSON
            </p>
          </div>
          <button 
            className="btn btn-primary btn-sm"
            onClick={() => setIsModalOpen(true)}
          >
            <span>Get Started</span>
            <ArrowRight size={14} />
          </button>
        </div>
      </div>

      {/* Active Job Real-Time Card */}
      {activeJob && (
        <div style={{ marginBottom: 'var(--spacing-xl)' }}>
          <h2 style={{ fontSize: 'var(--font-size-base)', fontWeight: 'var(--font-weight-semibold)', marginBottom: 'var(--spacing-sm)' }}>
            Live Background Extraction
          </h2>
          <JobProgressCard job={activeJob} onJobUpdated={loadData} />
        </div>
      )}

      {/* Statistics Grid */}
      <div className="stats-grid">
        <StatCard 
          label="Total Records" 
          value={summary?.total_records.toLocaleString() || '0'} 
          helper="Persisted in database"
          icon={<Database size={20} />}
        />
        <StatCard 
          label="Extracted" 
          value={summary?.total_extracted.toLocaleString() || '0'} 
          helper={`${summary?.total_successful.toLocaleString() || 0} valid`}
          icon={<CheckCircle size={20} />}
        />
        <StatCard 
          label="Success Rate" 
          value={`${successRate}%`} 
          helper="Validation pass rate"
          icon={<ShieldCheck size={20} />}
        />
        <StatCard 
          label="Extraction Speed" 
          value={`${summary?.avg_speed_rec_sec || 0} rec/s`} 
          helper="Average pipeline throughput"
          icon={<Zap size={20} />}
        />
        <StatCard 
          label="Duplicates Filtered" 
          value={summary?.total_duplicates.toLocaleString() || '0'} 
          helper="Deduplicated by Reg No"
          icon={<Copy size={20} />}
        />
        <StatCard 
          label="Data Quality Score" 
          value={`${summary?.data_quality_score || 0} / 100`} 
          helper="Completeness, validity & consistency"
          icon={<TrendingUp size={20} />}
        />
      </div>

      {/* Recent Jobs Overview */}
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Recent Extraction Jobs</h2>
            <p className="card-subtitle">Latest batch execution history and data quality</p>
          </div>
          <button className="btn btn-secondary btn-sm" onClick={() => navigate('/jobs')}>
            <span>View All Jobs</span>
          </button>
        </div>

        {jobs.length === 0 ? (
          <div style={{ textAlign: 'center', padding: 'var(--spacing-xl)' }}>
            <p style={{ color: 'var(--color-text-muted)', marginBottom: 'var(--spacing-md)' }}>
              No extraction jobs executed yet. Launch your first job to extract public Council of Architecture records.
            </p>
            <button className="btn btn-primary" onClick={() => setIsModalOpen(true)}>
              <Play size={14} />
              <span>Create Extraction Job</span>
            </button>
          </div>
        ) : (
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Job ID</th>
                  <th>Status</th>
                  <th>Pages</th>
                  <th>Processed</th>
                  <th>Valid</th>
                  <th>Duplicates</th>
                  <th>Speed</th>
                  <th>Quality Score</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {jobs.map((job) => (
                  <tr key={job.id} style={{ cursor: 'pointer' }} onClick={() => navigate(`/jobs/${job.id}`)}>
                    <td style={{ fontWeight: 'var(--font-weight-medium)', color: 'var(--color-primary)' }}>
                      #{job.id}
                    </td>
                    <td>
                      <span className={`badge ${job.status === 'COMPLETED' ? 'badge-success' : job.status === 'RUNNING' ? 'badge-info' : 'badge-warning'}`}>
                        {job.status}
                      </span>
                    </td>
                    <td>{job.start_page}–{job.end_page}</td>
                    <td>{job.processed_records.toLocaleString()}</td>
                    <td>{job.successful_records.toLocaleString()}</td>
                    <td>{job.duplicate_records.toLocaleString()}</td>
                    <td>{job.speed_records_per_sec} rec/s</td>
                    <td><strong>{job.data_quality_score}%</strong></td>
                    <td style={{ color: 'var(--color-text-muted)' }}>
                      {new Date(job.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
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
        onJobCreated={loadData}
      />
    </div>
  );
};
