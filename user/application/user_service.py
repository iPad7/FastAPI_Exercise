from dependency_injector.wiring import inject, Provide
from typing import Annotated
from fastapi import HTTPException, Depends
from ulid import ULID
from utils.crypto import Crypto
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository

class UserService:
    @inject
    def __init__(
            self,
            user_repo: IUserRepository,
    ):
        self.user_repo = user_repo
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(self, name: str, email: str, password: str, memo: str | None = None):
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
            memo=memo,
            created_at=now,
            updated_at=now,
        )
        self.user_repo.save(user)
        return user
    
    def update_user(
            self,
            user_id: str,
            name: str | None = None,
            password: str | None = None,
    ):
        user = self.user_repo.find_by_id(user_id)

        if name:
            user.name = name
        if password:
            user.password = password
        user.updated_at = datetime.now()

        self.user_repo.update(user)

        return user
    
    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        users = self.user_repo.get_users(page, items_per_page)

        return users
    

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