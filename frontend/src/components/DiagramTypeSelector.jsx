import React from 'react';

const diagramTypes = [
  { value: 'general', label: '일반', icon: '📐', description: '일반적인 물리 다이어그램' },
  { value: 'mechanics', label: '역학', icon: '⚙️', description: '힘, 운동, 에너지' },
  { value: 'electricity', label: '전기', icon: '⚡', description: '회로, 전기장' },
  { value: 'optics', label: '광학', icon: '🔬', description: '빛, 렌즈, 반사' },
  { value: 'thermodynamics', label: '열역학', icon: '🌡️', description: '열, 엔트로피, PV 다이어그램' },
  { value: 'quantum', label: '양자', icon: '⚛️', description: '에너지 준위, 파동함수' },
];

const DiagramTypeSelector = ({ selectedType, onSelectType }) => {
  return (
    <div className="card">
      <h3 className="text-xl font-semibold text-gray-800 mb-4">다이어그램 유형</h3>
      
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {diagramTypes.map((type) => (
          <button
            key={type.value}
            onClick={() => onSelectType(type.value)}
            className={`
              p-4 rounded-lg border-2 text-left transition-all duration-200
              ${selectedType === type.value
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-200 hover:border-primary-300'
              }
            `}
          >
            <div className="text-3xl mb-2">{type.icon}</div>
            <div className="font-semibold text-gray-800">{type.label}</div>
            <div className="text-xs text-gray-600 mt-1">{type.description}</div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default DiagramTypeSelector;
