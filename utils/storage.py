import json


class DataBase:
    """Класс для работы с файлом хранения данных"""

    def __init__(self) -> None:
        self.names_db: list = ["aliases", "short_url", "short_alias"]

    def read_db(self, name_db: str) -> dict:
        """Метод для загрузки данных в память"""
        with open(f"storage/{name_db}.json", "r") as file:
            result: dict = json.loads(file.read())
            return result

    def _write_db(self, name_db: str, data: dict) -> None:
        """Метод для сохранения данных после изменения"""
        with open(f"storage/{name_db}.json", "w") as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))

    def save_all_data(self, *args, **kwargs) -> None:
        """Метод для сохранения всех полученных данных в базу"""
        alias, short_url, home_url, user_url = args[0]
        database_alias, database_short, database_short_alias = kwargs.values()
        databases: list = [database_alias, database_short, database_short_alias]

        if alias not in database_alias["aliases"].keys():
            database_alias["aliases"][alias] = home_url
        if (
            alias not in database_short["short_url_db"]
            or short_url not in database_short["short_url_db"][alias]
        ):
            database_short["short_url_db"][alias] = {short_url: user_url}
        if alias not in database_short_alias["short_alias"]:
            database_short_alias["short_alias"][short_url] = alias

        for name, data in zip(self.names_db, databases):
            self._write_db(name_db=name, data=data)
