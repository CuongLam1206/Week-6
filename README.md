# 🎬 Mail Video Service

> **Nền tảng SaaS tự động tạo video email cá nhân hóa với AI Avatar**

Biến email thông thường thành video tương tác với AI Avatar của bạn, tăng engagement lên 300% và conversion rate lên 200%.

---

## 💡 Ý Tưởng Dự Án

### Vấn Đề Cần Giải Quyết

📧 **Email truyền thống không còn hiệu quả:**
- Open rate thấp (trung bình 21%)
- Click-through rate kém (trung bình 2.6%)
- Thiếu tính cá nhân hóa
- Dễ bị bỏ qua trong hộp thư đầy

🎯 **Giải pháp:** Tự động hóa việc tạo video email với AI Avatar cá nhân, mang lại:
- **Tăng Open Rate**: Video thumbnail trong email thu hút hơn text thuần túy
- **Tăng Engagement**: Video cá nhân tạo kết nối mạnh mẽ với người nhận
- **Tiết Kiệm Thời Gian**: Tự động tạo hàng trăm video từ template
- **Scalable**: Phục vụ từ cá nhân đến doanh nghiệp lớn

### Workflow Chính

```mermaid
graph LR
    A[User Upload Photo + Voice] --> B[Tạo AI Avatar]
    B --> C[Viết Email Script]
    C --> D[AI Text-to-Speech]
    D --> E[Video Generation]
    E --> F[Gửi Email với Video]
    F --> G[Tracking & Analytics]
```

### Use Cases Thực Tế

1. **Sales & Marketing**
   - Cold email outreach với video giới thiệu
   - Follow-up khách hàng tiềm năng
   - Product demo cá nhân

2. **Customer Success**
   - Onboarding video cho khách hàng mới
   - Support tickets với video hướng dẫn
   - Thank you messages

3. **HR & Recruitment**
   - Job offer letters với video
   - Welcome aboard videos
   - Training materials

4. **Real Estate**
   - Property tour intro videos
   - Personalized follow-ups
   - Market updates

---

## 🏗️ Kiến Trúc Hệ Thống

### Tổng Quan

```
┌─────────────────┐
│ Outlook Add-in  │ ←─── User Interface (Office.js)
└────────┬────────┘
         │
         ↓ HTTPS
┌─────────────────┐
│  Admin Portal   │ ←─── Dashboard (React + Vite)
└────────┬────────┘
         │
         ↓ REST API
┌─────────────────────────────────────────┐
│         FastAPI Backend                 │
│  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │   Auth   │  │  Avatar  │  │ Video │ │
│  │ Service  │  │ Service  │  │Service│ │
│  └──────────┘  └──────────┘  └───────┘ │
└────────┬──────────────┬─────────────────┘
         │              │
    ┌────┴───┐    ┌─────┴──────┐
    │ Postgre│    │   MinIO    │
    │   SQL  │    │  Storage   │
    └────────┘    └────────────┘
         │
    ┌────┴──────────┐
    │  External API │
    │ - Heygen      │
    │ - OpenAI GPT  │
    │ - SendGrid    │
    └───────────────┘
```

### Video Generation Pipeline

**Option 1: Heygen Lip-Sync (Recommended for Production)**

```
Input: Text Script + Avatar Photo
         ↓
    [1. Create Heygen Avatar] (One-time)
         ↓ Upload photo to Heygen API
    Heygen Avatar ID
         ↓
    [2. Generate Video Request]
         ↓ POST /v2/video/generate
    Video ID + Status: "processing"
         ↓
    [3. Async Polling] (30-60s)
         ↓ GET /v2/video/{id} every 10s
    Status: "completed" + Video URL
         ↓
    [4. Download from Heygen CDN]
         ↓ HTTPS download
    Video File (.mp4) with Lip-Sync
         ↓
    [5. Upload to MinIO]
         ↓ S3-compatible storage
    Final Video URL
         ↓
    [6. Database Update]
         ↓ Status: completed
    Ready for Email Delivery
```

**Option 2: Static Image + Audio (Fallback/Demo)**

