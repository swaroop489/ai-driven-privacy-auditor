import api from './api';

const UPLOAD_URL = '/upload';
const USER_UPLOAD_URL = '/user-uploads';

// Upload Content (Text or File)
export const uploadContent = async (formData) => {
    // Note: if sending FormData (image), axios should handle Content-Type if we pass it directly
    // or we can let the interceptor handle it if we set headers manually for this call.
    // Actually, axios automatically sets Content-Type to multipart/form-data if data is FormData.
    // EXCEPT we set application/json globally. We might need to override.

    const response = await api.post(UPLOAD_URL, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

// Fetch User Upload History
export const fetchUserUploads = async (params) => {
    const response = await api.get(`${USER_UPLOAD_URL}/my-uploads`, { params });
    return response.data;
};
