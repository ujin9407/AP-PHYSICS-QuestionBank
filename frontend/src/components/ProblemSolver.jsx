import React, { useState } from 'react';
import { uploadProblem, solveProblem } from '../services/api';

const ProblemSolver = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [solving, setSolving] = useState(false);
  const [ocrText, setOcrText] = useState('');
  const [solution, setSolution] = useState(null);
  const [imageId, setImageId] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setError(null);
      setSolution(null);
      setOcrText('');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('파일을 선택해주세요');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const data = await uploadProblem(selectedFile);
      setImageId(data.image_id);
      setOcrText(data.ocr_text || '');
      console.log('Upload successful:', data);
    } catch (err) {
      console.error('Upload error:', err);
      setError('업로드 중 오류가 발생했습니다: ' + (err.response?.data?.detail || err.message));
    } finally {
      setUploading(false);
    }
  };

  const handleSolve = async () => {
    if (!imageId && !ocrText) {
      setError('먼저 문제 이미지를 업로드하거나 텍스트를 입력해주세요');
      return;
    }

    setSolving(true);
    setError(null);

    try {
      const data = await solveProblem(ocrText || null, imageId || null);

      if (data.success) {
        setSolution(data.solution);
        console.log('Solution:', data.solution);
      } else {
        setError('문제 풀이 중 오류가 발생했습니다: ' + data.error);
      }
    } catch (err) {
      console.error('Solve error:', err);
      setError('문제 풀이 중 오류가 발생했습니다: ' + (err.response?.data?.detail || err.message));
    } finally {
      setSolving(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="card bg-gradient-to-r from-purple-600 to-blue-600 text-white">
        <h1 className="text-3xl font-bold mb-2">🧮 AI 물리 문제 풀이</h1>
        <p className="text-purple-100 mb-3">
          물리 문제를 입력하거나 이미지를 업로드하면 AI가 자동으로 단계별 풀이를 제공합니다
        </p>
        <div className="bg-white/10 rounded-lg p-3 mt-3">
          <p className="text-sm text-white/90">
            💡 <strong>이용 방법:</strong> 샘플 문제 버튼을 클릭하거나, 
            문제를 직접 입력하거나, 이미지를 업로드하세요
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Upload & Input */}
        <div className="space-y-6">
          {/* File Upload */}
          <div className="card">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              📤 문제 이미지 업로드
            </h2>
            
            <div className="space-y-4">
              {/* File input */}
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-500 transition-colors">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  className="hidden"
                  id="file-upload"
                />
                <label htmlFor="file-upload" className="cursor-pointer">
                  <div className="text-4xl mb-2">📷</div>
                  <p className="text-gray-600 mb-2">
                    클릭하여 이미지 선택
                  </p>
                  <p className="text-sm text-gray-500">
                    PNG, JPG, JPEG 지원
                  </p>
                </label>
              </div>

              {/* Preview */}
              {previewUrl && (
                <div className="border border-gray-200 rounded-lg p-4">
                  <p className="text-sm font-medium mb-2">미리보기:</p>
                  <img
                    src={previewUrl}
                    alt="Preview"
                    className="max-w-full h-auto rounded-lg shadow-md"
                  />
                  <p className="text-xs text-gray-500 mt-2">{selectedFile?.name}</p>
                </div>
              )}

              {/* Upload button */}
              <button
                onClick={handleUpload}
                disabled={!selectedFile || uploading}
                className={`btn-primary w-full ${
                  (!selectedFile || uploading) ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                {uploading ? (
                  <>
                    <span className="animate-spin">⏳</span> 업로드 중...
                  </>
                ) : (
                  <>📤 이미지 업로드 및 텍스트 인식</>
                )}
              </button>
            </div>
          </div>

          {/* OCR Text or Manual Input */}
          {(ocrText || imageId) && (
            <div className="card bg-blue-50 border border-blue-200">
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                {imageId ? '📝 이미지에서 인식된 문제' : '✍️ 문제 입력'}
              </h3>
              <textarea
                value={ocrText}
                onChange={(e) => setOcrText(e.target.value)}
                className="w-full p-3 border border-blue-300 rounded-lg font-mono text-sm"
                rows="12"
                placeholder="문제를 여기에 입력하거나 수정하세요...

예시:
A 5kg object is thrown vertically upward with initial velocity 20 m/s.
Calculate:
a) Maximum height
b) Time to reach max height
c) Total time in air
Given: g = 10 m/s²"
              />
              <div className="mt-3 bg-amber-50 border border-amber-200 rounded-lg p-3">
                <p className="text-xs text-amber-800 flex items-start gap-2">
                  <span className="text-lg">💡</span>
                  <span>
                    <strong>OCR 기능 안내:</strong> 현재 개발 모드에서는 이미지 업로드 후 
                    문제를 직접 입력하거나 수정해주세요. 실제 프로덕션에서는 
                    Google Gemini Vision이나 GPT-4 Vision을 통해 자동으로 
                    손글씨를 인식합니다.
                  </span>
                </p>
              </div>
            </div>
          )}
          
          {/* Manual Problem Input (no image) */}
          {!imageId && !ocrText && !selectedFile && (
            <div className="card bg-green-50 border border-green-200">
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                ✍️ 또는 문제를 직접 입력하세요
              </h3>
              <textarea
                value={ocrText}
                onChange={(e) => setOcrText(e.target.value)}
                className="w-full p-3 border border-green-300 rounded-lg font-mono text-sm"
                rows="10"
                placeholder="물리 문제를 직접 입력하세요...

예시:
A car accelerates from 0 to 30 m/s in 5 seconds.
Calculate:
a) The acceleration
b) The distance traveled
c) The average velocity"
              />
              <p className="text-xs text-green-700 mt-2">
                💡 이미지 업로드 없이도 문제를 직접 입력하여 AI 풀이를 받을 수 있습니다
              </p>
            </div>
          )}

          {/* Quick Sample Buttons */}
          {!ocrText && (
            <div className="card bg-gradient-to-r from-purple-50 to-blue-50 border-2 border-purple-200">
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                ⚡ 빠른 시작
              </h3>
              <p className="text-sm text-gray-700 mb-4">
                샘플 문제로 AI 풀이를 바로 체험해보세요
              </p>
              <div className="grid grid-cols-1 gap-2">
                <button
                  onClick={() => {
                    const sampleProblem = `A 2kg block is placed on a 30° inclined plane. 
The coefficient of kinetic friction is 0.3.
Calculate:
a) The acceleration of the block
b) The normal force
c) The friction force

