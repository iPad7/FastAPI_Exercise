# FastAPI 실습

: FastAPI로 배우는 백엔드 프로그래밍 with 클린 아키텍처

## 환경 설정

### 가상환경: `./.venv`

```bash
# 가상 환경 생성
# 로컬에 python이 설치 및 환경 변수 설정되어 있어야 함.
python -m venv .venv

# 가상 환경 활성화(Windows 기준)
.\.venv\Scripts\activate

# 이후 모든 활동은 가상 환경을 활성화한 뒤 실행
```

### 라이브러리 의존성: `./requirements.txt`

```bash
pip install -r requirements.txt
```

### DB: Docker Container(MYSQL)

```bash
# 컨테이너 생성
docker run --name mysql-local -p 3306:3306/tcp -e MYSQL_ROOT_PASSWORD=test -d mysql:8
```

```bash
# Command Prompt에서 Container로 접근
docker exec -it <container_id> bash

# DB로 직접 접근
mysql -u root -p
```

```bash
# 마이그레이션
alembic init migrations
```

```bash
# User Table revision 파일 생성
alembic revision --autogenerate -m "messages to leave"
```

```bash
# 최신 revision 반영
alembic upgrade head

# 최근에 수행한 revision보다 앞에 있는 n개의 revision 실행
alembic upgrade +n

# 최근에 수행한 revision보다 뒤에 있는 n개의 revision 실행
alembic downgrade -n
```

