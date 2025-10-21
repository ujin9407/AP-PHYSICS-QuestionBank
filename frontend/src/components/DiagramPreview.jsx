import React, { useState } from 'react';

const DiagramPreview = ({ conversionId, onExport, tikzCode }) => {
  const [showCode, setShowCode] = useState(false);

  console.log('DiagramPreview:', { conversionId, hasCode: !!tikzCode, showCode });

  if (!tikzCode) {
    return (
      <div className="card">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center text-gray-500">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p>TikZ 코드를 기다리는 중...</p>
          </div>
        </div>
      </div>
    );
  }

  const handleCopyCode = () => {
    navigator.clipboard.writeText(tikzCode);
    alert('TikZ 코드가 클립보드에 복사되었습니다!');
  };

  return (
    <div className="space-y-4">
      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-semibold text-gray-800">
            미리보기 ✓
          </h3>
          <div className="flex space-x-2">
            <button
              onClick={() => setShowCode(!showCode)}
              className="btn-secondary text-sm"
            >
              {showCode ? '📊 이미지 보기' : '📝 TikZ 코드 보기'}
            </button>
            <button
              onClick={onExport}
              className="btn-primary text-sm"
            >
              📄 PDF로 내보내기
            </button>
          </div>
        </div>

        {!showCode ? (
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-8 min-h-[400px]">
            <div className="bg-white rounded-lg shadow-md p-6 max-w-2xl mx-auto">
              <div className="text-center mb-4">
                <div className="inline-block bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-medium mb-4">
                  TikZ 다이어그램
                </div>
              </div>
              
              {/* Placeholder for diagram visualization */}
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center bg-gray-50">
                <svg className="w-24 h-24 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p className="text-gray-600 font-medium mb-2">
                  다이어그램이 생성되었습니다!
                </p>
                <p className="text-sm text-gray-500 mb-4">
                  LaTeX로 컴파일하면 실제 다이어그램을 볼 수 있습니다
                </p>
                <div className="flex gap-2 justify-center">
                  <button
                    onClick={() => setShowCode(true)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
                  >
                    TikZ 코드 보기
                  </button>
                  <button
                    onClick={onExport}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm"
                  >
                    PDF로 저장
                  </button>
                </div>
              </div>

              <div className="mt-4 text-center text-xs text-gray-500">
                ID: {conversionId}
              </div>
            </div>
          </div>
        ) : (
          <div className="relative">
            <button
              onClick={handleCopyCode}
              className="absolute top-2 right-2 bg-gray-800 text-white px-4 py-2 rounded-lg text-sm hover:bg-gray-700 z-10 flex items-center gap-2"
            >
              📋 복사
            </button>
            <pre className="bg-gray-900 text-gray-100 p-6 rounded-lg overflow-x-auto max-h-[600px] text-sm leading-relaxed">
              <code>{tikzCode}</code>
            </pre>
            <div className="mt-2 text-xs text-gray-500 text-right">
              {tikzCode.split('\n').length} 줄, {tikzCode.length} 문자
            </div>
          </div>
        )}
      </div>

      <div className="card bg-blue-50 border border-blue-200">
        <h4 className="font-semibold text-blue-900 mb-2 flex items-center gap-2">
          💡 사용 방법
        </h4>
        <ul className="text-sm text-blue-800 space-y-2">
          <li className="flex items-start gap-2">
            <span className="text-blue-600">1.</span>
            <span>위의 "TikZ 코드 보기" 버튼을 클릭하여 코드를 확인하세요</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-600">2.</span>
            <span>"복사" 버튼으로 코드를 클립보드에 복사할 수 있습니다</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-600">3.</span>
            <span>LaTeX 문서에 붙여넣고 컴파일하면 다이어그램이 생성됩니다</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-600">4.</span>
            <span>"PDF로 내보내기"로 다이어그램과 코드를 함께 저장하세요</span>
          </li>
        </ul>
      </div>

      <div className="card bg-green-50 border border-green-200">
        <h4 className="font-semibold text-green-900 mb-2">✅ 성공!</h4>
        <p className="text-sm text-green-800">
          TikZ 코드가 성공적으로 생성되었습니다. 이제 LaTeX에서 사용하거나 PDF로 저장할 수 있습니다.
        </p>
      </div>
    </div>
  );
};

export default DiagramPreview;
