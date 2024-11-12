from pydantic import EmailStr
from src.entity.UserEntity import UserEntity as User
from src.helpers.templates import TemplatesEnum
from src.helpers.templates import TemplateEngine
from src.cache import CacheService
from src.helpers.errors import BadRequestException, NotFoundException


async def verify_user_by_code(code: str) -> None:
    confirmation_key: str = TemplateEngine.build_string(
        TemplatesEnum.CACHE.value.CONFIRMATION_RECORD.value, code
        )
    user_email: EmailStr = await CacheService.get(confirmation_key)
    if not user_email:
        raise BadRequestException('Ссылка недействительна')
    user_entity: User = User.get_or_none(User.email == user_email)
    if not user_entity:
        raise NotFoundException('Пользователь с таким email не найден')
    user_entity.is_verified = True
    user_entity.save()
