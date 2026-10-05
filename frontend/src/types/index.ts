export type JobStatus = 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'CANCELLED';

export interface Architect {
  id: number;
  registration_number: string;
  name: string;
  normalized_name: string;
  city?: string;
  state?: string;
  valid_up_to?: string;
  registration_year?: number;
  qualification?: string;
  status: string;
  address?: string;
  job_id?: string;
  created_at: string;
  updated_at: string;
}

export interface ArchitectListResponse {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  items: Architect[];
}

export interface Job {
  id: string;
  status: JobStatus;
  total_target: number;
  processed_records: number;
  successful_records: number;
  failed_records: number;
  duplicate_records: number;
  start_page: number;
  end_page: number;
  current_page: number;
  concurrency: number;
  requests_per_second: number;
  timeout_seconds: number;
  retry_count: number;
  mode: 'live' | 'mock';
  error_message?: string;
  speed_records_per_sec: number;
  data_quality_score: number;
  started_at?: string;
  completed_at?: string;
  created_at: string;
}

export interface JobCreateRequest {
  start_page: number;
  end_page: number;
  concurrency: number;
  requests_per_second: number;
  timeout_seconds: number;
  retry_count: number;
  mode: 'live' | 'mock';
}

export interface JobProgressEvent {
  job_id: string;
  status: JobStatus;
  total_target: number;
  processed_records: number;
  successful_records: number;
  failed_records: number;
  duplicate_records: number;
  current_page: number;
  progress_percentage: number;
  speed_records_per_sec: number;
  elapsed_seconds: number;
  estimated_remaining_seconds?: number;
  error_message?: string;
  timestamp: string;
}

export interface StateCount {
  state: string;
  count: number;
}

export interface CityCount {
  city: string;
  count: number;
}

export interface YearCount {
  year: number;
  count: number;
}

export interface StatusCount {
  status: string;
  count: number;
}

export interface ErrorCount {
  error_type: string;
  count: number;
}

export interface AnalyticsSummary {
  total_records: number;
  total_extracted: number;
  total_successful: number;
  total_failed: number;
  total_duplicates: number;
  active_jobs: number;
  avg_speed_rec_sec: number;
  data_quality_score: number;
  states_distribution: StateCount[];
  cities_distribution: CityCount[];
  years_distribution: YearCount[];
  status_distribution: StatusCount[];
  errors_distribution: ErrorCount[];
}

export interface SystemConfig {
  project_name: string;
  version: string;
  coa_base_url: string;
  max_concurrency: number;
  default_requests_per_second: number;
  default_timeout_seconds: number;
  default_retries: number;
  use_mock_data: boolean;
  status: string;
}
