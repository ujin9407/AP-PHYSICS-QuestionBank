import React, { useState, useEffect, useRef } from 'react';

const DiagramPreview = ({ conversionId, onExport, tikzCode }) => {
  const [showCode, setShowCode] = useState(false);
  const [isRendering, setIsRendering] = useState(false);
  const tikzContainerRef = useRef(null);

  console.log('DiagramPreview:', { conversionId, hasCode: !!tikzCode, showCode });

  useEffect(() => {
    if (tikzCode && !showCode && tikzContainerRef.current) {
      setIsRendering(true);
      
      // TikZJax가 로드될 때까지 기다림
      const checkTikzJax = setInterval(() => {
        if (window.tikzjax) {
          clearInterval(checkTikzJax);
          setTimeout(() => {
            setIsRendering(false);
          }, 2000); // TikZ 렌더링 시간 대기
        }
      }, 100);

      return () => clearInterval(checkTikzJax);
    }
  }, [tikzCode, showCode]);

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

  const handleDownloadLatex = () => {
    const fullLatexDoc = `\\documentclass[border=2pt]{standalone}
\\usepackage{tikz}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usetikzlibrary{arrows.meta,positioning,shapes,decorations.markings,circuits.ee.IEC}

\\begin{document}
${tikzCode}
\\end{document}`;

    const blob = new Blob([fullLatexDoc], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `diagram_${conversionId}.tex`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-4">
      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-semibold text-gray-800 flex items-center gap-2">
            <span>미리보기</span>
            <span className="text-green-500">✓</span>
          </h3>
          <div className="flex space-x-2">
            <button
              onClick={() => setShowCode(!showCode)}
              className="btn-secondary text-sm"
            >
              {showCode ? '📊 렌더링 보기' : '📝 TikZ 코드'}
            </button>
            <button
              onClick={handleDownloadLatex}
              className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 text-sm"
            >
              📥 .tex 다운로드
            </button>
            <button
              onClick={onExport}
              className="btn-primary text-sm"
            >
              📄 PDF 내보내기
            </button>
          </div>
        </div>

        {!showCode ? (
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-8 min-h-[400px]">
            <div className="bg-white rounded-lg shadow-lg p-8 max-w-4xl mx-auto">
              <div className="text-center mb-6">
                <div className="inline-block bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-2 rounded-full text-sm font-medium mb-4">
                  🎨 LaTeX 렌더링 미리보기
                </div>
              </div>
              
              {isRendering && (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                  <p className="text-gray-600">TikZ 다이어그램 렌더링 중...</p>
                </div>
              )}
              
              {/* TikZ 렌더링 영역 */}
              <div 
                ref={tikzContainerRef}
                className="tikz-container flex items-center justify-center min-h-[300px] p-4"
                style={{ 
                  background: 'white',
                  border: '2px dashed #e5e7eb',
                  borderRadius: '0.5rem'
                }}
              >
                <script type="text/tikz">
                  {tikzCode}
                </script>
              </div>

              <div className="mt-6 flex justify-center gap-3">
                <button
                  onClick={() => setShowCode(true)}
                  className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 text-sm"
                >
                  📝 소스 코드 보기
                </button>
                <button
                  onClick={handleDownloadLatex}
                  className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 text-sm"
                >
                  💾 LaTeX 파일 저장
                </button>
                <button
                  onClick={onExport}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm"
                >
                  📄 PDF로 저장
                </button>
              </div>

              <div className="mt-4 text-center text-xs text-gray-500">
                ID: {conversionId} | {tikzCode.split('\n').length} 줄
              </div>
            </div>
          </div>
        ) : (
          <div className="relative">
            <div className="absolute top-2 right-2 flex gap-2 z-10">
              <button
                onClick={handleCopyCode}
                className="bg-gray-800 text-white px-4 py-2 rounded-lg text-sm hover:bg-gray-700 flex items-center gap-2"
              >
                📋 복사
              </button>
              <button
                onClick={handleDownloadLatex}
                className="bg-purple-700 text-white px-4 py-2 rounded-lg text-sm hover:bg-purple-800 flex items-center gap-2"
              >
                💾 저장
              </button>
            </div>
            <pre className="bg-gray-900 text-gray-100 p-6 rounded-lg overflow-x-auto max-h-[600px] text-sm leading-relaxed pt-16">
              <code>{tikzCode}</code>
            </pre>
            <div className="mt-2 p-3 bg-gray-100 rounded text-xs text-gray-600 flex justify-between items-center">
              <span>
                {tikzCode.split('\n').length} 줄 | {tikzCode.length} 문자
              </span>
              <span className="text-blue-600">
                LaTeX에 직접 붙여넣기 가능
              </span>
            </div>
          </div>
        )}
      </div>

      <div className="card bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200">
        <h4 className="font-semibold text-blue-900 mb-3 flex items-center gap-2 text-lg">
          💡 사용 방법
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <h5 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
              <span className="bg-blue-100 text-blue-800 w-6 h-6 rounded-full flex items-center justify-center text-sm">1</span>
              웹에서 미리보기
            </h5>
            <p className="text-sm text-gray-600">
              위의 렌더링된 다이어그램을 바로 확인하세요. TikZJax가 실시간으로 렌더링합니다.
            </p>
          </div>
          
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <h5 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
              <span className="bg-blue-100 text-blue-800 w-6 h-6 rounded-full flex items-center justify-center text-sm">2</span>
              LaTeX에서 사용
            </h5>
            <p className="text-sm text-gray-600">
              "📝 TikZ 코드" 버튼으로 소스를 확인하고 복사하여 LaTeX 문서에 붙여넣으세요.
            </p>
          </div>
          
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <h5 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
              <span className="bg-blue-100 text-blue-800 w-6 h-6 rounded-full flex items-center justify-center text-sm">3</span>
              .tex 파일로 저장
            </h5>
            <p className="text-sm text-gray-600">
              "💾 .tex 다운로드" 버튼으로 완전한 LaTeX 문서를 다운로드하여 컴파일하세요.
            </p>
          </div>
          
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <h5 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
              <span className="bg-blue-100 text-blue-800 w-6 h-6 rounded-full flex items-center justify-center text-sm">4</span>
              PDF로 내보내기
            </h5>
            <p className="text-sm text-gray-600">
              "📄 PDF 내보내기" 버튼으로 다이어그램과 코드를 함께 PDF로 저장하세요.
            </p>
          </div>
        </div>
      </div>

      <div className="card bg-green-50 border border-green-200">
        <div className="flex items-start gap-3">
          <div className="text-2xl">✅</div>
          <div className="flex-1">
            <h4 className="font-semibold text-green-900 mb-1">성공적으로 생성되었습니다!</h4>
            <p className="text-sm text-green-800">
              TikZ 코드가 생성되었으며 웹 브라우저에서 바로 렌더링되었습니다. 
              이제 LaTeX 문서에서 사용하거나 PDF로 저장할 수 있습니다.
            </p>
          </div>
        </div>
      </div>

      <div className="card bg-amber-50 border border-amber-200">
        <div className="flex items-start gap-3">
          <div className="text-2xl">⚠️</div>
          <div className="flex-1">
            <h4 className="font-semibold text-amber-900 mb-1">참고사항</h4>
            <ul className="text-sm text-amber-800 space-y-1">
              <li>• 복잡한 다이어그램은 렌더링에 시간이 걸릴 수 있습니다</li>
              <li>• 일부 고급 TikZ 기능은 브라우저에서 지원되지 않을 수 있습니다</li>
              <li>• 완벽한 결과를 위해 LaTeX 문서에서 직접 컴파일하는 것을 권장합니다</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DiagramPreview;