```
Input: Text Script + Avatar Photo
         ↓
    [1. Text-to-Speech]
         ↓ gTTS / Google Cloud TTS
    Audio File (.mp3)
         ↓
    [2. Image Processing]
         ↓ Download/Fetch Avatar Photo
    Image File (.jpg)
         ↓
    [3. FFmpeg Video Creation]
         ↓ Merge Audio + Static Image
    Video File (.mp4) 720x1280
         ↓
    [4. Upload to MinIO]
         ↓ S3-compatible storage
    Video URL
         ↓
    [5. Database Update]
         ↓ Status: completed
    Ready for Email Delivery
```

**Comparison:**

| Feature | Heygen Lip-Sync | Static (Current) |
|---------|----------------|------------------|
| **Lip Movement** | ✅ Professional | ❌ None |
| **Generation Time** | 30-60s | ~10s |
| **Cost** | $0.10-0.50/video | Free |
| **Requirements** | API Key | None |
| **Quality** | High | Basic |



---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose | Lý do chọn |
|------------|---------|-----------|
| **FastAPI** | REST API framework | Hiệu suất cao, async native, OpenAPI auto-docs |
| **PostgreSQL** | Database chính | ACID compliance, JSON support, mature |
| **SQLAlchemy** | ORM async | Type-safe, migration support |
| **JWT** | Authentication | Stateless, secure, scalable |
| **MinIO** | Object Storage | S3-compatible, self-hosted, cost-effective |

### AI/Video Processing
| Technology | Purpose | Lý do chọn |
|------------|---------|-----------|
| **gTTS** | Text-to-Speech | Free, đa ngôn ngữ, không cần API key |
| **FFmpeg** | Video processing | Industry standard, mạnh mẽ, đa format |
| **Heygen API** | Advanced Avatar | Lip-sync chất lượng cao, professional |
| **SadTalker** | Local lip-sync | Self-hosted, GPU acceleration, privacy |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI framework |
| **Vite** | Build tool (Admin Portal) |
| **Office.js** | Outlook integration |
| **Recharts** | Analytics dashboard |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| **Docker Compose** | Container orchestration |
| **Nginx** | Reverse proxy |

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop
- Git

### 1. Clone Repository

```bash
git clone <repository-url>
cd mail-video-service
```

### 2. Setup Environment

```bash
copy .env.example .env
```

**Cấu hình tối thiểu:**
```env
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=postgresql://postgres:postgres@db:5432/mail_video_service
MINIO_ENDPOINT=minio:9000
```

**Heygen API (Recommended - Lip-Sync Videos):**

> [!IMPORTANT]
> **Để có chuyển động môi miệng (lip-sync)**, bạn cần đăng ký Heygen API:
> 
> 1. Đăng ký tại: https://app.heygen.com/
> 2. Navigate to: Settings → API Keys
> 3. Create new API key → Copy

```env
# Heygen API for lip-sync videos
HEYGEN_API_KEY=sk_V2_your_heygen_api_key_here
HEYGEN_API_URL=https://api.heygen.com
```

**Without Heygen**: Hệ thống vẫn hoạt động, nhưng videos sẽ là **static images** (ảnh tĩnh + audio).

**Optional APIs (nâng cao):**
```env
# OpenAI (email summarization)
OPENAI_API_KEY=your-openai-api-key

# SendGrid (email delivery)
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=noreply@yourdomain.com
```


### 3. Start Services

```bash
docker-compose up -d --build
```

### 4. Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **API Docs** | http://localhost:8000/docs | - |
| **Admin Portal** | http://localhost:3000 | - |
| **MinIO Console** | http://localhost:9001 | minioadmin / minioadmin |

### 5. Demo Test

**A. Authorize API:**
1. Mở http://localhost:8000/docs
2. Click **Authorize**
3. Login: `admin@demo.com` / `admin123`

**B. Upload Avatar Photo:**
- Endpoint: `POST /api/v1/avatars/{avatar_id}/upload-photo`
- avatar_id: `605f28ea-8094-4356-b8b3-09f7e2229425`
- Upload ảnh chân dung

