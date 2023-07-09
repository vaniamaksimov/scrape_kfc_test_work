class BaseCrudError(Exception):
    message: str = ''


class InvalidAttrNameError(BaseCrudError):
    ...


class InvalidOperatorError(BaseCrudError):
    def __init__(self, operator: str, *args: object) -> None:
        self.message = f'Недопустимый оператор {operator}'
