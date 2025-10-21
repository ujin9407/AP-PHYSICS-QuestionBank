# 배포 가이드

## 현재 실행 중인 서비스

### ✅ 백엔드 서버 (FastAPI)
- **포트**: 8000
- **상태**: 🟢 Running
- **공개 URL**: https://8000-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai
- **API 문서**: https://8000-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai/docs
- **헬스체크**: https://8000-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai/health

### ✅ 프론트엔드 서버 (Vite + React)
- **포트**: 5173
- **상태**: 🟢 Running
- **공개 URL**: https://5173-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai
- **빌드**: Development mode with HMR

## 🚀 빠른 시작

### 웹 애플리케이션 접속
```
https://5173-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai
```

위 URL을 브라우저에서 열면 바로 Physics Diagram Converter를 사용할 수 있습니다!

## 🔧 서버 관리

### 서버 시작

#### 방법 1: 스크립트 사용 (권장)
```bash
# 백엔드
cd /home/user/webapp
./start_backend.sh

# 프론트엔드
cd /home/user/webapp
./start_frontend.sh
```

#### 방법 2: 직접 실행
```bash
# 백엔드
cd /home/user/webapp/backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 프론트엔드
cd /home/user/webapp/frontend
npm run dev
```

### 서버 중지
```bash
# 실행 중인 프로세스 찾기
ps aux | grep uvicorn
ps aux | grep vite

# 프로세스 종료
kill <PID>
```

### 서버 재시작
```bash
# 기존 프로세스 종료 후 재시작
pkill -f uvicorn
pkill -f vite

./start_backend.sh &
./start_frontend.sh &
```

## 📊 서비스 상태 확인

### 백엔드 헬스체크
```bash
curl http://localhost:8000/health
# 응답: {"status":"healthy"}
```

### 프론트엔드 확인
```bash
curl -I http://localhost:5173
# 응답: HTTP/1.1 200 OK
```

### 로그 확인
```bash
# 백엔드 로그는 터미널에 출력됨
# 프론트엔드 로그도 터미널에 출력됨
```

## 🔒 환경 변수 설정

### 백엔드 (.env)
```bash
cd /home/user/webapp/backend
cp .env.example .env
nano .env
```

필수 환경 변수:
- `DATIKZ_API_KEY`: DaTikZv2 API 키 (프로덕션용)
- `DATIKZ_API_URL`: DaTikZv2 API 엔드포인트

## 🏗️ 프로덕션 배포

### 1. 프론트엔드 빌드
```bash
cd /home/user/webapp/frontend
npm run build
# dist/ 디렉토리에 정적 파일 생성
```

### 2. 백엔드 프로덕션 모드
```bash
cd /home/user/webapp/backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. Nginx 설정 (선택사항)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 프론트엔드
    location / {
        root /home/user/webapp/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 백엔드 API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🐳 Docker 배포 (선택사항)

### Dockerfile 생성
```dockerfile
# 백엔드
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# 프론트엔드
FROM node:20-alpine
WORKDIR /app
COPY frontend/package*.json .
RUN npm install
COPY frontend/ .
RUN npm run build
CMD ["npm", "run", "preview"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATIKZ_API_KEY=${DATIKZ_API_KEY}
    volumes:
      - ./backend/uploads:/app/uploads
      - ./backend/outputs:/app/outputs

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend
```

## 🔍 트러블슈팅

### 포트가 이미 사용 중
```bash
# 포트 사용 프로세스 확인
lsof -i :8000
lsof -i :5173

# 프로세스 종료
kill -9 <PID>
```

### 패키지 의존성 오류
```bash
# 백엔드
cd /home/user/webapp/backend
pip install -r requirements.txt --force-reinstall

# 프론트엔드
cd /home/user/webapp/frontend
rm -rf node_modules package-lock.json
npm install
```

### CORS 오류
`backend/app/config.py`에서 CORS 설정 확인:
```python
cors_origins: List[str] = [
    "http://localhost:5173",
    "https://5173-i5i05lzj3t3eujl43229l-c07dda5e.sandbox.novita.ai"
]
```

## 📈 성능 최적화

### 백엔드
- Gunicorn을 사용한 멀티 워커 실행
- Redis 캐싱 추가
- 데이터베이스 연결 풀링

### 프론트엔드
- 프로덕션 빌드 사용
- CDN 활용
- 이미지 최적화
- Code splitting

## 🔐 보안 권장사항

1. **환경 변수**: 민감한 정보는 환경 변수로 관리
2. **HTTPS**: 프로덕션에서는 반드시 HTTPS 사용
3. **API 키**: DaTikZv2 API 키 보안 관리
4. **파일 업로드**: 파일 크기 및 타입 검증
5. **Rate Limiting**: API 요청 제한 설정

## 📝 유지보수

### 로그 관리
```bash
# systemd를 사용한 로그 관리
journalctl -u physics-diagram-backend -f
journalctl -u physics-diagram-frontend -f
```

### 백업
```bash
# 업로드 및 출력 파일 백업
tar -czf backup-$(date +%Y%m%d).tar.gz \
  backend/uploads backend/outputs
```

### 모니터링
- 서버 상태 주기적 확인
- 디스크 공간 모니터링
- API 응답 시간 측정

---

**현재 상태**: 🟢 모든 서비스 정상 작동 중
**마지막 업데이트**: 2025-10-21