Given: g = 10 m/s²`;
                    setOcrText(sampleProblem);
                  }}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-3 rounded-lg hover:from-blue-700 hover:to-purple-700 font-medium text-sm"
                >
                  📐 샘플 1: 경사면 문제 (역학)
                </button>
                <button
                  onClick={() => {
                    const sampleProblem = `A projectile is launched at 45° with initial velocity 40 m/s.
Calculate:
a) Maximum height reached
b) Range (horizontal distance)
c) Time of flight
Given: g = 10 m/s²`;
                    setOcrText(sampleProblem);
                  }}
                  className="bg-gradient-to-r from-green-600 to-teal-600 text-white px-4 py-3 rounded-lg hover:from-green-700 hover:to-teal-700 font-medium text-sm"
                >
                  🎯 샘플 2: 포물선 운동 (역학)
                </button>
                <button
                  onClick={() => {
                    const sampleProblem = `A series circuit has:
- Voltage source: 12V
- Resistor R1: 4Ω
- Resistor R2: 2Ω
Calculate:
a) Total resistance
b) Current in the circuit
c) Voltage across R1 and R2`;
                    setOcrText(sampleProblem);
                  }}
                  className="bg-gradient-to-r from-yellow-600 to-orange-600 text-white px-4 py-3 rounded-lg hover:from-yellow-700 hover:to-orange-700 font-medium text-sm"
                >
                  ⚡ 샘플 3: 직렬 회로 (전기)
                </button>
                <button
                  onClick={() => {
                    const sampleProblem = `Given a velocity-time graph showing:
