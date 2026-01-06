import api from './api';

const ADMIN_URL = '/admin';

// Get System Stats
export const getSystemStats = async () => {
    const response = await api.get(`${ADMIN_URL}/stats`);
    return response.data;
};

// Get Global Violations
export const getGlobalViolations = async () => {
    const response = await api.get(`${ADMIN_URL}/violations`);
    return response.data;
};
