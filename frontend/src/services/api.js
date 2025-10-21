import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Upload service
export const uploadDiagram = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

// Convert service
export const convertDiagram = async (imageId, diagramType, description = null) => {
  const response = await api.post('/convert', {
    image_id: imageId,
    diagram_type: diagramType,
    description: description,
  });
  
  return response.data;
};

export const getConversionStatus = async (conversionId) => {
  const response = await api.get(`/convert/${conversionId}`);
  return response.data;
};

// Template service
export const getTemplates = async (diagramType = null) => {
  const params = diagramType ? { diagram_type: diagramType } : {};
  const response = await api.get('/templates', { params });
  return response.data;
};

export const getTemplate = async (templateId) => {
  const response = await api.get(`/templates/${templateId}`);
  return response.data;
};

// Render service
export const renderTikz = async (tikzCode, format = 'png') => {
  const response = await api.post('/render', {
    tikz_code: tikzCode,
    format: format,
  });
  
  return response.data;
};

// Export service
export const exportToPdf = async (diagramId, includeCode = false, title = null) => {
  const response = await api.post('/export/pdf', {
    diagram_id: diagramId,
    include_code: includeCode,
    title: title,
  });
  
  return response.data;
};

// Problem Solver service
export const uploadProblem = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(`${API_BASE_URL}/solver/upload-problem`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const solveProblem = async (problemText = null, imageId = null) => {
  const response = await api.post('/solver/solve', {
    problem_text: problemText,
    image_id: imageId,
  });
  
  return response.data;
};

export const getSolution = async (solutionId) => {
  const response = await api.get(`/solver/solution/${solutionId}`);
  return response.data;
};

export default api;