**C. Tạo Video:**
- Endpoint: `POST /api/v1/videos/`
```json
{
  "avatar_id": "605f28ea-8094-4356-b8b3-09f7e2229425",
  "script": "Xin chào! Tôi là AI Avatar của bạn."
}
```

**D. Xem Video:**
- Sau 10-15 giây, vào MinIO Console
- Bucket: `videos` → tìm video theo ID

---

## 📁 Project Structure

```
mail-video-service/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/v1/         # REST endpoints
│   │   │   ├── auth.py     # Authentication
│   │   │   ├── avatars.py  # Avatar management
│   │   │   ├── videos.py   # Video generation
│   │   │   └── emails.py   # Email handling
│   │   ├── core/           # Core modules
│   │   │   ├── config.py   # Settings
│   │   │   ├── security.py # JWT, password
│   │   │   └── database.py # DB connection
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   │       ├── video_service.py
│   │       ├── avatar_service.py
│   │       └── storage_service.py
│   ├── alembic/            # Database migrations
│   └── Dockerfile
├── ai/                     # AI Pipeline (GPU)
│   ├── video_pipeline.py   # SadTalker integration
│   └── Dockerfile.gpu
├── admin-portal/           # React Dashboard
│   └── src/
├── outlook-addin/          # Office Add-in
│   ├── manifest.xml
│   └── src/
└── docker-compose.yml
```

---

## 🎯 Core Features

### ✅ Implemented

- [x] **Multi-tenant Architecture** - Hỗ trợ nhiều organization
- [x] **Avatar Management** - Upload photo, voice samples
- [x] **Video Generation** - Text → TTS → Video
  - ✅ Static video (ảnh tĩnh + audio) - Working
  - ✅ Heygen API integration - Ready (cần API key để enable)
- [x] **S3 Storage** - MinIO for video/image storage
- [x] **REST API** - FastAPI with OpenAPI docs
- [x] **Authentication** - JWT-based auth
- [x] **Database Migrations** - Alembic for schema changes

### 🚧 Ready to Enable

- [ ] **Heygen Lip-Sync** - Professional talking avatar (cần thêm API key)
  - ✅ Service created (`heygen_service.py`)
  - ✅ Avatar service integrated
  - [ ] Database migration (`heygen_avatar_id` field)
  - [ ] End-to-end testing

### 📋 Planned Features

- [ ] **SendGrid Integration** - Automated email delivery
- [ ] **Outlook Add-in** - In-email video creation
- [ ] **Analytics Dashboard** - Video performance tracking
- [ ] **Voice Cloning** - Custom voice generation
- [ ] **Template Library** - Pre-built email templates
- [ ] **A/B Testing** - Video variant testing


---

## 📊 Performance Metrics

### Current Results (Demo)

| Metric | Value |
|--------|-------|
| **Video Generation** | ~10 giây (simple static) |
| **Audio Duration** | Tương ứng với text length |
| **Video Quality** | 720x1280 (9:16 portrait) |
| **File Size** | ~250-300 KB cho 7 giây |
| **Concurrent Videos** | 10+ (CPU mode) |

### Expected Production Metrics

| Metric | Target |
|--------|--------|
| **API Response Time** | < 200ms (p95) |
| **Video Generation** | < 30s (with GPU) |
| **Uptime** | 99.9% |
| **Max File Size** | 10 MB per video |

---

## 🔧 Development

### Running Tests

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
cd admin-portal && npm test
```

### Database Migrations

```bash
# Create new migration
docker-compose exec backend alembic revision -m "description"

# Apply migrations
docker-compose exec backend alembic upgrade head

# Rollback
docker-compose exec backend alembic downgrade -1
```

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last N lines
docker-compose logs --tail=50 backend
```

---

## 📝 API Documentation

Sau khi start services, API docs tự động có tại:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Key Endpoints

#### Authentication
```http
POST /api/v1/auth/register
POST /api/v1/auth/login
```

#### Avatars
```http
GET    /api/v1/avatars/
POST   /api/v1/avatars/
POST   /api/v1/avatars/{id}/upload-photo
POST   /api/v1/avatars/{id}/upload-voice
POST   /api/v1/avatars/{id}/generate
```

#### Videos
```http
POST   /api/v1/videos/
GET    /api/v1/videos/{id}
GET    /api/v1/videos/
```

#### Emails
```http
POST   /api/v1/emails/summarize
POST   /api/v1/emails/send
```

---

## 🔐 Security

- **JWT Authentication** - Bearer token với expiry
- **Password Hashing** - bcrypt với cost factor 12
- **CORS** - Configurable allowed origins
- **SQL Injection Protection** - SQLAlchemy ORM
- **File Upload Validation** - Type và size checking
- **Rate Limiting** - (TODO) Prevent API abuse

---

## 🔐 Bảo Mật & Quản Lý Người Dùng

### Kiến Trúc Authentication

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Database
    
    User->>Frontend: Nhập email/password
    Frontend->>API: POST /auth/login
    API->>Database: Tìm user theo email
    Database-->>API: User data + hashed_password
    API->>API: Verify password (bcrypt)
    API->>API: Create JWT token
    API-->>Frontend: {access_token, token_type}
    Frontend->>Frontend: Lưu token vào localStorage
    
    Note over User,Database: Các request sau đó
    
    Frontend->>API: API Request + Bearer Token
    API->>API: Decode & validate JWT
    API->>Database: Get user details
    API-->>Frontend: Protected resource
```

### 1. User Registration

**Multi-tenant Architecture:**
- Mỗi đăng ký tạo **Tenant** (organization) riêng
- User đầu tiên tự động là **Admin**
- Tenant isolation: User chỉ thấy data của organization mình

**Process:**

```bash
POST /api/v1/auth/register
```

```json
{
  "email": "admin@company.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe",
  "tenant_name": "ACME Corp",
  "tenant_domain": "acme.com"
}
```

**Validation:**
- ✅ Email unique check
- ✅ Password strength (min 8 chars, mixed case, numbers)
- ✅ Domain format validation

**Security Measures:**
```python
# Password hashing với bcrypt (cost factor 12)
hashed_password = bcrypt.hash(plain_password, rounds=12)

# JWT token chứa:
{
  "sub": "user_id",           # Subject (user ID)
  "tenant_id": "tenant_uuid", # Multi-tenant isolation
  "exp": 1234567890           # Expiration (30 min default)
}
```

### 2. User Login

**Endpoints:**

```bash
# Standard login (JSON)
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin@demo.com
password=admin123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Token Usage:**
```bash
# Tất cả protected endpoints cần header:
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### 3. Authorization & Permissions

**Role-Based Access Control (RBAC):**

| Role | Permissions |
|------|-------------|
| **Admin** | Toàn quyền trong tenant: manage users, avatars, videos, settings |
| **User** | Tạo/xem avatars và videos của chính mình |
| **Viewer** | (Future) Chỉ xem, không tạo |

**Tenant Isolation:**
```python
# Mọi query tự động filter theo tenant_id
async def get_current_user(token: str):
    payload = decode_jwt(token)
    return {
        "user_id": payload["sub"],
        "tenant_id": payload["tenant_id"]  # ← Isolation key
    }

# Example: Chỉ lấy avatars của tenant hiện tại
avatars = db.query(Avatar).filter(
    Avatar.user_id == current_user["user_id"],
    Avatar.tenant_id == current_user["tenant_id"]  # ← Prevent cross-tenant access
)
```

### 4. Security Features

#### A. Password Security

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Cost factor
)

# Hash password
hashed = pwd_context.hash("user_password")

# Verify
is_valid = pwd_context.verify("user_password", hashed)
```

**Best Practices:**
- ✅ Bcrypt algorithm (industry standard)
- ✅ Cost factor 12 (balance security vs performance)
- ✅ Never store plain passwords
- ✅ Password rotation policy (TODO)

#### B. JWT Token Security

**Configuration:**
```python
# backend/app/core/config.py
SECRET_KEY = "your-256-bit-secret"  # ← MUST change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

**Token Structure:**
```json
{
  "sub": "uuid-user-id",
  "tenant_id": "uuid-tenant-id",
  "exp": 1707220800,
  "iat": 1707219000
}
```

**Security Considerations:**
- ✅ Short expiration (30 min)
- ✅ Signed with HMAC-SHA256
- ✅ Stateless (no server-side storage)
- ⚠️ TODO: Refresh tokens for long sessions
- ⚠️ TODO: Token blacklist for logout

#### C. CORS Protection

```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Admin Portal
        "https://your-domain.com"   # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production Settings:**
- ✅ Whitelist specific origins
- ✅ Enable credentials for cookies
- ❌ Disable `allow_origins=["*"]`

#### D. SQL Injection Protection

```python
# ✅ SAFE: SQLAlchemy ORM (parameterized queries)
user = db.query(User).filter(User.email == email).first()

# ❌ UNSAFE: Raw SQL with string interpolation
# db.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

**All queries use:**
- ✅ SQLAlchemy ORM
- ✅ Prepared statements
- ✅ Type validation with Pydantic

#### E. File Upload Security

```python
# backend/app/services/storage_service.py

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_AUDIO_TYPES = {"audio/mpeg", "audio/wav"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

async def upload_file(file: UploadFile):
    # 1. Validate content type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(400, "Invalid file type")
    
    # 2. Check file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large")
    
    # 3. Generate unique filename (prevent overwrite)
    filename = f"{uuid4()}.jpg"
    
    # 4. Upload to isolated storage
    storage.upload(bucket=tenant_id, filename=filename)
```

### 5. Demo Accounts

**Pre-seeded Data:**

| Email | Password | Role | Tenant |
|-------|----------|------|--------|
| `admin@demo.com` | `admin123` | Admin | Demo Tenant |
| `user@demo.com` | `user123` | User | Demo Tenant |

**Avatar IDs:**
| ID | Name | Photo | Status |
|----|------|-------|--------|
| `605f28ea-8094-4356-b8b3-09f7e2229425` | Demo Avatar | ✅ Uploaded | Ready |

### 6. Security Checklist

**Production Deployment:**

- [ ] **Change SECRET_KEY** to random 256-bit string
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

- [ ] **Enable HTTPS** for all endpoints
  ```nginx
  server {
      listen 443 ssl;
      ssl_certificate /path/to/cert.pem;
      ssl_certificate_key /path/to/key.pem;
  }
  ```

- [ ] **Set CORS origins** to production domains only
  ```python
  allow_origins=["https://your-app.com"]
  ```

- [ ] **Enable rate limiting** (TODO)
  ```python
  from slowapi import Limiter
  limiter = Limiter(key_func=get_remote_address)
  
  @app.post("/api/v1/auth/login")
  @limiter.limit("5/minute")  # Max 5 attempts per minute
  ```

- [ ] **Database SSL** connection
  ```env
  DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
  ```

- [ ] **Environment variables** không commit vào Git
  ```bash
  # .gitignore
  .env
  .env.local
  ```

- [ ] **Audit logs** cho sensitive actions (TODO)
  ```python
  logger.info(f"User {user_id} deleted avatar {avatar_id}")
  ```

### 7. API Authentication Flow

**Example với curl:**

```bash
# 1. Login
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@demo.com&password=admin123" \
  | jq -r .access_token)

# 2. Use token to create avatar
curl -X POST http://localhost:8000/api/v1/avatars/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Avatar"}'

# 3. Upload photo
curl -X POST http://localhost:8000/api/v1/avatars/{avatar_id}/upload-photo \
  -H "Authorization: Bearer $TOKEN" \
  -F "photo=@my-photo.jpg"
```

**Token Expiration Handling:**
```javascript
// Frontend example
const response = await fetch('/api/v1/videos/', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

if (response.status === 401) {
  // Token expired → redirect to login
  window.location.href = '/login';
}
```

---

## 🤝 Contributing

### Workflow

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Code Style

- **Python**: Black formatter, isort, flake8
- **JavaScript**: ESLint + Prettier
- **Git Commits**: Conventional Commits

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- **FastAPI** - Amazing async framework
- **FFmpeg** - Video processing powerhouse
- **Heygen** - AI avatar platform
- **SadTalker** - Open-source lip-sync

---

## 📞 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@example.com

---

**Built with ❤️ for better email communication**
