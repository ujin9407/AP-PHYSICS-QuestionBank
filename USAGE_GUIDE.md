# Physics Diagram Converter - 사용 가이드

## 🚀 서비스 URL

### 프론트엔드 (웹 애플리케이션)
**주소**: https://5173-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai

### 백엔드 API
**주소**: https://8000-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai
**API 문서**: https://8000-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai/docs

## 📋 주요 기능

### 1. 손글씨 다이어그램 업로드
- PNG, JPG, JPEG 형식의 이미지 지원
- 드래그 앤 드롭 또는 클릭하여 파일 선택
- 최대 파일 크기: 10MB

### 2. 다이어그램 유형 선택
다음 물리 다이어그램 유형 중 선택:
- **일반** (📐): 일반적인 물리 다이어그램
- **역학** (⚙️): 힘, 운동, 에너지 관련
- **전기** (⚡): 회로, 전기장
- **광학** (🔬): 빛, 렌즈, 반사
- **열역학** (🌡️): 열, 엔트로피, PV 다이어그램
- **양자** (⚛️): 에너지 준위, 파동함수

### 3. 템플릿 시스템
- 각 다이어그램 유형별 미리 정의된 템플릿 제공
- 템플릿 선택 시 더 정확한 변환 결과
- 7개의 기본 물리 템플릿 포함

### 4. 실시간 미리보기
- AI 변환 후 즉시 결과 확인
- 이미지 미리보기
- TikZ 코드 보기/복사

### 5. PDF 내보내기
- 생성된 다이어그램을 PDF로 다운로드
- TikZ 소스 코드 포함 옵션
- 커스텀 제목 설정

## 🎯 사용 방법

### Step 1: 다이어그램 유형 선택
화면 왼쪽의 다이어그램 유형 카드 중 하나를 선택하세요.

### Step 2: 설명 입력 (선택사항)
추가 설명을 입력하면 더 정확한 변환 결과를 얻을 수 있습니다.

### Step 3: 템플릿 선택 (선택사항)
사용 가능한 템플릿 중 적합한 것을 선택하세요.

### Step 4: 이미지 업로드
손글씨 물리 다이어그램 이미지를 드래그하거나 클릭하여 업로드하세요.

### Step 5: 변환 대기
AI가 자동으로 이미지를 분석하고 TikZ 코드로 변환합니다.

### Step 6: 결과 확인
- 오른쪽 패널에서 변환된 다이어그램 미리보기
- "TikZ 코드 보기" 버튼으로 소스 코드 확인
- "복사" 버튼으로 코드를 클립보드에 복사

### Step 7: PDF 내보내기
"PDF로 내보내기" 버튼을 클릭하여 최종 결과물을 다운로드하세요.

## 🔧 API 사용 예제

### 이미지 업로드
```bash
curl -X POST "https://8000-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai/api/upload" \
  -F "file=@diagram.png"
```

### 다이어그램 변환
```bash
curl -X POST "https://8000-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai/api/convert" \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": "your-image-id",
    "diagram_type": "mechanics",
    "description": "A mass on an inclined plane"
  }'
```

### 템플릿 조회
```bash
curl "https://8000-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai/api/templates"
```

### PDF 내보내기
```bash
curl -X POST "https://8000-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai/api/export/pdf" \
  -H "Content-Type: application/json" \
  -d '{
    "diagram_id": "your-diagram-id",
    "include_code": true,
    "title": "My Physics Diagram"
  }'
```

## 💡 팁과 권장사항

### 최상의 결과를 위한 팁:
1. **깨끗한 이미지**: 배경이 깨끗하고 대비가 명확한 이미지 사용
2. **적절한 유형 선택**: 다이어그램의 물리 분야에 맞는 유형 선택
3. **템플릿 활용**: 유사한 템플릿이 있다면 선택하여 사용
4. **설명 추가**: 특별한 기호나 개념이 있다면 설명란에 기재
5. **고해상도 이미지**: 가능한 한 선명한 이미지 사용

### 지원되는 다이어그램 요소:
- ✅ 기본 도형 (사각형, 원, 선)
- ✅ 화살표 및 벡터
- ✅ 텍스트 라벨 및 수식
- ✅ 각도 표시
- ✅ 좌표계
- ✅ 물리 기호 및 변수

## 🛠️ 로컬 개발 환경 설정

### 백엔드 실행
```bash
cd /home/user/webapp/backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 프론트엔드 실행
```bash
cd /home/user/webapp/frontend
npm install
npm run dev
```

## 📚 기술 스택

### 백엔드
- FastAPI 0.104.1
- Python 3.9+
- Uvicorn (ASGI 서버)
- Pillow (이미지 처리)
- ReportLab (PDF 생성)

### 프론트엔드
- React 18
- Vite 5
- TailwindCSS 3
- Axios (HTTP 클라이언트)
- React Dropzone (파일 업로드)

### AI 모델
- DaTikZv2 (손글씨 다이어그램 → TikZ 변환)

## ❓ 문제 해결

### 업로드 실패
- 파일 형식이 PNG, JPG, JPEG인지 확인
- 파일 크기가 10MB 이하인지 확인
- 인터넷 연결 상태 확인

### 변환 실패
- 이미지가 너무 흐릿하지 않은지 확인
- 다이어그램 유형이 올바른지 확인
- 템플릿을 선택해보세요

### PDF 내보내기 실패
- 변환이 완료되었는지 확인
- 브라우저의 팝업 차단이 해제되어 있는지 확인

## 📞 지원

문제가 발생하거나 질문이 있으시면:
1. API 문서 확인: https://8000-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai/docs
2. README.md 파일 참조
3. GitHub Issues 생성

---

**Physics Diagram Converter** - Powered by DaTikZv2 🚀
