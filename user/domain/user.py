from dataclasses import dataclass
from datetime import datetime

################################################
# @dataclass
# Python 3.7부터 도입된 데이터 클래스 데코레이터
# @dataclass 없이 사용한다면 생성자를 통해 모든 attribute들에 대한 특성을 정의해야 함
# 예를 들어
# class User:
#     def __init__(self, id: str, name: str, email: str):
#         self.id = id
#         self.name = name
#         self.email = email
#
#     def __repr__(self):
#         return f"User(id='{self.id}', name='{self.name}', email='{self.email}')"
# 
# __init__(), __repr__(), __eq__() 메소드가 자동으로 생성됨
#
# 특징
# 1. @dataclass(frozen=True)를 통해 불변성 보장 가능
# 2. 메소드 없이 데이터만 담는 구조체 역할
# 3. 보일러플레이트 코드 제거.
#
# Domain Entity는 데이터 + 비즈니스 규칙만을 담는 순수한 객체여야 함.
# @dataclass는 이에 적절함.

@dataclass
class User:
    id: str
    name: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime