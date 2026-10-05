import { apiClient } from './client';
import { Job, JobCreateRequest, ArchitectListResponse } from '../types';

export const jobsApi = {
  list: (limit: number = 20) => apiClient<Job[]>(`/jobs?limit=${limit}`),
  get: (id: string) => apiClient<Job>(`/jobs/${id}`),
  create: (data: JobCreateRequest) => apiClient<Job>('/jobs', {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  cancel: (id: string) => apiClient<{ message: string; job_id: string }>(`/jobs/${id}/cancel`, {
    method: 'POST'
  }),
  retry: (id: string) => apiClient<Job>(`/jobs/${id}/retry`, {
    method: 'POST'
  }),
  getRecords: (id: string, page: number = 1, pageSize: number = 25) => 
    apiClient<ArchitectListResponse>(`/jobs/${id}/records?page=${page}&page_size=${pageSize}`),
  getErrors: (id: string) => apiClient<any[]>(`/jobs/${id}/errors`)
};
