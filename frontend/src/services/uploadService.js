import api from './api';

const UPLOAD_URL = '/upload';
const USER_UPLOAD_URL = '/user-uploads';

export const uploadContent = async (formData) => {
    const response = await api.post(UPLOAD_URL, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const fetchUserUploads = async (params) => {
    const response = await api.get(`${USER_UPLOAD_URL}/my-uploads`, { params });
    return response.data;
};
