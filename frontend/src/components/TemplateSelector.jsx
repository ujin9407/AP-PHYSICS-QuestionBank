import React, { useState, useEffect } from 'react';
import { getTemplates } from '../services/api';

const TemplateSelector = ({ selectedType, onSelectTemplate }) => {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState(null);

  useEffect(() => {
    loadTemplates();
  }, [selectedType]);

  const loadTemplates = async () => {
    setLoading(true);
    try {
      const response = await getTemplates(selectedType);
      setTemplates(response.templates || []);
    } catch (error) {
      console.error('Failed to load templates:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTemplateClick = (template) => {
    setSelectedTemplate(template.id);
    onSelectTemplate(template);
  };

  if (loading) {
    return (
      <div className="card">
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
          <p className="text-gray-600 mt-2">템플릿 로딩 중...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="text-xl font-semibold text-gray-800 mb-4">템플릿 선택</h3>
      
      {templates.length === 0 ? (
        <p className="text-gray-500 text-center py-4">사용 가능한 템플릿이 없습니다.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {templates.map((template) => (
            <div
              key={template.id}
              onClick={() => handleTemplateClick(template)}
              className={`
                border-2 rounded-lg p-4 cursor-pointer transition-all duration-200
                ${selectedTemplate === template.id 
                  ? 'border-primary-500 bg-primary-50' 
                  : 'border-gray-200 hover:border-primary-300'
                }
              `}
            >
              <div className="aspect-video bg-gray-100 rounded mb-3 flex items-center justify-center">
                <svg
                  className="w-12 h-12 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              
              <h4 className="font-semibold text-gray-800 mb-1">{template.name}</h4>
              <p className="text-sm text-gray-600">{template.description}</p>
              
              <div className="mt-2">
                <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                  {template.diagram_type}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
      
      {selectedTemplate && (
        <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-sm text-green-800">
            ✓ 템플릿이 선택되었습니다! 오른쪽에서 미리보기를 확인하세요.
          </p>
          <p className="text-xs text-green-700 mt-1">
            이미지를 업로드하면 이 템플릿을 기반으로 변환됩니다.
          </p>
        </div>
      )}
    </div>
  );
};

export default TemplateSelector;
