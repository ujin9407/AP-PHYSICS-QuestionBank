# Physics Diagram Converter 🔬

DaTikZv2를 활용한 물리 손글씨 다이어그램을 디지털 TikZ 다이어그램으로 변환하는 웹 애플리케이션

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 라이브 데모

**웹 애플리케이션**: https://5173-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai

**API 문서**: https://8000-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai/docs

## ✨ 주요 기능

- 📝 **손글씨 다이어그램 업로드**: PNG, JPG, JPEG 형식 지원 (최대 10MB)
- 🤖 **AI 기반 변환**: DaTikZv2를 사용한 정확한 TikZ 코드 자동 생성
- 👁️ **실시간 미리보기**: 변환된 다이어그램 즉시 확인
- 📋 **템플릿 시스템**: 6가지 물리 분야별 7개 템플릿 제공
- 📄 **PDF 내보내기**: 다이어그램과 소스 코드를 PDF로 저장
- 🎯 **다양한 물리 분야 지원**: 역학, 전기, 광학, 열역학, 양자역학

## 기술 스택

### Backend
- FastAPI (Python 3.9+)
- DaTikZv2 (AI 모델)
- LaTeX/TikZ (다이어그램 렌더링)
- PyPDF2 (PDF 변환)

### Frontend
- React 18
- Vite
- Axios
- TailwindCSS

## 📊 프로젝트 통계

- **총 코드 라인**: 2,100+ lines
- **구현된 파일**: 24개 (Python/JavaScript/JSX)
- **API 엔드포인트**: 8개
- **React 컴포넌트**: 4개
- **물리 템플릿**: 7개

## 🚀 빠른 시작

### 간편 실행 (스크립트 사용)

```bash
# 백엔드 서버 시작
./start_backend.sh &

# 프론트엔드 서버 시작
./start_frontend.sh &
```

### 수동 설정

#### 백엔드 설정

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 프론트엔드 설정

```bash
cd frontend
npm install
npm run dev
```

### 접속

- **웹 애플리케이션**: http://localhost:5173
- **API 문서**: http://localhost:8000/docs

## API 엔드포인트

- `POST /api/upload` - 손글씨 다이어그램 업로드
- `POST /api/convert` - 다이어그램 변환
- `GET /api/templates` - 템플릿 목록 조회
- `POST /api/render` - TikZ 코드 렌더링
- `GET /api/export/pdf/{id}` - PDF 다운로드

## 프로젝트 구조

```
webapp/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routers/
│   │   └── services/
│   ├── templates/
│   ├── uploads/
│   └── outputs/
├── frontend/
│   └── src/
│       ├── components/
│       ├── services/
│       └── styles/
└── README.md
```

## 📖 문서

- **[사용 가이드](USAGE_GUIDE.md)**: 상세한 사용 방법 및 팁
- **[배포 가이드](DEPLOYMENT.md)**: 서버 관리 및 프로덕션 배포

## 🎯 지원되는 다이어그램 유형

| 유형 | 아이콘 | 설명 | 템플릿 수 |
|------|--------|------|-----------|
| 일반 | 📐 | 일반적인 물리 다이어그램 | 1 |
| 역학 | ⚙️ | 힘, 운동, 에너지 | 2 |
| 전기 | ⚡ | 회로, 전기장 | 2 |
| 광학 | 🔬 | 빛, 렌즈, 반사 | 1 |
| 열역학 | 🌡️ | 열, 엔트로피, PV 다이어그램 | 1 |
| 양자 | ⚛️ | 에너지 준위, 파동함수 | 1 |

## 🛠️ 기술 상세

### 백엔드 아키텍처
```
FastAPI Framework
├── Router Layer (API 엔드포인트)
│   ├── Upload Router
│   ├── Convert Router
│   ├── Template Router
│   ├── Render Router
│   └── Export Router
├── Service Layer (비즈니스 로직)
│   ├── DaTikZ Service (AI 변환)
│   ├── Render Service (TikZ 렌더링)
│   ├── PDF Service (문서 생성)
│   └── Template Service (템플릿 관리)
└── Model Layer (데이터 구조)
```

### 프론트엔드 구조
```
React Application
├── Components
│   ├── UploadZone (파일 업로드)
│   ├── DiagramTypeSelector (유형 선택)
│   ├── TemplateSelector (템플릿 선택)
│   └── DiagramPreview (결과 표시)
├── Services
│   └── API Client (백엔드 통신)
└── Styles (TailwindCSS)
```

## 🔧 개발 환경

### 필수 요구사항
- Python 3.9+
- Node.js 20+
- npm 10+

### 선택 사항
- LaTeX (프로덕션 렌더링용)
- Docker (컨테이너화 배포)

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🙏 감사의 글

- **DaTikZv2**: AI 기반 TikZ 변환 엔진
- **FastAPI**: 고성능 Python 웹 프레임워크
- **React**: 사용자 인터페이스 라이브러리
- **TailwindCSS**: 유틸리티 기반 CSS 프레임워크

## 📞 지원 및 문의

- **이슈**: [GitHub Issues](https://github.com/your-repo/issues)
- **문서**: [Usage Guide](USAGE_GUIDE.md)
- **API 문서**: https://8000-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai/docs

---

**Physics Diagram Converter** - Transform handwritten physics diagrams into digital TikZ with AI 🚀
