import { apiClient } from './client';
import { AnalyticsSummary, SystemConfig } from '../types';

export const analyticsApi = {
  getSummary: () => apiClient<AnalyticsSummary>('/analytics')
};

export const configApi = {
  getConfig: () => apiClient<SystemConfig>('/config')
};
