import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const registerUser = async (username: string, email: string, password: string) => {
  return await api.post('/users/user/', { Username: username, Email: email, Password: password });
};

export const loginUser = async (username: string, password: string) => {
  return api.post('/users/login/', { username, password });
};

export const fetchFiles = async (userId: string) => {
  return api.get(`/files/files/user/${userId}`);
};


export const uploadFile = async (file: File, userId: string, comment?: string) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('user_id', userId);
  formData.append('comment', comment || '');

  return api.post('/files/file/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const downloadFile = async (fileId: string) => {
  return api.get(`/files/file/${fileId}/`, { responseType: 'blob' });
};

export const deleteFile = async (fileId: string) => {
  return api.delete(`/files/file/${fileId}/`);
};
