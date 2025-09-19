from dependency_injector import containers, providers
from user.application.user_service import UserService

from user.infra.repository.user_repo import UserRepository

#########################################################################
# IoC(Inversion of Control) Container
# 애플리케이션이 구동될 때 IoC 컨테이너에 미리 의존성을 제공하는 객체를 등록해두고
# 필요한 모듈에서 주입하도록 할 수 있음
# 이렇게 되면 주입할 때의 타입을 인터페이스로 선언하더라도
# 실제로 주입되는 객체는 구현체가 되도록 할 수 있게 됨
#########################################################################

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        package=["user"]
    )

    user_repo = providers.Factory(UserRepository)
    user_service = providers.Factory(UserService, user_repo=user_repo)

#########################################################################
# providers 모듈에는 Factory 외에도 여러 종류의 프로바이더를 제공함.
# Factory: 객체를 매번 생성
# Singleton: 처음 호출될 때 생성한 객체를 재활용
#########################################################################