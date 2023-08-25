from utils.url_request import UrlRequest
from utils.regex import RegexUrl
from utils.deco import DbDecorator as db_decorator


class Message:
    """
    Класс для показа меню пользователю и выбора варианта отображения
    в зависимости от выбранного пункта меню
    """

    @classmethod
    def show_menu(cls) -> None:
        """Начальное меню пользователя"""
        print(
            "\nГлавное меню:\n"
            "1 - регистрация короткого интернет-адреса по стандартному URL\n"
            "2 - получение и проверка домашней страницы интернет-адреса по псевдониму\n"
            "3 - получение и проверка стандартного интернет-адреса по короткому URL\n"
            "4 - вывод информации о всех сокращённых URL\n"
            "5 - завершение программы\n"
        )

    @classmethod
    def get_answer(cls, menu_id: int):
        """Метод выбора класса для отображения информации пользователю"""
        classes = {
            1: MessageForAdd,
            2: MessageHomeUrl,
            3: MessageFullUrl,
            4: MessageAllInfo,
        }
        return classes.get(menu_id)()


class MessageForAdd:
    """Класс для вывода результатов пользователю при выборе первого пункта меню"""

    def __init__(self):
        self.regex: RegexUrl = RegexUrl()

    @db_decorator()
    def message(self, **kwargs) -> tuple[str, str, str, str]:
        """
        Метод генерации сообщения пользователю. Возвращает кортеж с данными из url.
        Эти данные используются в декораторе для сохранения в базу данных.
        """

        user_url: str = input("Введите стандартный url для регистрации: ")
        alias, short_url, home_url = self.regex.get_all_data_from_url(url=user_url)

        print(
            f"Короткий интернет-адрес: {short_url}\n"
            f"Псевдоним домашней страницы: {alias}\n"
            f"Стандартный интернет-адрес: {user_url}"
        )

        return alias, short_url, home_url, user_url


class MessageHomeUrl:
    """Класс для вывода домашней страницы по псевдониму"""

    def __init__(self) -> None:
        self.get_status_code: UrlRequest = UrlRequest()

    @db_decorator()
    def message(self, **kwargs) -> None:
        """Метод генерации сообщения пользователю"""
        data_alias, _, _ = kwargs.values()
        user_input: str = input("Введите псевдоним домашней страницы: ").lower()
        home_url: str | None = data_alias["aliases"].get(user_input, None)
        if home_url is None:
            print("Адрес домашней страницы не найден")
        else:
            response_code: int = self.get_status_code.get_response(url=home_url)
            print(
                f"Интернет-адрес домашней страницы: {home_url}\n"
                f"Псевдоним домашней страницы: {user_input}\n"
                f"Код ответа страницы: {response_code}"
            )


class MessageFullUrl:
    """Класс для формирования и вывода стандартного интернет адреса по короткому"""

    def __init__(self) -> None:
        self.get_status_code: UrlRequest = UrlRequest()

    @db_decorator()
    def message(self, **kwargs) -> None:
        """Метод генерации сообщения пользователю"""
        _, data_short, short_alias = kwargs.values()
        user_input: str = input("Введите сокращенный url: ").lower()
        alias: str | None = short_alias["short_alias"].get(user_input, None)
        if alias is None:
            print("Стандартный интернет-адрес не найден")
        else:
            full_url = data_short["short_url_db"][alias][user_input]
            response_code: int = self.get_status_code.get_response(url=full_url)
            print(
                f"Стандартный интернет адрес: {full_url}\n"
                f"Короткий интернет адрес: {user_input}\n"
                f"Код ответа страницы: {response_code}"
            )


class MessageAllInfo:
    """Класс для формирования и вывода информации по всем парам псевдонимов и коротких интернет-адресов"""

    def __init__(self) -> None:
        pass

    @db_decorator()
    def message(self, **kwargs) -> None:
        """Метод генерации сообщения пользователю"""
        data_alias, data_short, _ = kwargs.values()
        data_alias_print: list[tuple[str, str]] = [
            (alias, data_alias["aliases"][alias])
            for alias in data_alias["aliases"].keys()
        ]
        print("Псевдонимы:")
        for alias in data_alias_print:
            print(alias)

        data_short_url_print: list[tuple] = [
            (short, full)
            for keys in data_short["short_url_db"].items()
            for short, full in keys[1].items()
        ]
        print("Короткие интернет-адреса:")
        for urls in data_short_url_print:
            print(urls)