- Phase 1 (0-4s): Linear increase from 0 to 20 m/s
- Phase 2 (4-8s): Constant velocity at 20 m/s
- Phase 3 (8-12s): Linear decrease from 20 to 0 m/s

Calculate:
a) Acceleration during phase 1
b) Total distance traveled  
c) Average velocity

[This problem includes graph analysis]`;
                    setOcrText(sampleProblem);
                  }}
                  className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-4 py-3 rounded-lg hover:from-indigo-700 hover:to-purple-700 font-medium text-sm"
                >
                  📊 샘플 4: 속도-시간 그래프 (운동학)
                </button>
              </div>
            </div>
          )}

          {/* Solve Button */}
          {ocrText && (
            <button
              onClick={handleSolve}
              disabled={solving}
              className={`btn-primary w-full text-lg py-4 ${
                solving ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              {solving ? (
                <>
                  <span className="animate-spin">🔄</span> AI가 문제를 풀고 있습니다...
                </>
              ) : (
                <>🚀 AI로 문제 풀이 시작</>
              )}
            </button>
          )}
        </div>

        {/* Right Column: Solution */}
        <div className="space-y-6">
          {error && (
            <div className="card bg-red-50 border border-red-200">
              <div className="flex items-start gap-3">
                <div className="text-2xl">❌</div>
                <div>
                  <h4 className="font-semibold text-red-900">오류</h4>
                  <p className="text-sm text-red-800">{error}</p>
                </div>
              </div>
            </div>
          )}

          {!solution && !error && (
            <div className="card bg-gray-50">
              <div className="text-center py-12 text-gray-500">
                <div className="text-6xl mb-4">🤖</div>
                <h3 className="text-xl font-semibold mb-2">AI 문제 풀이 대기중</h3>
                <p className="text-sm">
                  왼쪽에서 문제 이미지를 업로드하고<br />
                  "AI로 문제 풀이 시작" 버튼을 클릭하세요
                </p>
              </div>
            </div>
          )}

          {solution && (
            <SolutionDisplay solution={solution} />
          )}
        </div>
      </div>
    </div>
  );
};

