import api from './api';

const AUTH_URL = '/users';

export const register = async (userData) => {
    const response = await api.post(`${AUTH_URL}/register`, userData);
    if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user', JSON.stringify(response.data));
    }
    return response.data;
};

export const login = async (userData) => {
    const response = await api.post(`${AUTH_URL}/login`, userData);
    if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user', JSON.stringify(response.data));
    }
    return response.data;
};

export const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
};

export const getCurrentUser = async () => {
    const response = await api.get(`${AUTH_URL}/me`);
    return response.data;
}
