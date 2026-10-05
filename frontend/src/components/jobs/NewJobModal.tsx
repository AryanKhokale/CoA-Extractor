import React, { useState } from 'react';
import { Modal } from '../common/Modal';
import { JobCreateRequest } from '../../types';
import { jobsApi } from '../../api/jobs';
import { Info, Play, ShieldAlert } from 'lucide-react';

interface NewJobModalProps {
  isOpen: boolean;
  onClose: () => void;
  onJobCreated: () => void;
}

export const NewJobModal: React.FC<NewJobModalProps> = ({ isOpen, onClose, onJobCreated }) => {
  const [formData, setFormData] = useState<JobCreateRequest>({
    start_page: 1,
    end_page: 5,
    concurrency: 5,
    requests_per_second: 2.0,
    timeout_seconds: 30,
    retry_count: 3,
    mode: 'live'
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      await jobsApi.create(formData);
      onJobCreated();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Failed to start extraction job');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Configure New Extraction Job">
      <form onSubmit={handleSubmit}>
        <div className="alert-banner alert-info">
          <Info size={16} />
          <div>
            Extraction settings are automatically constrained to respect the target Council of Architecture website and prevent excessive traffic.
          </div>
        </div>

        {error && (
          <div className="alert-banner alert-warning">
            <ShieldAlert size={16} />
            <div>{error}</div>
          </div>
        )}

        {/* Scope Section */}
        <h3 style={{ fontSize: 'var(--font-size-sm)', fontWeight: 'var(--font-weight-semibold)', marginBottom: 'var(--spacing-xs)' }}>
          1. Extraction Scope
        </h3>
        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Start Page</label>
            <input 
              type="number"
              className="form-input"
              min={1}
              max={1000}
              value={formData.start_page}
              onChange={(e) => setFormData({ ...formData, start_page: parseInt(e.target.value) || 1 })}
              required
            />
            <span className="form-hint">Directory page index (50 records/page)</span>
          </div>

          <div className="form-group">
            <label className="form-label">End Page</label>
            <input 
              type="number"
              className="form-input"
              min={formData.start_page}
              max={1000}
              value={formData.end_page}
              onChange={(e) => setFormData({ ...formData, end_page: parseInt(e.target.value) || 1 })}
              required
            />
            <span className="form-hint">
              Target ~{(Math.max(1, formData.end_page - formData.start_page + 1) * 50).toLocaleString()} records
            </span>
          </div>
        </div>

        {/* Performance Section */}
        <h3 style={{ fontSize: 'var(--font-size-sm)', fontWeight: 'var(--font-weight-semibold)', marginTop: 'var(--spacing-md)', marginBottom: 'var(--spacing-xs)' }}>
          2. Concurrency & Rate Limiting
        </h3>
        <div className="form-row">
          <div className="form-group">
            <label className="form-label">
              Concurrency ({formData.concurrency} workers)
            </label>
            <input 
              type="range"
              min={1}
              max={10}
              value={formData.concurrency}
              onChange={(e) => setFormData({ ...formData, concurrency: parseInt(e.target.value) })}
              style={{ width: '100%' }}
            />
            <span className="form-hint">Simultaneous async HTTP connections (max 10)</span>
          </div>

          <div className="form-group">
            <label className="form-label">
              Rate Limit ({formData.requests_per_second} req/s)
            </label>
            <input 
              type="range"
              min={0.5}
              max={5.0}
              step={0.5}
              value={formData.requests_per_second}
              onChange={(e) => setFormData({ ...formData, requests_per_second: parseFloat(e.target.value) })}
              style={{ width: '100%' }}
            />
            <span className="form-hint">Token-bucket request pacing</span>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Timeout (seconds)</label>
            <input 
              type="number"
              className="form-input"
              min={5}
              max={60}
              value={formData.timeout_seconds}
              onChange={(e) => setFormData({ ...formData, timeout_seconds: parseInt(e.target.value) || 30 })}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Max Retries</label>
            <input 
              type="number"
              className="form-input"
              min={1}
              max={5}
              value={formData.retry_count}
              onChange={(e) => setFormData({ ...formData, retry_count: parseInt(e.target.value) || 3 })}
            />
          </div>
        </div>

        {/* Mode Selection */}
        <div className="form-group" style={{ marginTop: 'var(--spacing-md)' }}>
          <label className="form-label">Source Mode</label>
          <select 
            className="form-select"
            value={formData.mode}
            onChange={(e) => setFormData({ ...formData, mode: e.target.value as 'live' | 'mock' })}
          >
            <option value="live">Live CoA Portal (https://www.coa.gov.in/default_arch.php)</option>
            <option value="mock">Offline Mock Mode (Safe demo with local synthetic records)</option>
          </select>
          <span className="form-hint">
            {formData.mode === 'live' 
              ? 'Sends respectful, bounded requests to the live statutory registry.'
              : 'Executes pipeline simulation using pre-validated mock records.'}
          </span>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 'var(--spacing-sm)', marginTop: 'var(--spacing-lg)' }}>
          <button type="button" className="btn btn-secondary" onClick={onClose} disabled={submitting}>
            Cancel
          </button>
          <button type="submit" className="btn btn-primary" disabled={submitting}>
            <Play size={14} />
            <span>{submitting ? 'Starting...' : 'Start Extraction Job'}</span>
          </button>
        </div>
      </form>
    </Modal>
  );
};
