from dataclasses import dataclass


@dataclass(eq=False)
class AppError(Exception):
    """Base Error"""

    @property
    def message(self) -> str:
        return "Произошла ошибка в приложении"


class DomainError(AppError):
    """Base Domain Error"""

    @property
    def message(self) -> str:
        return "Произошла ошибка бизнес логики"
