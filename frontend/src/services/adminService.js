import api from './api';

const ADMIN_URL = '/admin';

export const getSystemStats = async () => {
    const response = await api.get(`${ADMIN_URL}/stats`);
    return response.data;
};

export const getGlobalViolations = async () => {
    const response = await api.get(`${ADMIN_URL}/violations`);
    return response.data;
};
