import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchPrograms = async () => {
  const response = await api.get('/programs');
  return response.data;
};

export const fetchProgramStats = async () => {
  const response = await api.get('/stats/programs');
  return response.data;
};

export const fetchYearStats = async () => {
  const response = await api.get('/stats/years');
  return response.data;
};

export const fetchDivisionStats = async () => {
  const response = await api.get('/stats/divisions');
  return response.data;
};

export const fetchLifetimeStats = async () => {
  const response = await api.get('/stats/lifetime');
  return response.data;
};

export const fetchYearlyBreakdown = async () => {
  const response = await api.get('/stats/yearly-breakdown');
  return response.data;
};

export const fetchEnrollments = async (params?: {
  program_id?: number;
  year?: number;
  limit?: number;
}) => {
  const response = await api.get('/enrollments', { params });
  return response.data;
};

export const fetchPlayerEnrollmentStats = async (limit: number = 50) => {
  const response = await api.get('/stats/player-enrollments', { params: { limit } });
  return response.data;
};

export default api;
