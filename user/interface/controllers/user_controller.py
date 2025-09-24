from datetime import datetime
from dependency_injector.wiring import inject, Provide
from containers import Container
from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr, Field
from user.application.user_service import UserService

router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

@router.post("", status_code=201)
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
    # user_service: UserService = Depends(Provide["user_service"]),
    ) -> UserResponse:
    created_user = user_service.create_user(
        name=user.name,
        email=user.email,
        password=user.password
    )

    return created_user

class UpdateUser(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)

@router.put("/{user_id}")
@inject
def update_user(
    user_id: str,
    user: UpdateUser,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    user = user_service.update_user(
        user_id=user_id,
        name=user.name,
        password=user.password
    )

    return user

class GetUserResponse(BaseModel):
    total_count: int
    page: int
    users: list[UserResponse]

@router.get("")
@inject
def get_users(
    page: int = 1,
    items_per_page: int = 10,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> GetUserResponse:
    total_count, users = user_service.get_users(page, items_per_page)


    return {
        "total_count": total_count,
        "page": page,
        "users": users,
    }

@router.delete("", status_code=204)   # 204: 저장 후 편집 계속. 기본적으로 캐시 가능. 캐시에서 가져왔다면 ETag 헤더 포함.
@inject
def delete_user(
    user_id: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    # TODO: 다른 유저를 삭제할 수 없도록 토큰에서 유저 아이디를 구한다.
    
    user_service.delete_user(user_id)

# class CreateUserBody(BasdModel):
# DTO(Data Transfer Object) Pattern
# - Pydantic이 자동으로 타입/형식 검사
# - FastAPI가 자동으로 OpenAPI 스키마 생성
# - 필요한 필드만 노출

# created_user = user_service.create_user(
#     name=user.name,
#     email=user.email,
#     password=user.password
# )
# HTTP JSON -> DTO -> Application Layer

# 전체 데이터 흐름 추적

# HTTP Request (JSON)
#     ↓
# CreateUserBody (DTO) ← Pydantic 검증
#     ↓
# UserService.create_user() ← Application Layer
#     ↓
# User(Domain Entity) ← 비즈니스 로직
#     ↓
# UserRepository.save() ← Infrastructure
#     ↓
# Database