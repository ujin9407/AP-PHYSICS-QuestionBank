import React, { useState, useEffect } from 'react';
import UploadZone from './components/UploadZone';
import DiagramTypeSelector from './components/DiagramTypeSelector';
import TemplateSelector from './components/TemplateSelector';
import DiagramPreview from './components/DiagramPreview';
import ProblemSolver from './components/ProblemSolver';
import { uploadDiagram, convertDiagram, getConversionStatus, exportToPdf } from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState('converter'); // 'converter' or 'solver'
  const [selectedType, setSelectedType] = useState('general');
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [uploadedImageId, setUploadedImageId] = useState(null);
  const [uploadedImageUrl, setUploadedImageUrl] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isConverting, setIsConverting] = useState(false);
  const [conversionId, setConversionId] = useState(null);
  const [conversionStatus, setConversionStatus] = useState(null);
  const [tikzCode, setTikzCode] = useState(null);
  const [description, setDescription] = useState('');

  // Poll conversion status
  useEffect(() => {
    if (!conversionId || conversionStatus === 'completed' || conversionStatus === 'failed') {
      return;
    }

    console.log('Polling conversion status for:', conversionId);
    
    const interval = setInterval(async () => {
      try {
        const status = await getConversionStatus(conversionId);
        console.log('Conversion status update:', status);
        setConversionStatus(status.status);
        
        if (status.status === 'completed') {
          setTikzCode(status.tikz_code);
          setIsConverting(false);
          console.log('Conversion completed with TikZ code:', status.tikz_code?.substring(0, 100));
        } else if (status.status === 'failed') {
          alert('변환 실패: ' + (status.error_message || '알 수 없는 오류'));
          setIsConverting(false);
        }
      } catch (error) {
        console.error('Failed to get conversion status:', error);
        console.error('Error details:', error.response?.data);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [conversionId, conversionStatus]);

  const handleUpload = async (file) => {
    setIsUploading(true);
    try {
      const response = await uploadDiagram(file);
      setUploadedImageId(response.id);
      setUploadedImageUrl(URL.createObjectURL(file));
      
      // Auto-start conversion
      await handleConvert(response.id);
    } catch (error) {
      console.error('Upload failed:', error);
      alert('업로드 실패: ' + (error.response?.data?.detail || error.message));
    } finally {
      setIsUploading(false);
    }
  };

  const handleConvert = async (imageId) => {
    setIsConverting(true);
    setConversionStatus('processing');
    
    try {
      console.log('Starting conversion for imageId:', imageId, 'type:', selectedType);
      const response = await convertDiagram(
        imageId,
        selectedType,
        description || null
      );
      
      console.log('Conversion started:', response);
      setConversionId(response.id);
    } catch (error) {
      console.error('Conversion failed:', error);
      console.error('Error details:', error.response?.data);
      alert('변환 실패: ' + (error.response?.data?.detail || error.message));
      setIsConverting(false);
    }
  };

  const handleExport = async () => {
    if (!conversionId) {
      alert('먼저 다이어그램을 변환해주세요.');
      return;
    }

    try {
      const response = await exportToPdf(conversionId, true, '물리 다이어그램');
      
      // Download the PDF
      const link = document.createElement('a');
      link.href = response.pdf_url;
      link.download = response.filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      alert('PDF 내보내기가 완료되었습니다!');
    } catch (error) {
      console.error('Export failed:', error);
      alert('PDF 내보내기 실패: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleReset = () => {
    setUploadedImageId(null);
    setUploadedImageUrl(null);
    setConversionId(null);
    setConversionStatus(null);
    setTikzCode(null);
    setDescription('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Physics AI Assistant
              </h1>
              <p className="text-gray-600 mt-1">
                AI 기반 물리 다이어그램 변환 및 문제 풀이 서비스
              </p>
            </div>
            <div className="text-4xl">🔬</div>
          </div>
          
          {/* Tab Navigation */}
          <div className="flex gap-4 mt-6 border-b border-gray-200">
            <button
              onClick={() => setActiveTab('converter')}
              className={`px-6 py-3 font-semibold transition-colors ${
                activeTab === 'converter'
                  ? 'text-blue-600 border-b-2 border-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              📊 다이어그램 변환기
            </button>
            <button
              onClick={() => setActiveTab('solver')}
              className={`px-6 py-3 font-semibold transition-colors ${
                activeTab === 'solver'
                  ? 'text-blue-600 border-b-2 border-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              🧮 AI 문제 풀이
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {activeTab === 'converter' ? (
          <DiagramConverterTab
            selectedType={selectedType}
            setSelectedType={setSelectedType}
            selectedTemplate={selectedTemplate}
            setSelectedTemplate={setSelectedTemplate}
            uploadedImageId={uploadedImageId}
            uploadedImageUrl={uploadedImageUrl}
            isUploading={isUploading}
            isConverting={isConverting}
            conversionId={conversionId}
            conversionStatus={conversionStatus}
            tikzCode={tikzCode}
            description={description}
            setDescription={setDescription}
            setTikzCode={setTikzCode}
            setConversionId={setConversionId}
            setConversionStatus={setConversionStatus}
            handleUpload={handleUpload}
            handleReset={handleReset}
            handleExport={handleExport}
          />
        ) : (
          <ProblemSolver />
        )}
      </main>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Input */}
          <div className="space-y-6">
            <DiagramTypeSelector
              selectedType={selectedType}
              onSelectType={setSelectedType}
            />

            <div className="card">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">
                설명 (선택사항)
              </h3>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="다이어그램에 대한 추가 설명을 입력하세요..."
                className="input-field h-24 resize-none"
              />
              <p className="text-sm text-gray-500 mt-2">
                추가 설명을 제공하면 더 정확한 변환 결과를 얻을 수 있습니다.
              </p>
            </div>

            <TemplateSelector
              selectedType={selectedType}
              onSelectTemplate={(template) => {
                setSelectedTemplate(template);
                // 템플릿 선택 시 미리보기를 바로 보여주기
                if (template && template.tikz_code) {
                  console.log('Template selected:', template.id);
                  // 데모 모드: 템플릿의 TikZ 코드를 바로 표시
                  setTikzCode(template.tikz_code);
                  setConversionId(`template-${template.id}`);
                  setConversionStatus('completed');
                }
              }}
            />

            {!uploadedImageId ? (
              <UploadZone onUpload={handleUpload} isUploading={isUploading} />
            ) : (
              <div className="card">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">
                  업로드된 이미지
                </h3>
                <img
                  src={uploadedImageUrl}
                  alt="Uploaded diagram"
                  className="w-full rounded-lg border border-gray-200"
                />
                <button
                  onClick={handleReset}
                  className="btn-secondary w-full mt-4"
                >
                  새 이미지 업로드
                </button>
              </div>
            )}

            {isConverting && (
              <div className="card bg-yellow-50 border border-yellow-200">
                <div className="flex items-center space-x-3">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-yellow-600"></div>
                  <div>
                    <p className="font-semibold text-yellow-900">
                      다이어그램 변환 중...
                    </p>
                    <p className="text-sm text-yellow-800">
                      AI가 손글씨 다이어그램을 분석하고 있습니다.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Right Column - Output */}
          <div className="space-y-6">
            {conversionId && conversionStatus === 'completed' ? (
              <DiagramPreview
                conversionId={conversionId}
                onExport={handleExport}
                tikzCode={tikzCode}
              />
            ) : conversionId && conversionStatus === 'processing' ? (
              <div className="card bg-blue-50 min-h-[400px] flex items-center justify-center">
                <div className="text-center text-blue-700">
                  <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
                  <p className="text-lg font-semibold">변환 중...</p>
                  <p className="text-sm mt-2">AI가 다이어그램을 분석하고 있습니다</p>
                  <p className="text-xs mt-4 text-blue-600">ID: {conversionId}</p>
                </div>
              </div>
            ) : (
              <div className="card bg-gray-50 min-h-[400px] flex items-center justify-center">
                <div className="text-center text-gray-500">
                  <svg
                    className="w-24 h-24 mx-auto mb-4 text-gray-300"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                  <p className="text-lg font-medium">
                    다이어그램을 업로드하면 여기에 미리보기가 표시됩니다
                  </p>
                  {conversionStatus && (
                    <p className="text-sm mt-2">상태: {conversionStatus}</p>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

      {/* Footer */}
      <footer className="bg-white mt-12 py-6 border-t">
        <div className="container mx-auto px-4 text-center text-gray-600">
          <p>© 2024 Physics AI Assistant. Powered by AI</p>
        </div>
      </footer>
    </div>
  );
}

// Diagram Converter Tab Component
const DiagramConverterTab = ({
  selectedType,
  setSelectedType,
  selectedTemplate,
  setSelectedTemplate,
  uploadedImageId,
  uploadedImageUrl,
  isUploading,
  isConverting,
  conversionId,
  conversionStatus,
  tikzCode,
  description,
  setDescription,
  setTikzCode,
  setConversionId,
  setConversionStatus,
  handleUpload,
  handleReset,
  handleExport,
}) => {
  return (
    <>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Column - Input */}
        <div className="space-y-6">
          <DiagramTypeSelector
            selectedType={selectedType}
            onSelectType={setSelectedType}
          />

          <div className="card">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              설명 (선택사항)
            </h3>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="다이어그램에 대한 추가 설명을 입력하세요..."
              className="input-field h-24 resize-none"
            />
            <p className="text-sm text-gray-500 mt-2">
              추가 설명을 제공하면 더 정확한 변환 결과를 얻을 수 있습니다.
            </p>
          </div>

          <TemplateSelector
            selectedType={selectedType}
            onSelectTemplate={(template) => {
              setSelectedTemplate(template);
              if (template && template.tikz_code) {
                setTikzCode(template.tikz_code);
                setConversionId(`template-${template.id}`);
                setConversionStatus('completed');
              }
            }}
          />

          {!uploadedImageId ? (
            <UploadZone onUpload={handleUpload} isUploading={isUploading} />
          ) : (
            <div className="card">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">
                업로드된 이미지
              </h3>
              <img
                src={uploadedImageUrl}
                alt="Uploaded diagram"
                className="w-full rounded-lg border border-gray-200"
              />
              <button
                onClick={handleReset}
                className="btn-secondary w-full mt-4"
              >
                새 이미지 업로드
              </button>
            </div>
          )}

          {isConverting && (
            <div className="card bg-yellow-50 border border-yellow-200">
              <div className="flex items-center space-x-3">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-yellow-600"></div>
                <div>
                  <p className="font-semibold text-yellow-900">
                    다이어그램 변환 중...
                  </p>
                  <p className="text-sm text-yellow-800">
                    AI가 손글씨 다이어그램을 분석하고 있습니다.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Column - Output */}
        <div className="space-y-6">
          {conversionId && conversionStatus === 'completed' ? (
            <DiagramPreview
              conversionId={conversionId}
              onExport={handleExport}
              tikzCode={tikzCode}
            />
          ) : conversionId && conversionStatus === 'processing' ? (
            <div className="card bg-blue-50 min-h-[400px] flex items-center justify-center">
              <div className="text-center text-blue-700">
                <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
                <p className="text-lg font-semibold">변환 중...</p>
                <p className="text-sm mt-2">AI가 다이어그램을 분석하고 있습니다</p>
                <p className="text-xs mt-4 text-blue-600">ID: {conversionId}</p>
              </div>
            </div>
          ) : (
            <div className="card bg-gray-50 min-h-[400px] flex items-center justify-center">
              <div className="text-center text-gray-500">
                <svg
                  className="w-24 h-24 mx-auto mb-4 text-gray-300"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
                <p className="text-lg font-medium">
                  다이어그램을 업로드하면 여기에 미리보기가 표시됩니다
                </p>
                {conversionStatus && (
                  <p className="text-sm mt-2">상태: {conversionStatus}</p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Features Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
        <div className="card text-center">
          <div className="text-4xl mb-3">🤖</div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">
            AI 기반 변환
          </h3>
          <p className="text-sm text-gray-600">
            DaTikZv2를 사용한 정확한 손글씨 다이어그램 인식
          </p>
        </div>

        <div className="card text-center">
          <div className="text-4xl mb-3">⚡</div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">
            실시간 미리보기
          </h3>
          <p className="text-sm text-gray-600">
            변환된 다이어그램을 즉시 확인하고 수정 가능
          </p>
        </div>

        <div className="card text-center">
          <div className="text-4xl mb-3">📄</div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">
            PDF 내보내기
          </h3>
          <p className="text-sm text-gray-600">
            다이어그램과 TikZ 코드를 PDF로 저장
          </p>
        </div>
      </div>
    </>
  );
};

export default App;
