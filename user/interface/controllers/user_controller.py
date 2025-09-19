from dependency_injector.wiring import inject, Provide
from containers import Container
from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from user.application.user_service import UserService

router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel):
    name: str
    email: str
    password: str

@router.post("", status_code=201)
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
    # user_service: UserService = Depends(Provide["user_service"]),
    ):
    created_user = user_service.create_user(
        name=user.name,
        email=user.email,
        password=user.password
    )

    return created_user


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