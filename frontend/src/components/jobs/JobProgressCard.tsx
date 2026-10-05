import React, { useEffect, useState } from 'react';
import { Job, JobProgressEvent } from '../../types';
import { jobsApi } from '../../api/jobs';
import { getEventSourceUrl, getExportUrl } from '../../api/client';
import { StatusBadge } from '../common/StatusBadge';
import { ProgressBar } from '../common/ProgressBar';
import { 
  Play, 
  Square, 
  RotateCcw, 
  Download, 
  Clock, 
  Zap, 
  CheckCircle, 
  AlertTriangle, 
  Copy 
} from 'lucide-react';

interface JobProgressCardProps {
  job: Job;
  onJobUpdated?: () => void;
}

export const JobProgressCard: React.FC<JobProgressCardProps> = ({ job, onJobUpdated }) => {
  const [liveData, setLiveData] = useState<JobProgressEvent | null>(null);
  const [cancelling, setCancelling] = useState(false);
  const [retrying, setRetrying] = useState(false);

  useEffect(() => {
    if (job.status === 'RUNNING' || job.status === 'PENDING') {
      const sseUrl = getEventSourceUrl(`/jobs/${job.id}/events`);
      const eventSource = new EventSource(sseUrl);

      eventSource.addEventListener('progress', (e) => {
        try {
          const parsed = JSON.parse(e.data) as JobProgressEvent;
          setLiveData(parsed);
          if (parsed.status === 'COMPLETED' || parsed.status === 'FAILED' || parsed.status === 'CANCELLED') {
            eventSource.close();
            onJobUpdated?.();
          }
        } catch (err) {
          console.error('Error parsing SSE event', err);
        }
      });

      eventSource.onerror = () => {
        eventSource.close();
      };

      return () => {
        eventSource.close();
      };
    }
  }, [job.id, job.status, onJobUpdated]);

  const handleCancel = async () => {
    setCancelling(true);
    try {
      await jobsApi.cancel(job.id);
      onJobUpdated?.();
    } catch (err) {
      console.error('Cancel failed', err);
    } finally {
      setCancelling(false);
    }
  };

  const handleRetry = async () => {
    setRetrying(true);
    try {
      await jobsApi.retry(job.id);
      onJobUpdated?.();
    } catch (err) {
      console.error('Retry failed', err);
    } finally {
      setRetrying(false);
    }
  };

  const currentStatus = liveData?.status || job.status;
  const processed = liveData?.processed_records ?? job.processed_records;
  const total = liveData?.total_target ?? job.total_target;
  const successful = liveData?.successful_records ?? job.successful_records;
  const failed = liveData?.failed_records ?? job.failed_records;
  const duplicates = liveData?.duplicate_records ?? job.duplicate_records;
  const speed = liveData?.speed_records_per_sec ?? job.speed_records_per_sec;
  const pct = total > 0 ? (processed / total) * 100 : (job.status === 'COMPLETED' ? 100 : 0);

  return (
    <div className="card" style={{ marginBottom: 'var(--spacing-lg)' }}>
      <div className="card-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
          <h2 className="card-title">Job #{job.id}</h2>
          <StatusBadge status={currentStatus} />
          {job.mode === 'mock' && (
            <span className="badge badge-warning">MOCK MODE</span>
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-xs)' }}>
          {currentStatus === 'RUNNING' && (
            <button 
              className="btn btn-secondary btn-sm" 
              onClick={handleCancel}
              disabled={cancelling}
            >
              <Square size={12} />
              <span>{cancelling ? 'Stopping...' : 'Cancel Job'}</span>
            </button>
          )}

          {(currentStatus === 'FAILED' || currentStatus === 'CANCELLED') && (
            <button 
              className="btn btn-primary btn-sm" 
              onClick={handleRetry}
              disabled={retrying}
            >
              <RotateCcw size={12} />
              <span>{retrying ? 'Starting...' : 'Retry Extraction'}</span>
            </button>
          )}

          {currentStatus === 'COMPLETED' && (
            <>
              <a 
                href={getExportUrl(`/jobs/${job.id}/export/csv`)} 
                className="btn btn-secondary btn-sm"
                download={`coa_${job.id}.csv`}
              >
                <Download size={12} />
                <span>CSV</span>
              </a>
              <a 
                href={getExportUrl(`/jobs/${job.id}/export/json`)} 
                className="btn btn-secondary btn-sm"
                download={`coa_${job.id}.json`}
              >
                <Download size={12} />
                <span>JSON</span>
              </a>
            </>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      <div style={{ marginBottom: 'var(--spacing-md)' }}>
        <ProgressBar percentage={pct} />
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          fontSize: 'var(--font-size-xs)',
          color: 'var(--color-text-muted)',
          marginTop: '6px'
        }}>
          <span>{processed.toLocaleString()} / {total.toLocaleString()} records</span>
          {liveData?.estimated_remaining_seconds != null && (
            <span>Est. Remaining: {liveData.estimated_remaining_seconds}s</span>
          )}
        </div>
      </div>

      {/* Metrics Row */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', 
        gap: 'var(--spacing-md)',
        backgroundColor: 'var(--color-surface-secondary)',
        padding: 'var(--spacing-md)',
        borderRadius: 'var(--radius-md)'
      }}>
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>Throughput</span>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: '2px' }}>
            <Zap size={14} color="var(--color-primary)" />
            <strong style={{ fontSize: 'var(--font-size-base)' }}>{speed}</strong>
            <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>rec/s</span>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>Successful</span>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: '2px' }}>
            <CheckCircle size={14} color="var(--color-success)" />
            <strong style={{ fontSize: 'var(--font-size-base)' }}>{successful.toLocaleString()}</strong>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>Duplicates</span>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: '2px' }}>
            <Copy size={14} color="var(--color-warning)" />
            <strong style={{ fontSize: 'var(--font-size-base)' }}>{duplicates.toLocaleString()}</strong>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <span style={{ fontSize: 'var(--font-size-xs)', color: 'var(--color-text-muted)' }}>Failed</span>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: '2px' }}>
            <AlertTriangle size={14} color="var(--color-danger)" />
            <strong style={{ fontSize: 'var(--font-size-base)' }}>{failed.toLocaleString()}</strong>
          </div>
        </div>
      </div>

      {job.error_message && (
        <div className="alert-banner alert-warning" style={{ marginTop: 'var(--spacing-md)' }}>
          <AlertTriangle size={16} />
          <div>{job.error_message}</div>
        </div>
      )}
    </div>
  );
};
