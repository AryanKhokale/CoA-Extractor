import { apiClient } from './client';
import { ArchitectListResponse, Architect } from '../types';

export interface DirectoryFilterParams {
  query?: string;
  state?: string;
  city?: string;
  status?: string;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  page?: number;
  pageSize?: number;
}

export const directoryApi = {
  list: (params: DirectoryFilterParams = {}) => {
    const searchParams = new URLSearchParams();
    if (params.query) searchParams.append('query', params.query);
    if (params.state) searchParams.append('state', params.state);
    if (params.city) searchParams.append('city', params.city);
    if (params.status) searchParams.append('status', params.status);
    if (params.sortBy) searchParams.append('sort_by', params.sortBy);
    if (params.sortOrder) searchParams.append('sort_order', params.sortOrder);
    if (params.page) searchParams.append('page', params.page.toString());
    if (params.pageSize) searchParams.append('page_size', params.pageSize.toString());

    return apiClient<ArchitectListResponse>(`/directory/architects?${searchParams.toString()}`);
  },
  search: (q: string, limit: number = 10) => apiClient<Architect[]>(`/directory/search?q=${encodeURIComponent(q)}&limit=${limit}`),
  getFilters: () => apiClient<{ states: string[]; cities: string[]; statuses: string[] }>('/directory/filters')
};
