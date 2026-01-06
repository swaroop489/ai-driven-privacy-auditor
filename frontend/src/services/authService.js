import api from './api';

const AUTH_URL = '/users';

// Register User
export const register = async (userData) => {
    const response = await api.post(`${AUTH_URL}/register`, userData);
    if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        // You might want to store user info as well
        localStorage.setItem('user', JSON.stringify(response.data));
    }
    return response.data;
};

// Login User
export const login = async (userData) => {
    const response = await api.post(`${AUTH_URL}/login`, userData);
    if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user', JSON.stringify(response.data));
    }
    return response.data;
};

// Logout User
export const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
};

// Get Current User
export const getCurrentUser = async () => {
    const response = await api.get(`${AUTH_URL}/me`);
    return response.data;
}
