from fastapi import HTTPException
from ulid import ULID
from utils.crypto import Crypto
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository

class UserService:
    def __init__(self):
        self.user_repo: IUserRepository = UserRepository()
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(self, name: str, email: str, password: str):
        _user = None

        try:
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e
            
        if _user:
            raise HTTPException(status_code=422)

        now = datetime.now()
        user: User = User(
            id=self.ulid.generate(),
            name=name,
            email=email,
            password=self.crypto.encrypt(password),
            created_at=now,
            updated_at=now,
        )
        self.user_repo.save(user)
        return user
    

    # def __init__(self):
    #     self.user_repo: IUserRepository = UserRepository()
    #     왜 이렇게 관리하는 걸까?
    #     IUserRepository = Port(인터페이스. 이런 모양으로 넘겨주세요.)
    #     UserRepository = Adapter(실제 구현체.)
    #     1. 의존성 역전
    #     2. 테스트 용이성
    #         user_service.repo = MockUserRepository()
    #     3. 기술 교체 가능성
    #         class PostgreSQLUserRepository(IuserRepository):
    #             ...
    #         -> 이렇게 해도 UserService는 수정할 필요 없음
    # 핵심: "구체적인 것에 의존하지 말고, 추상적ㅇ니 것에 의존하라"
    # Domain Layer는 "저장한다"는 개념만 알면 됨
    # Infrastructure Layer가 "어떻게 저장하는지" 구현을 담당