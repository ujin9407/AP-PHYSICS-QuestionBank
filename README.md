# Physics Diagram Converter

DaTikZv2를 활용한 물리 손글씨 다이어그램을 디지털 다이어그램으로 변환하는 웹 애플리케이션

## 기능

- 📝 **손글씨 다이어그램 업로드**: 물리 다이어그램 이미지를 업로드하여 디지털화
- 🤖 **AI 변환**: DaTikZv2를 사용한 자동 TikZ 코드 생성
- 👁️ **실시간 미리보기**: 생성된 다이어그램을 실시간으로 확인
- 📋 **템플릿 시스템**: 다양한 물리 다이어그램 템플릿 제공
- 📄 **PDF 내보내기**: 생성된 다이어그램을 PDF로 다운로드

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

## 설치 및 실행

### 백엔드 설정

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 프론트엔드 설정

```bash
cd frontend
npm install
npm run dev
```

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

## 라이선스

MIT License
