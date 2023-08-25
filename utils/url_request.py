from requests import Session, Response


class UrlRequest:
    """Класс для работы с запросами к интернет-адресам"""

    def __init__(self) -> None:
        self._session: Session = Session()

    def get_response(self, url: str) -> int:
        """Функция для получения статус-кода от сайта"""
        response: Response = self._session.get(url=url)
        return response.status_code