// Solution Display Component
const SolutionDisplay = ({ solution }) => {
  const [activeStep, setActiveStep] = useState(0);

  return (
    <div className="space-y-6">
      {/* Image Analysis (if available) */}
      {solution.has_image && solution.image_description && (
        <div className="card bg-gradient-to-r from-purple-50 to-pink-50 border-2 border-purple-200">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-2xl">📸</span>
            <h3 className="text-xl font-bold text-purple-900">이미지 분석</h3>
          </div>
          <div className="bg-white rounded-lg p-4">
            <p className="text-sm text-gray-700 whitespace-pre-line">
              {solution.image_description}
            </p>
          </div>
        </div>
      )}

      {/* Problem Type & Given Info */}
      <div className="card bg-gradient-to-r from-green-50 to-blue-50">
        <div className="flex items-center gap-2 mb-4">
          <span className="text-2xl">✅</span>
          <h2 className="text-2xl font-bold text-green-800">풀이 완료!</h2>
        </div>
        
        <div className="bg-white rounded-lg p-4 mb-4">
          <h3 className="font-semibold text-gray-700 mb-2">문제 유형</h3>
          <div className="flex items-center gap-2">
            <p className="text-lg capitalize bg-blue-100 text-blue-800 px-3 py-1 rounded-full inline-block">
              {solution.problem_type}
            </p>
            {solution.has_image && (
              <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full">
                📊 그래프/다이어그램 포함
              </span>
            )}
          </div>
        </div>

        <div className="bg-white rounded-lg p-4">
          <h3 className="font-semibold text-gray-700 mb-2">주어진 정보</h3>
          <ul className="space-y-1">
            {solution.given_info.map((info, idx) => (
              <li key={idx} className="text-sm flex items-start gap-2">
                <span className="text-blue-600">•</span>
                <span>{info}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-white rounded-lg p-4 mt-4">
          <h3 className="font-semibold text-gray-700 mb-2">구하는 것</h3>
          <ul className="space-y-1">
            {solution.find.map((item, idx) => (
              <li key={idx} className="text-sm flex items-start gap-2">
                <span className="text-purple-600">➤</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Solution Steps */}
      <div className="card">
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          📚 풀이 과정
        </h2>

        {/* Step Navigation */}
        <div className="flex gap-2 mb-4 overflow-x-auto pb-2">
          {solution.solution_steps.map((step, idx) => (
            <button
              key={idx}
              onClick={() => setActiveStep(idx)}
              className={`px-4 py-2 rounded-lg font-medium whitespace-nowrap transition-colors ${
                activeStep === idx
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Step {step.step_number}
            </button>
          ))}
        </div>

        {/* Active Step Content */}
        {solution.solution_steps[activeStep] && (
          <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg p-6">
            <h3 className="text-lg font-bold text-blue-900 mb-3">
              {solution.solution_steps[activeStep].title}
            </h3>
            
            <p className="text-gray-700 mb-4">
              {solution.solution_steps[activeStep].explanation}
            </p>

            {solution.solution_steps[activeStep].formulas.length > 0 && (
              <div className="bg-white rounded-lg p-4 mb-4">
                <h4 className="font-semibold text-sm text-gray-600 mb-2">공식:</h4>
                {solution.solution_steps[activeStep].formulas.map((formula, idx) => (
                  <div key={idx} className="font-mono text-sm bg-gray-50 p-2 rounded mb-1">
                    {formula}
                  </div>
                ))}
              </div>
            )}

            {solution.solution_steps[activeStep].calculations.length > 0 && (
              <div className="bg-white rounded-lg p-4 mb-4">
                <h4 className="font-semibold text-sm text-gray-600 mb-2">계산:</h4>
                {solution.solution_steps[activeStep].calculations.map((calc, idx) => (
                  <div key={idx} className="font-mono text-sm bg-green-50 p-2 rounded mb-1">
                    {calc}
                  </div>
                ))}
              </div>
            )}

            <div className="bg-yellow-100 border-l-4 border-yellow-500 p-3 rounded">
              <p className="font-semibold text-sm text-yellow-800">
                결과: {solution.solution_steps[activeStep].result}
              </p>
            </div>
          </div>
        )}

        {/* Step Navigation Buttons */}
        <div className="flex justify-between mt-4">
          <button
            onClick={() => setActiveStep(Math.max(0, activeStep - 1))}
            disabled={activeStep === 0}
            className="px-4 py-2 bg-gray-200 rounded-lg disabled:opacity-50"
          >
            ← 이전 단계
          </button>
          <button
            onClick={() => setActiveStep(Math.min(solution.solution_steps.length - 1, activeStep + 1))}
            disabled={activeStep === solution.solution_steps.length - 1}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50"
          >
            다음 단계 →
          </button>
        </div>
      </div>

      {/* TikZ Diagrams */}
      {solution.tikz_diagrams && solution.tikz_diagrams.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            🎨 다이어그램
          </h2>
          {solution.tikz_diagrams.map((diagram, idx) => (
            <div key={idx} className="mb-6">
              <h3 className="font-semibold mb-2">{diagram.title}</h3>
              <div className="bg-white rounded-lg p-4 border border-gray-200">
                <pre className="text-xs overflow-x-auto bg-gray-50 p-3 rounded">
                  <code>{diagram.code}</code>
                </pre>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Final Answers */}
      <div className="card bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-200">
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          ✨ 최종 답안
        </h2>
        <div className="space-y-4">
          {solution.final_answers.map((answer, idx) => (
            <div key={idx} className="bg-white rounded-lg p-4 shadow-sm">
              <p className="font-semibold text-gray-800 mb-2">{answer.question}</p>
              <p className="text-2xl font-bold text-green-600 mb-2">{answer.answer}</p>
              <p className="text-sm text-gray-600">{answer.explanation}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProblemSolver;
