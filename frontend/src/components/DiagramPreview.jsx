import React, { useState, useEffect } from 'react';

const DiagramPreview = ({ conversionId, onExport, tikzCode }) => {
  const [previewUrl, setPreviewUrl] = useState(null);
  const [showCode, setShowCode] = useState(false);

  useEffect(() => {
    if (conversionId) {
      // In real implementation, this would be from the conversion status
      setPreviewUrl(`/api/outputs/${conversionId}.png`);
    }
  }, [conversionId]);

  const handleCopyCode = () => {
    if (tikzCode) {
      navigator.clipboard.writeText(tikzCode);
      alert('TikZ 코드가 클립보드에 복사되었습니다!');
    }
  };

  if (!previewUrl && !tikzCode) {
    return null;
  }

  return (
    <div className="space-y-4">
      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-semibold text-gray-800">미리보기</h3>
          <div className="flex space-x-2">
            <button
              onClick={() => setShowCode(!showCode)}
              className="btn-secondary text-sm"
            >
              {showCode ? '이미지 보기' : 'TikZ 코드 보기'}
            </button>
            <button
              onClick={onExport}
              className="btn-primary text-sm"
            >
              PDF로 내보내기
            </button>
          </div>
        </div>

        {!showCode ? (
          <div className="bg-gray-100 rounded-lg p-8 flex items-center justify-center min-h-[400px]">
            {previewUrl ? (
              <img
                src={previewUrl}
                alt="Diagram Preview"
                className="max-w-full max-h-[500px] object-contain"
                onError={(e) => {
                  e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300"><rect width="400" height="300" fill="%23f0f0f0"/><text x="50%" y="50%" text-anchor="middle" fill="%23999">미리보기를 불러오는 중...</text></svg>';
                }}
              />
            ) : (
              <div className="text-center text-gray-500">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
                <p>다이어그램을 생성하는 중...</p>
              </div>
            )}
          </div>
        ) : (
          <div className="relative">
            <button
              onClick={handleCopyCode}
              className="absolute top-2 right-2 bg-gray-800 text-white px-3 py-1 rounded text-sm hover:bg-gray-700"
            >
              복사
            </button>
            <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto max-h-[500px] text-sm">
              <code>{tikzCode || '// TikZ 코드를 생성하는 중...'}</code>
            </pre>
          </div>
        )}
      </div>

      <div className="card bg-blue-50 border border-blue-200">
        <h4 className="font-semibold text-blue-900 mb-2">💡 팁</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• TikZ 코드를 LaTeX 문서에 직접 복사하여 사용할 수 있습니다</li>
          <li>• PDF로 내보내기를 클릭하면 다이어그램과 코드를 함께 저장할 수 있습니다</li>
          <li>• 템플릿을 사용하면 더 정확한 변환 결과를 얻을 수 있습니다</li>
        </ul>
      </div>
    </div>
  );
};

export default DiagramPreview;
