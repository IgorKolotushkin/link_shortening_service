import re
from re import Match

from utils.utils import generate_suffix


class RegexUrl:
    """Класс для обработки URL регулярными выражениями"""

    _PATTERN_PREFIX: str = r"http\w?://"
    _PATTERN_ALIAS: str = _PATTERN_PREFIX + r"w{0,3}.?\w*"
    _PATTERN_HOME: str = r"http\w{0,1}://w{0,3}.?\w*.\w{2,4}"
    _PATTERN_HOME_WITHOUT: str = r"\w{0,3}.?\w*.\w{2,4}"
    _PATTERN_SUB: str = r"http\w?://w{0,3}\.?"
    _PATTERN_PARTS: str = r"(\w{3})(\w{2})"
    _PREFIX: str = "https://"

    def __init__(self) -> None:
        self._suffix: str = generate_suffix()

    def _get_prefix(self, url: str) -> str:
        """Метод проверки наличия префикса в URL"""
        result: Match[str] | None = re.match(self._PATTERN_PREFIX, url)
        return result.group(0)

    def _get_alias_and_short_url(self, url: str) -> tuple[str, str]:
        """Метод для получения псевдонима
        и короткого адреса из исходного url"""
        if not self._get_prefix(url):
            url: str = self._PREFIX + url
        result = re.search(self._PATTERN_ALIAS, url)
        alias = re.sub(self._PATTERN_SUB, "", result.group(0))
        parts_short_url: list = re.findall(self._PATTERN_PARTS, alias)[0]
        return alias, parts_short_url[0] + "." + parts_short_url[1]

    def _get_home_url(self, url: str) -> str:
        """Метод для получения домашнего адреса из исходного url"""
        prefix: str = self._get_prefix(url)
        if prefix:
            result: Match = re.search(self._PATTERN_HOME, url)
            return result.group(0)

        result: str = re.search(self._PATTERN_HOME_WITHOUT, url).group(0)
        return self._PREFIX + result

    def get_all_data_from_url(self, url: str):
        """Метод для поучения всей информации из url адреса"""
        alias_and_short: tuple[str, str] = self._get_alias_and_short_url(url=url)
        short_url: str = alias_and_short[1] + "/" + self._suffix
        home_url: str = self._get_home_url(url=url)
        return alias_and_short[0], short_url, home_url
