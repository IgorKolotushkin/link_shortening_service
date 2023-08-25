from functools import wraps
from typing import Callable

from utils.storage import DataBase


class DbDecorator:
    """
    Класс-декоратор для загрузки данных в память
    с выбором загружаемого файла(зависит от класса)
    и сохранения полученных данных
    """

    def __init__(self) -> None:
        self.data_alias: dict | None = None
        self.data_short: dict | None = None
        self.short_alias: dict | None = None
        self.database: DataBase = DataBase()

    def __call__(self, cls) -> Callable:
        @wraps(cls)
        def wrapper(*args, **kwargs):
            # Тут пока не придумал, как сделать лучше
            if cls.__qualname__ in ["MessageForAdd.message", "MessageAllInfo.message"]:
                self.data_alias = self.database.read_db("aliases")
                self.data_short = self.database.read_db("short_url")
                self.short_alias = self.database.read_db("short_alias")
            elif cls.__qualname__ == "MessageHomeUrl.message":
                self.data_alias = self.database.read_db("aliases")
            elif cls.__qualname__ == "MessageFullUrl.message":
                self.data_short = self.database.read_db("short_url")
                self.short_alias = self.database.read_db("short_alias")

            result = cls(
                *args,
                data_alias=self.data_alias,
                data_short=self.data_short,
                short_alias=self.short_alias
            )

            if cls.__qualname__ == "MessageForAdd.message":
                self.database.save_all_data(
                    result,
                    data_alias=self.data_alias,
                    data_short=self.data_short,
                    short_alias=self.short_alias,
                )
            return result

        return wrapper
